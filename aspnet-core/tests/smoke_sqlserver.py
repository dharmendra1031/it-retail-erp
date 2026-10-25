"""Disposable SQL Server smoke test for the ASP.NET Core API."""

import json
from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
import tempfile
import time
from http.cookiejar import CookieJar
from urllib.error import HTTPError, URLError
from urllib.request import HTTPCookieProcessor, Request, build_opener
from urllib.parse import quote

import pyodbc


URL = "http://127.0.0.1:5000"
PROJECT = "aspnet-core/src/ITRetailERP.Web/ITRetailERP.Web.csproj"


def request(client, path, method="GET", payload=None, csrf=None, multipart=False):
    body = None
    headers = {}
    if payload is not None:
        if multipart:
            boundary = "ERP-Smoke-Boundary"
            fields = []
            for key, value in payload.items():
                if isinstance(value, tuple):
                    filename, mime, contents = value
                    fields.append(
                        f'--{boundary}\r\nContent-Disposition: form-data; '
                        f'name="{key}"; filename="{filename}"\r\n'
                        f'Content-Type: {mime}\r\n\r\n'.encode("utf-8")
                        + contents + b"\r\n"
                    )
                else:
                    fields.append(
                        f'--{boundary}\r\nContent-Disposition: form-data; '
                        f'name="{key}"\r\n\r\n{value}\r\n'.encode("utf-8")
                    )
            body = b"".join(fields) + f"--{boundary}--\r\n".encode("utf-8")
            headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        else:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

    if csrf:
        headers["X-CSRF-TOKEN"] = csrf

    try:
        response = client.open(Request(URL + path, data=body, headers=headers, method=method), timeout=10)
    except HTTPError as error:
        response = error

    data = response.read()
    return response.status, json.loads(data) if data else None


def sql_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=127.0.0.1,1433;DATABASE=erp_net_ci;UID=sa;"
        f"PWD={os.environ['DB_PASSWORD']};Encrypt=yes;TrustServerCertificate=yes;"
    )


def check_schema():
    with sql_connection() as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT is_unique FROM sys.indexes "
            "WHERE object_id=OBJECT_ID('AspNetUsers') AND name='EmailIndex'"
        )
        row = cursor.fetchone()
        assert row is not None and row[0] == 1, "NormalizedEmail index must be unique"
        for table in ("AspNetUsers", "AspNetRoles", "Companies"):
            cursor.execute(
                "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_NAME = ? AND COLUMN_NAME = 'Id'", table
            )
            assert cursor.fetchone()[0].lower() == "bigint", f"{table}.Id must be BIGINT"
            cursor.execute(
                f"SELECT COLUMNPROPERTY(OBJECT_ID('{table}'), 'Id', 'IsIdentity')"
            )
            assert cursor.fetchone()[0] == 1, f"{table}.Id must be IDENTITY"

        cursor.execute(
            "SELECT is_unique FROM sys.indexes WHERE object_id = OBJECT_ID('AspNetUsers') "
            "AND name = 'EmailIndex'"
        )
        assert cursor.fetchone()[0] == 1, "NormalizedEmail index must be unique"

        cursor.execute(
            "SELECT COUNT(*) FROM sys.check_constraints "
            "WHERE parent_object_id = OBJECT_ID('Units') "
            "AND name = 'CK_Units_DecimalPlaces'"
        )
        assert cursor.fetchone()[0] == 1, "Unit decimal precision CHECK constraint missing"

        try:
            cursor.execute(
                "INSERT INTO AspNetUserRoles (UserId, RoleId) VALUES (?, ?)",
                999999999, 999999999,
            )
            raise AssertionError("Orphan role relation should be rejected")
        except pyodbc.IntegrityError:
            db.rollback()



