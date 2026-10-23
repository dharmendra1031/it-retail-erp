"""Disposable SQL Server smoke test for the ASP.NET Core API."""

import json
import os
import subprocess
import tempfile
import time
from http.cookiejar import CookieJar
from urllib.error import HTTPError, URLError
from urllib.request import HTTPCookieProcessor, Request, build_opener

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


def check_schema():
    connection = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=127.0.0.1,1433;DATABASE=erp_net_ci;UID=sa;"
        f"PWD={os.environ['DB_PASSWORD']};Encrypt=yes;TrustServerCertificate=yes;"
    )
    with pyodbc.connect(connection) as db:
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
    employee = build_opener(HTTPCookieProcessor(CookieJar()))
    _, employee_csrf = request(employee, "/api/auth/csrf")
    status, session = request(employee, "/api/auth/login", "POST", {
        "email": "sqlsales@example.test", "password": "StrongSalesPass123!", "rememberMe": False,
    }, employee_csrf["csrfToken"])
    assert status == 200 and not session["isAdmin"], "Branch employee login failed"
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
