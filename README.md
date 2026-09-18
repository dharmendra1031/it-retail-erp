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