def check_api():
    client = build_opener(HTTPCookieProcessor(CookieJar()))
    for _ in range(40):
        try:
            status, tokens = request(client, "/api/auth/csrf")
            if status == 200:
                break
        except (URLError, TimeoutError):
            time.sleep(2)
    else:
        raise RuntimeError("ASP.NET Core API did not start")

    status, _ = request(client, "/api/roles")
    assert status == 401, f"Anonymous Role API expected 401, got {status}"

    status, _ = request(client, "/api/auth/login", "POST", {
        "email": os.environ["ERP_ADMIN_EMAIL"],
        "password": os.environ["ERP_ADMIN_PASSWORD"],
    })
    assert status == 403, "Login without CSRF must return 403"

    status, _ = request(client, "/api/auth/login", "POST", {
        "email": os.environ["ERP_ADMIN_EMAIL"], "password": "wrong password",
    }, tokens["csrfToken"])
    assert status == 401, "Invalid password must be rejected"

    status, account = request(
        client, "/api/auth/login", "POST",
        {"email": os.environ["ERP_ADMIN_EMAIL"],
         "password": os.environ["ERP_ADMIN_PASSWORD"], "rememberMe": False},
        tokens["csrfToken"],
    )
    assert status == 200 and account["isAdmin"], f"Admin login failed: {status}"

    status, tokens = request(client, "/api/auth/csrf")
    assert status == 200
    csrf = tokens["csrfToken"]

    status, _ = request(client, "/api/roles", "POST", {"name": "BlockedWithoutCsrf"})
    assert status == 403, "Role mutation without CSRF must be rejected"

    status, invalid_role = request(client, "/api/roles", "POST", {"name": "  "}, csrf)
    assert status == 400 and invalid_role == {"detail": "Invalid request."}, "Empty role name must be rejected"

    status, invalid_company = request(
        client, "/api/companies", "POST", {"nameEn": "   "}, csrf, multipart=True
    )
    assert status == 400 and invalid_company == {"detail": "Invalid request."}, "Whitespace company name must be rejected"

    status, catalog = request(client, "/api/permissions")
    assert status == 200 and any(item["code"] == "sales.reverse" for item in catalog), "Permission catalog missing"

    status, role = request(client, "/api/roles", "POST", {"name": "SQL Cashier"}, csrf)
    assert status == 201 and isinstance(role["id"], int), "Role creation failed"
    status, duplicate = request(client, "/api/roles", "POST", {"name": "sql cashier"}, csrf)
    assert status == 400 and duplicate == {"detail": "Role name already exists."}, "Duplicate Role name must be rejected"

    status, assigned = request(
        client, f"/api/roles/{role['id']}/permissions", "PUT",
        {"permissions": ["companies.add", "sales.view"]}, csrf,
    )
    assert status == 200 and assigned["permissions"] == ["companies.add", "sales.view"], "Role permissions not saved"
    status, denied = request(
        client, f"/api/roles/{role['id']}/permissions", "PUT",
        {"permissions": ["sales.post", "invalid.action"]}, csrf,
    )
    assert status == 400 and denied == {"detail": "Invalid request."}, "Unknown privilege accepted"
    status, saved = request(client, f"/api/roles/{role['id']}/permissions")
    assert status == 200 and saved["permissions"] == ["companies.add", "sales.view"], "Invalid update changed grants"

    status, changed = request(
        client, f"/api/roles/{role['id']}", "PUT", {"name": "SQL Sales"}, csrf
    )
    assert status == 200 and changed["name"] == "SQL Sales", "Role update failed"

    status, created_user = request(
        client, "/api/users", "POST",
        {
            "username": "sqlsales", "email": "sqlsales@example.test",
            "fullName": "SQL Sales", "mobile": "9876543210",
            "password": "StrongSalesPass123!", "roleIds": [role["id"]],
            "isActive": True,
        }, csrf,
    )
    assert status == 201 and created_user["roleIds"] == [role["id"]], "User with role creation failed"
    assert "password" not in created_user and "passwordHash" not in created_user, "Password leaked"

    status, deactivated = request(
        client, f"/api/users/{created_user['id']}", "PUT",
        {
            "username": "sqlsales", "email": "sqlsales@example.test",
            "fullName": "SQL Sales", "mobile": "9876543210",
            "roleIds": [role["id"]], "isActive": False,
        }, csrf,
    )
    assert status == 200 and deactivated["isActive"] is False, "User deactivation failed"
    employee = build_opener(HTTPCookieProcessor(CookieJar()))
    _, employee_csrf = request(employee, "/api/auth/csrf")
    status, _ = request(
        employee, "/api/auth/login", "POST",
        {"email": "sqlsales@example.test", "password": "StrongSalesPass123!", "rememberMe": False},
        employee_csrf["csrfToken"],
    )
    assert status == 401, "Disabled-user login unexpectedly permitted"

    status, category = request(client, "/api/categories", "POST", {
        "code": "COMPUTERS", "nameEn": "Computers", "nameAr": "الحواسيب",
    }, csrf)
    assert status == 201, f"Category creation failed: {status} {category}"
    status, searched = request(client, "/api/categories?search=" + quote("الحواسيب"))
    assert status == 200 and [row["id"] for row in searched] == [category["id"]], (
        f"Arabic category search failed: {status} {searched}"
    )
    status, searched = request(client, "/api/categories?search=computer")
    assert status == 200 and [row["id"] for row in searched] == [category["id"]], (
        f"English category search failed: {status} {searched}"
    )
    status, _ = request(client, "/api/categories", "POST", {
        "code": "INVALID-PARENT", "nameEn": "Invalid Parent", "parentId": 999999,
    }, csrf)
    assert status == 400, "Invalid parent was accepted"
    status, _ = request(client, "/api/categories", "POST", {
        "code": "computers", "nameEn": "Duplicate Root",
    }, csrf)
    assert status == 400, "Duplicate normalized root category code accepted"
    status, subcategory = request(client, "/api/categories", "POST", {
        "code": "LAPTOPS", "nameEn": "Laptops", "parentId": category["id"],
    }, csrf)
    assert status == 201, "Subcategory creation failed"
    status, _ = request(client, "/api/categories", "POST", {
        "code": "laptops", "nameEn": "Duplicate Sibling", "parentId": category["id"],
    }, csrf)
    assert status == 400, "Duplicate normalized sibling code accepted"
    with ThreadPoolExecutor(max_workers=2) as pool:
        sibling_statuses = list(pool.map(
            lambda _: request(client, "/api/categories", "POST", {
                "code": "SSD-RACE", "nameEn": "Concurrent SSD",
                "parentId": category["id"],
            }, csrf)[0], range(2),
        ))
    assert sorted(sibling_statuses) == [201, 400], (
        f"Concurrent duplicate siblings were not rejected: {sibling_statuses}"
    )
    status, cycle = request(client, f"/api/categories/{category['id']}", "PUT", {
        "code": "COMPUTERS", "nameEn": "Computers", "parentId": subcategory["id"],
    }, csrf)
    assert status == 400, "Cyclic category accepted"
    status, brand = request(client, "/api/brands", "POST", {
        "code": "DELL", "nameEn": "Dell", "nameAr": "ديل",
    }, csrf)
    assert status == 201, f"Brand creation failed: {status} {brand}"
    status, updated_brand = request(client, f"/api/brands/{brand['id']}", "PUT", {
        "code": "dell", "nameEn": "Dell Technologies", "nameAr": "ديل الجديدة",
        "isActive": True,
    }, csrf)
    assert status == 200 and updated_brand["code"] == "DELL", f"Brand update failed: {status} {updated_brand}"
    status, reloaded_brand = request(client, f"/api/brands/{brand['id']}")
    assert status == 200 and reloaded_brand["nameAr"] == "ديل الجديدة", "Arabic brand update was not persisted"
    status, _ = request(client, "/api/brands", "POST", {
        "code": "dell", "nameEn": "Duplicate Brand",
    }, csrf)
    assert status == 400, "Duplicate normalized brand code accepted"
    status, found_brands = request(client, "/api/brands?search=%D8%AF%D9%8A%D9%84")
    assert status == 200 and brand["id"] in [row["id"] for row in found_brands], "Arabic brand search failed"
    status, found_brands = request(client, "/api/brands?search=Technologies")
    assert status == 200 and brand["id"] in [row["id"] for row in found_brands], "English brand search failed"
    status, unit = request(client, "/api/units", "POST", {
        "code": "PCS", "nameEn": "Pieces", "decimalPlaces": 0,
    }, csrf)
    assert status == 201, f"Unit creation failed: {status} {unit}"
    status, updated_unit = request(client, f"/api/units/{unit['id']}", "PUT", {
        "code": "pcs", "nameEn": "Pieces", "nameAr": "قطعة", "decimalPlaces": 3,
    }, csrf)
    assert status == 200 and updated_unit["decimalPlaces"] == 3, (
        f"Unit update failed: {status} {updated_unit}"
    )
    status, reloaded_unit = request(client, f"/api/units/{unit['id']}")
    assert status == 200 and reloaded_unit["nameAr"] == "قطعة", "Arabic unit update was not persisted"
    status, found_units = request(client, "/api/units?search=%D9%82%D8%B7%D8%B9%D8%A9")
    assert status == 200 and unit["id"] in [row["id"] for row in found_units], "Arabic unit search failed"
    with sql_connection() as db:
        try:
            db.execute("UPDATE Units SET DecimalPlaces = 7 WHERE Id = ?", unit["id"])
        except pyodbc.IntegrityError:
            db.rollback()
        else:
            raise AssertionError("SQL Server allowed invalid decimal places")
    status, unchanged_unit = request(client, f"/api/units/{unit['id']}")
    assert status == 200 and unchanged_unit["decimalPlaces"] == 3, (
        "Rejected SQL precision update changed saved unit"
    )
    status, _ = request(client, "/api/units", "POST", {
        "code": "KG", "nameEn": "Kilograms", "nameAr": "كيلوغرام", "decimalPlaces": 6,
    }, csrf)
    assert status == 201, "Valid 6-decimal unit was rejected"
    status, _ = request(client, "/api/units", "POST", {
        "code": "NEG", "nameEn": "Negative Precision", "decimalPlaces": -1,
    }, csrf)
    assert status == 400, "Negative unit decimal places accepted"
    status, _ = request(client, "/api/units", "POST", {
        "code": "INVALID", "nameEn": "Wrong Precision", "decimalPlaces": 7,
    }, csrf)
    assert status == 400, "Invalid unit decimal places accepted"
    product = {
        "sku": "SKU-100", "barcode": "123456789012", "nameEn": "Laptop",
        "nameAr": "حاسوب محمول", "categoryId": subcategory["id"],
        "brandId": brand["id"], "unitId": unit["id"],
        "productType": "stock", "serialTracked": True,
        "costPrice": "250.000", "basePrice": "320.500",
        "minPrice": "300.000", "reorderLevel": "5.000000",
    }
    status, created_product = request(client, "/api/products", "POST", product, csrf)
    assert status == 201 and created_product["sku"] == "SKU-100", f"Product creation failed: {status} {created_product}"
    status, duplicate = request(client, "/api/products", "POST", {
        **product, "barcode": "987654321000",
    }, csrf)
    assert status == 400, "Duplicate SKU accepted"
    status, invalid_type = request(client, "/api/products", "POST", {
        **product, "sku": "SERVICE-01", "barcode": "",
        "productType": "nonstock",
    }, csrf)
    assert status == 400, "Non-stock with serial quantity accepted"
    status, _ = request(client, f"/api/categories/{category['id']}", "DELETE", csrf=csrf)
    assert status == 409, "Referenced category should be protected"
    status, _ = request(client, f"/api/categories/{subcategory['id']}", "DELETE", csrf=csrf)
    assert status == 409, "Category used by product must remain protected"
    status, _ = request(client, f"/api/brands/{brand['id']}", "DELETE", csrf=csrf)
    assert status == 409, "Referenced brand should be protected"
    status, _ = request(client, f"/api/units/{unit['id']}", "DELETE", csrf=csrf)
    assert status == 409, "Referenced unit should be protected"

    customer_data = {
        "code": "C-001", "nameEn": "Credit Shop", "nameAr": "عميل الائتمان",
        "addressAr": "الكويت", "mobile": "96599887766", "customerType": "corporate",
        "paymentTermsDays": 30, "creditLimit": "2500.750", "civilId": "123456",
        "companyName": "Credit Shop LLC", "contactPerson": "Ahmed",
        "telephone": "22221111", "email": "credit@example.test",
        "taxNumber": "VAT-555", "openingBalance": "50.250", "remarks": "Net 30",
    }
    status, customer = request(client, "/api/customers", "POST", customer_data, csrf)
    assert status == 201 and customer["code"] == "C-001" and customer["creditLimit"] == "2500.750", "Customer creation failed"
    assert customer["companyName"] == "Credit Shop LLC" and customer["openingBalance"] == "50.250", "Customer details missing"
    status, blank_email_customer = request(client, "/api/customers", "POST", {
        **customer_data, "code": "C-EMPTY-EMAIL", "email": "", "telephone": "",
    }, csrf)
    assert status == 201 and blank_email_customer["email"] == "", f"Blank optional Customer email rejected: {status} {blank_email_customer}"
    status, _ = request(client, "/api/customers", "POST", {
        **customer_data, "code": "C-BAD-EMAIL", "email": "not-an-email",
    }, csrf)
    assert status == 400, "Invalid Customer email was accepted"
    status, customer_updated = request(client, f"/api/customers/{customer['id']}", "PUT", {
        **customer_data, "contactPerson": "Fatima",
        "openingBalance": "60.375", "companyName": "Credit Shop Updated",
    }, csrf)
    assert status == 200 and customer_updated["contactPerson"] == "Fatima", f"Customer update failed: {status} {customer_updated}"
    assert customer_updated["openingBalance"] == "60.375", "Customer opening balance update lost decimal precision"
    status, reloaded_customer = request(client, f"/api/customers/{customer['id']}")
    assert status == 200 and reloaded_customer["companyName"] == "Credit Shop Updated", "Customer update was not persisted"
    for field in ("mobile", "nameAr"):
        status, rejected = request(client, "/api/customers", "POST", {
            **customer_data, field: "",
        }, csrf)
        assert status == 400, f"Required Customer {field} accepted: {status} {rejected}"
    status, duplicate_customer = request(client, "/api/customers", "POST", customer_data, csrf)
    assert status == 400, "Duplicate customer code accepted"
    status, invalid_credit = request(client, "/api/customers", "POST", {
        **customer_data, "code": "C-002", "creditLimit": "-5.000",
    }, csrf)
    assert status == 400, "Negative credit limit accepted"

    browser_customer = {
        "code": "C-BROWSER", "nameEn": "Credit Partner", "nameAr": "عميل تجريبي",
        "addressEn": "", "addressAr": "", "mobile": "96599887766", "contactPerson": "Ali",
        "telephone": "", "remarks": "", "paymentTermsDays": 30, "isActive": True,
        "companyName": "Credit Shop LLC", "civilId": "", "customerType": "retail",
        "creditLimit": "2500.750", "email": "", "taxNumber": "",
        "openingBalance": "15.250",
    }
    status, browser_customer_response = request(client, "/api/customers", "POST", browser_customer, csrf)
    assert status == 201, f"Browser-equivalent customer payload rejected: {status} {browser_customer_response}"

    supplier_data = {
        "code": "S-001", "nameEn": "Main Supplier", "nameAr": "المورد",
        "paymentTermsDays": 14, "openingBalance": "135.500",
        "creditLimit": "800.500", "contactPerson": "Omar",
        "telephone": "12345678", "remarks": "Net 14",
    }
    status, supplier = request(client, "/api/suppliers", "POST", supplier_data, csrf)
    assert status == 201 and supplier["openingBalance"] == "135.500", f"Supplier opening balance incorrect: {status} {supplier}"
    assert supplier["creditLimit"] == "800.500" and supplier["contactPerson"] == "Omar", "Supplier details missing"
    status, blank_email_supplier = request(client, "/api/suppliers", "POST", {
        **supplier_data, "code": "S-EMPTY-EMAIL", "email": "",
    }, csrf)
    assert status == 201 and blank_email_supplier["email"] == "", f"Blank optional Supplier email rejected: {status} {blank_email_supplier}"
    status, _ = request(client, "/api/suppliers", "POST", {
        **supplier_data, "code": "S-BAD-EMAIL", "email": "not-an-email",
    }, csrf)
    assert status == 400, "Invalid Supplier email was accepted"
    status, supplier_updated = request(client, f"/api/suppliers/{supplier['id']}", "PUT", {
        **supplier_data, "contactPerson": "Sara", "creditLimit": "955.125",
    }, csrf)
    assert status == 200 and supplier_updated["creditLimit"] == "955.125", f"Supplier update failed: {status} {supplier_updated}"
    status, reloaded_supplier = request(client, f"/api/suppliers/{supplier['id']}")
    assert status == 200 and reloaded_supplier["contactPerson"] == "Sara", "Supplier update was not persisted"
    status, duplicate_supplier = request(client, "/api/suppliers", "POST", supplier_data, csrf)
    assert status == 400 and duplicate_supplier == {"detail": "Code already exists."}, (
        f"Duplicate supplier error contract changed: {status} {duplicate_supplier}"
    )

    browser_supplier = {
        "code": "S-BROWSER", "nameEn": "First Supplier", "nameAr": "",
        "addressEn": "", "addressAr": "", "mobile": "", "contactPerson": "Omar",
        "telephone": "", "remarks": "", "paymentTermsDays": 0, "isActive": True,
        "taxNumber": "", "email": "", "openingBalance": "135.500", "creditLimit": "800.500",
    }
    status, browser_supplier_response = request(client, "/api/suppliers", "POST", browser_supplier, csrf)
    assert status == 201, f"Browser-equivalent supplier payload rejected: {status} {browser_supplier_response}"

    race_cases = (
        ("/api/customers", {**customer_data, "code": "C-RACE"}),
        ("/api/suppliers", {**supplier_data, "code": "S-RACE"}),
        ("/api/categories", {"code": "CAT-RACE", "nameEn": "Race Category"}),
        ("/api/brands", {"code": "BR-RACE", "nameEn": "Race Brand"}),
        ("/api/units", {"code": "UN-RACE", "nameEn": "Race Unit", "decimalPlaces": 0}),
    )
    for path, payload in race_cases:
        with ThreadPoolExecutor(max_workers=2) as pool:
            statuses = list(pool.map(
                lambda _: request(client, path, "POST", payload, csrf)[0], range(2),
            ))
        assert sorted(statuses) == [201, 400], (
            f"Concurrent duplicate write to {path} was not safely rejected: {statuses}"
        )

    status, _ = request(client, f"/api/suppliers/{supplier['id']}/documents", "POST", {
        "file": ("fake.jpg", "application/pdf", b"%PDF-1.7\\nwrong extension"),
    }, csrf, multipart=True)
    assert status == 400, "Mismatched Supplier document extension accepted"
    status, _ = request(client, f"/api/suppliers/{supplier['id']}/documents", "POST", {
        "file": ("oversized.pdf", "application/pdf", b"%PDF-" + b"x" * (5 * 1024 * 1024)),
    }, csrf, multipart=True)
    assert status == 400, "Supplier oversized document accepted"
    status, supplier_files = request(client, f"/api/suppliers/{supplier['id']}/documents")
    assert status == 200 and supplier_files == [], "Rejected upload saved a Supplier file"
    status, _ = request(client, f"/api/customers/{customer['id']}/documents", "POST", {
        "file": ("fake.png", "application/pdf", b"%PDF-1.7\\nwrong extension"),
    }, csrf, multipart=True)
    assert status == 400, "Mismatched Customer document extension accepted"

    document_data = ("proof.pdf", "application/pdf", b"%PDF-1.4\\nprivate")
    status, document = request(client, f"/api/customers/{customer['id']}/documents", "POST", {
        "file": document_data,
    }, csrf, multipart=True)
    assert status == 201 and document["fileName"] == "proof.pdf", "Private customer upload failed"
    with client.open(URL + f"/api/customers/{customer['id']}/documents/{document['id']}") as downloaded:
        assert downloaded.read() == b"%PDF-1.4\\nprivate", "Customer document changed"
        assert downloaded.headers.get("X-Content-Type-Options") == "nosniff", "Customer download allows MIME sniffing"
        assert downloaded.headers.get("Cache-Control") == "no-store", "Customer document can be cached"
    status, _ = request(client, f"/api/customers/{customer['id']}", "DELETE", csrf=csrf)
    assert status == 409, "Customer with protected documents must not delete"

    supplier_document = ("supply.pdf", "application/pdf", b"%PDF-1.7\\nsupply agreement")
    status, supplier_file = request(client, f"/api/suppliers/{supplier['id']}/documents", "POST", {
        "file": supplier_document,
    }, csrf, multipart=True)
    assert status == 201 and supplier_file["fileName"] == "supply.pdf", (
        f"Supplier document upload failed: {status} {supplier_file}"
    )
    with client.open(URL + f"/api/suppliers/{supplier['id']}/documents/{supplier_file['id']}") as response:
        assert response.read() == supplier_document[2], "Supplier document bytes changed"
        assert response.headers.get("X-Content-Type-Options") == "nosniff", "Supplier download allows MIME sniffing"
        assert response.headers.get("Cache-Control") == "no-store", "Supplier document can be cached"
    status, _ = request(client, f"/api/customers/{customer['id']}/documents/{supplier_file['id']}")
    assert status == 404, "Supplier document leaked through Customer endpoint"
    status, _ = request(client, f"/api/suppliers/{supplier['id']}/documents/{document['id']}")
    assert status == 404, "Customer document leaked through Supplier endpoint"
    status, _ = request(client, f"/api/suppliers/{supplier['id']}", "DELETE", csrf=csrf)
    assert status == 409, "Supplier with secured documents must not delete"

    status, company = request(
        client, "/api/companies", "POST",
        {"nameEn": "SQL Shop", "nameAr": "متجر اختبار", "isActive": "true"},
        csrf, multipart=True,
    )
    assert status == 201 and isinstance(company["id"], int), "Company creation failed"

    status, company = request(client, f"/api/companies/{company['id']}")
    assert status == 200 and company["nameAr"] == "متجر اختبار", "Arabic round-trip failed"

    status, invalid_update = request(
        client, f"/api/companies/{company['id']}", "PUT",
        {"nameEn": "   "}, csrf, multipart=True
    )
    assert status == 400 and invalid_update == {"detail": "Invalid request."}, "Blank Company update accepted"
    status, unchanged_company = request(client, f"/api/companies/{company['id']}")
    assert status == 200 and unchanged_company["nameEn"] == "SQL Shop", "Rejected Company update modified record"

    status, branch = request(client, "/api/branches", "POST", {
        "companyId": company["id"], "code": "HQ", "nameEn": "Head Office",
        "nameAr": "المكتب الرئيسي", "isActive": True,
    }, csrf)
    assert status == 201 and branch["companyId"] == company["id"], "Branch creation failed"
    status, duplicate_branch = request(client, "/api/branches", "POST", {
        "companyId": company["id"], "code": "HQ", "nameEn": "Duplicate",
    }, csrf)
    assert status == 400, "Duplicate branch code must be rejected"
    status, another_branch = request(client, "/api/branches", "POST", {
        "companyId": company["id"], "code": "B2", "nameEn": "Branch Two",
    }, csrf)
    assert status == 201, "Second branch missing"
    status, warehouse = request(client, "/api/warehouses", "POST", {
        "branchId": branch["id"], "code": "MAIN",
        "nameEn": "Main Warehouse", "nameAr": "المخزن الرئيسي",
    }, csrf)
    assert status == 201, "Warehouse creation failed"
    status, duplicate_warehouse = request(client, "/api/warehouses", "POST", {
        "branchId": branch["id"], "code": "MAIN", "nameEn": "Duplicate",
    }, csrf)
    assert status == 400, "Duplicate warehouse key accepted"

    status, assigned_user = request(client, f"/api/users/{created_user['id']}", "PUT", {
        "username": "sqlsales", "email": "sqlsales@example.test",
        "fullName": "SQL Sales", "mobile": "9876543210",
        "roleIds": [role["id"]], "isActive": True, "branchId": branch["id"],
    }, csrf)
    assert status == 200 and assigned_user["branchId"] == branch["id"], "Branch assignment failed"
    status, updated_grants = request(client, f"/api/roles/{role['id']}/permissions", "PUT", {
        "permissions": ["companies.add", "sales.view", "customers.view"],
    }, csrf)
    assert status == 200, "Customer reader grant was not saved"

    employee = build_opener(HTTPCookieProcessor(CookieJar()))
    _, employee_csrf = request(employee, "/api/auth/csrf")
    status, session = request(employee, "/api/auth/login", "POST", {
        "email": "sqlsales@example.test", "password": "StrongSalesPass123!", "rememberMe": False,
    }, employee_csrf["csrfToken"])
    assert status == 200 and not session["isAdmin"], "Branch employee login failed"
    for path in ("/api/categories", "/api/brands", "/api/units"):
        status, _ = request(employee, path)
        assert status == 403, f"Employee without catalog grant accessed {path}: {status}"
    status, customer_list = request(employee, "/api/customers")
    assert status == 200, "Customer reader cannot list customers"
    selected = next(row for row in customer_list if row["id"] == customer["id"])
    assert "civilId" not in selected, "Customer list exposes Civil ID to non-admin"
    status, customer_detail = request(employee, f"/api/customers/{customer['id']}")
    assert status == 200 and "civilId" not in customer_detail, "Customer detail exposes Civil ID"
    status, _ = request(employee, f"/api/customers/{customer['id']}/documents/{document['id']}")
    assert status == 403, "Customer reader downloaded protected file"
    status, _ = request(employee, "/api/customers", "POST", customer_data, employee_csrf["csrfToken"])
    assert status == 403, "Read-only user created Customer"
    status, _ = request(employee, f"/api/suppliers/{supplier['id']}/documents/{supplier_file['id']}")
    assert status == 403, "Non-Admin accessed Supplier private document"
    status, visible_branches = request(employee, "/api/branches")
    assert status == 200 and [item["id"] for item in visible_branches] == [branch["id"]], "Cross-branch list leaked"
    status, visible_warehouses = request(employee, "/api/warehouses")
    assert status == 200 and [item["id"] for item in visible_warehouses] == [warehouse["id"]], "Cross-branch warehouse leaked"
    status, _ = request(employee, f"/api/branches/{another_branch['id']}")
    assert status == 404, "Cross-branch record access allowed"
    _, employee_csrf = request(employee, "/api/auth/csrf")
    status, _ = request(employee, "/api/branches", "POST", {
        "companyId": company["id"], "code": "BAD", "nameEn": "Forbidden",
    }, employee_csrf["csrfToken"])
    assert status == 403, "Employee changed branch without permission"
    status, _ = request(client, f"/api/companies/{company['id']}", "DELETE", csrf=csrf)
    assert status == 409, "Referenced company must remain protected"
    status, _ = request(client, f"/api/branches/{branch['id']}", "DELETE", csrf=csrf)
    assert status == 409, "In-use branch must remain protected"

    from io import BytesIO
    from PIL import Image
    image = BytesIO()
    Image.new("RGB", (2, 2), "white").save(image, format="PNG")
    status, invalid_logo = request(client, "/api/companies", "POST", {
        "nameEn": "Bad Mime Shop", "logo": ("logo.png", "text/plain", image.getvalue()),
    }, csrf, multipart=True)
    assert status == 400, "Mismatched MIME type accepted"
    status, invalid_logo = request(client, "/api/companies", "POST", {
        "nameEn": "Corrupt Image Shop", "logo": ("logo.png", "image/png", b"not an image"),
    }, csrf, multipart=True)
    assert status == 400, "Invalid PNG signature accepted"

    status, oversized_logo = request(client, "/api/companies", "POST", {
        "nameEn": "Oversized Logo Shop",
        "logo": ("too-large.png", "image/png", b"X" * (2 * 1024 * 1024 + 1)),
    }, csrf, multipart=True)
    assert status == 400, "Oversized logo was accepted"
    status, logo_company = request(client, "/api/companies", "POST", {
        "nameEn": "Logo Shop", "logo": ("logo.png", "image/png", image.getvalue()),
    }, csrf, multipart=True)
    assert status == 201 and logo_company["logoUrl"], "Valid logo upload failed"
    with client.open(URL + logo_company["logoUrl"], timeout=10) as image_response:
        assert image_response.status == 200 and image_response.read() == image.getvalue(), "Uploaded logo unavailable"
    status, _ = request(client, f"/api/companies/{logo_company['id']}", "DELETE", csrf=csrf)
    assert status == 204, "Unreferenced Logo Company delete failed"

    status, _ = request(client, f"/api/roles/{role['id']}", "DELETE", csrf=csrf)
    assert status == 409, "Assigned role must remain protected"
    status, _ = request(client, "/api/auth/logout", "POST", csrf=csrf)
    assert status == 204, "Logout failed"
    status, _ = request(client, "/api/auth/me")
    assert status == 401, "Logout session must be invalidated"
    print("ASP.NET Core SQL Server schema, CSRF, session, Role and Arabic Company CRUD: PASS")


def main():
    check_schema()
    with tempfile.TemporaryFile(mode="w+") as log:
        server = subprocess.Popen(
            ["dotnet", "run", "--no-launch-profile", "--project", PROJECT,
             "--urls", URL],
            stdout=log, stderr=subprocess.STDOUT,
        )
        try:
            check_api()
        except Exception:
            log.seek(0)
            print(log.read()[-8000:])
            raise
        finally:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()


if __name__ == "__main__":
    main()
