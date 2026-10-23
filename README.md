# IT Retail ERP

Computer hardware, software and IT retail management system for Kuwait.

## Architecture

The ERP has one shared React frontend and two interchangeable backend implementations:

- `frontend/` — React + TypeScript + Vite
- `aspnet-core/` — ASP.NET Core API + Entity Framework Core + Identity + SQL Server
- `django/` — Django REST Framework API + Django auth + SQL Server

Both backends expose the same API contract so the React application can switch between them without UI changes.

Development work is done on the `development` branch and promoted to `main` after review.

## Core business flow

Supplier → Purchase → Inventory → Sales / Service → Customer → Payment → Profit / Reports

Quotation flow:

Customer → Quotation → Approval → Sales Invoice → Payment → Stock Update → Customer Ledger

## Database

Microsoft SQL Server 2019 is the initial production database.

## Identifier convention

Application entities use numeric auto-incrementing primary keys. UUID/GUID identifiers are not used. ASP.NET Core uses `long` / SQL Server `BIGINT IDENTITY`, and Django uses `BigAutoField`.

## API convention

Frontend requests use relative `/api` URLs. During development, Vite proxies requests to the selected backend. Authentication uses secure session cookies with CSRF protection.


## Quick start and verification

Required tools: .NET 10 SDK, Python 3.12+, Node.js 22+, SQL Server with ODBC Driver 18, and `dotnet-ef` version 10. Copy the matching `.env.example` for **one selected backend**, then configure local SQL Server (do not commit real credentials). Only run one backend at a time.

```bash
# Django option (from django/)
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

```bash
# ASP.NET Core option (from aspnet-core/)
dotnet tool install --global dotnet-ef --version 10.0.13
dotnet restore src/ITRetailERP.Web/ITRetailERP.Web.csproj
dotnet ef database update --project src/ITRetailERP.Web/ITRetailERP.Web.csproj
dotnet run --project src/ITRetailERP.Web/ITRetailERP.Web.csproj --urls http://localhost:5000
```

```bash
# React frontend (from frontend/, in a second terminal)
npm install
# Configure VITE_PROXY_TARGET in frontend/.env for the running backend.
npm run dev
```

The `development` branch CI verifies Django unit tests, real disposable SQL Server migrations/concurrency, ASP.NET Core build/migrations/API tests, frontend TypeScript build and Playwright browser smoke. Configuration failures are explicit; demo credentials must be changed before deployment.


## Development standards

The mandatory rules are in [docs/CODING_STANDARDS.md](docs/CODING_STANDARDS.md): minimal idiomatic code, reusable keyboard-first form navigation (Enter = next field; last Enter submits), English/Arabic with RTL/LTR, and API parity for both SQL Server backends. New forms must add Playwright keyboard and bilingual tests.
