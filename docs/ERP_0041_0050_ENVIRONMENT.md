# ERP-0041–ERP-0050 — Reproducible development environment

**Source:** SRS §§56, 59, 62, 65, 66. **Scope:** developer setup and deterministic checks for Django + SQL Server or ASP.NET Core + SQL Server, sharing the same React frontend.

## Acceptance and code inventory

| Requirement | Implementation and evidence |
|---|---|
| .NET 10 build | `aspnet-core/src/ITRetailERP.Web/ITRetailERP.Web.csproj`, GitHub Actions `aspnet` job |
| Connection string | `Program.cs` loads optional protected local `aspnet-core/.env`; missing `ConnectionStrings__DefaultConnection` fails with clear error |
| EF migrations/rollback | `Migrations/`, disposable SQL job upgrades/downgrades `DocumentSequences` and re-applies |
| Python | `django/requirements.txt`, Python 3.12, `mssql-django`, ODBC 18 for SQL Server |
| Django config safety | `django/config/settings.py` requires production `SECRET_KEY` and `DB_NAME`; `settings_test.py` is test-only SQLite |
| Django migration drift | `python manage.py makemigrations --check --dry-run` in CI |
| React build | `frontend/package.json`, Node 22, `npm run build` TypeScript + Vite |
| Switching backends | `frontend/.env.example` controls `VITE_PROXY_TARGET`; Playwright runs the same Role Master journey against Django and ASP |
| No secrets committed | `.gitignore` excludes .env; CI generates random SQL Server/test-admin secrets per run |
| Versioned configuration | `django/.env.example`, `aspnet-core/.env.example`, `frontend/.env.example` |

## Developer happy path

From a fresh clone, select exactly one backend. Copy that backend's `.env.example` to `.env` and set local SQL Server credentials and a strong app secret/admin password. Follow the repository root README to install Python/.NET/Node dependencies, migrate the selected backend and run React with the matching proxy target. For verification, use the CI workflow and disposable DB; do not run test migrations on live data.

## Negative checks

- No production Django `SECRET_KEY`: explicit startup failure.
- No production Django `DB_NAME`: explicit startup failure.
- No ASP.NET connection string: explicit startup failure.
- No local SQL Server/ODBC driver: EF/Django connection and migration checks fail; setup documents expected prerequisites.
- Migration drift: CI fails if Django changes lack migrations or EF model and snapshot diverge.
- No plaintext live credentials or production database are used by CI.

## Data design decision for ERP-0046–ERP-0050

WP03 is infrastructure, not a business data owner. It adds **no new SQL table**. The `DocumentSequences` schema belongs to WP02, created in its existing EF/Django migration. At the WP03 gate, verify those migrations apply to disposable SQL Server and reverse/reapply safely; do not add placeholder tables. Numeric BIGINT IDs, Unicode Company fields, document-number uniqueness and deferrals to future financial, branch and audit work packages remain unchanged.

## Ownership and limitations

Full production deployment, HTTPS reverse-proxy, secrets vault, license enforcement, Arabic RTL/printing, business posting/stock-ledger tests and mandatory audit trails are separate downstream work packages. They are not complete merely because a fresh test build succeeds. **Project-level CI verifies development prerequisites only.**
