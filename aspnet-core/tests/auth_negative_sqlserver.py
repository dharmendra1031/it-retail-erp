"""Run after the UI smoke tests: intentionally lock the ephemeral CI administrator."""

import os
import subprocess
import tempfile
import time
from urllib.error import URLError

import smoke_sqlserver as smoke


def main():
    smoke.URL = "http://127.0.0.1:5001"
    client = smoke.build_opener(smoke.HTTPCookieProcessor(smoke.CookieJar()))

    with tempfile.TemporaryFile(mode="w+") as output:
        server = subprocess.Popen(
            ["dotnet", "run", "--no-launch-profile", "--project", smoke.PROJECT,
             "--urls", smoke.URL],
            stdout=output, stderr=subprocess.STDOUT,
        )
        try:
            for _ in range(40):
                try:
                    status, tokens = smoke.request(client, "/api/auth/csrf")
                    if status == 200:
                        break
                except (URLError, TimeoutError):
                    time.sleep(2)
            else:
                raise RuntimeError("Authentication smoke API did not start")

            for _ in range(5):
                status, _ = smoke.request(
                    client, "/api/auth/login", "POST",
                    {"email": os.environ["ERP_ADMIN_EMAIL"], "password": "WrongPass123!"},
                    tokens["csrfToken"],
                )
                assert status == 401, f"Expected 401 after invalid password, got {status}"

            status, _ = smoke.request(
                client, "/api/auth/login", "POST",
                {"email": os.environ["ERP_ADMIN_EMAIL"],
                 "password": os.environ["ERP_ADMIN_PASSWORD"]},
                tokens["csrfToken"],
            )
            assert status == 401, "Correct password must not bypass the 15-minute lockout"
            print("ASP.NET Core password lockout: PASS")
        except Exception:
            output.seek(0)
            print(output.read()[-8000:])
            raise
        finally:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()


if __name__ == "__main__":
    main()
