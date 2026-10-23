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
            fields = [
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n"
                for key, value in payload.items()
            ]
            body = ("".join(fields) + f"--{boundary}--\r\n").encode("utf-8")
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

    status, role = request(client, "/api/roles", "POST", {"name": "SQL Cashier"}, csrf)
    assert status == 201 and isinstance(role["id"], int), "Role creation failed"
    status, duplicate = request(client, "/api/roles", "POST", {"name": "sql cashier"}, csrf)
    assert status == 400 and duplicate == {"detail": "Role name already exists."}, "Duplicate Role name must be rejected"

    status, changed = request(
        client, f"/api/roles/{role['id']}", "PUT", {"name": "SQL Sales"}, csrf
    )
    assert status == 200 and changed["name"] == "SQL Sales", "Role update failed"

    status, company = request(
        client, "/api/companies", "POST",
        {"nameEn": "SQL Shop", "nameAr": "متجر اختبار", "isActive": "true"},
        csrf, multipart=True,
    )
    assert status == 201 and isinstance(company["id"], int), "Company creation failed"

    status, company = request(client, f"/api/companies/{company['id']}")
    assert status == 200 and company["nameAr"] == "متجر اختبار", "Arabic round-trip failed"

    status, _ = request(client, f"/api/companies/{company['id']}", "DELETE", csrf=csrf)
    assert status == 204, "Company delete failed"
    status, _ = request(client, f"/api/roles/{role['id']}", "DELETE", csrf=csrf)
    assert status == 204, "Role delete failed"
    print("ASP.NET Core SQL Server schema, auth, Role CRUD and Arabic Company CRUD: PASS")


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
