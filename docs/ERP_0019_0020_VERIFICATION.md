# ERP-0019–ERP-0020 — Integration and review

## Evidence collected in CI

The `development` branch now runs:

1. Django SQLite unit tests and SQL Server 2022 integration, schema, Unicode and concurrency tests.
2. Django migrations and core/document-sequence down/up migration rehearsal on disposable SQL Server.
3. ASP.NET Core EF migration and new document-number sequence down/up rehearsal on disposable SQL Server.
4. ASP.NET Identity/login, Role Master CRUD, Company Arabic value round-trip and duplicate rejection via actual HTTP.
5. ASP.NET document-sequence numeric/scoped/concurrent allocation xUnit integration tests.
6. React TypeScript and production build; Playwright on Django and ASP.NET backend using the unchanged frontend.
7. Django missing production secret/DB environment negative checks; migration drift checks.

No production data, secret, payment or existing customer instance is touched. See corresponding GitHub Actions run ID in `ERP_PROGRESS.json` only after all green tests.

## Review findings and disposition

- Fixed live ASP.NET antiforgery DI registration (build alone did not catch this).
- Added role-scoped Company write protection; future tenant/branch-scoped permission policy still WP06–09.
- Normalized current validation response shapes and documented remaining login CSRF / media upload parity pending WP05/WP10.
- Added SQL Server-locked per-series/year/branch counters. Final number formatting remains open business decision DEC-05; gap-free invoice issuance is not yet claimed.
- Company logo + DB update atomicity, unique ASP email index, Identity framework INT claim IDs, Company pagination, audit logging and full Arabic printing are tracked by their separate owner packages.
- WP01 requirement/evidence storage is version-controlled documents. There is no need for a runtime audit/traceability table in this scope.

ERP-0020 acceptance is limited to *current foundational surfaces*. Future feature-specific E2E remains pending its owning package.


## Final scoped verification — 2026-10-23

GitHub [Actions run 39911998441](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39911998441) completed all five jobs successfully on code commit `54901a8b2f7d630bbaf8056e5c15ab675a517053`.

- Django SQLite: 27 PASS + 5 SQL-only skipped; SQL Server: 32/32 PASS.
- ASP.NET Core: xUnit document sequence 3/3 PASS, EF migration forward/rollback/reapply PASS, Admin login/Role + Arabic Company CRUD REST smoke PASS.
- Playwright: Django 2/2 PASS, ASP 1/1 PASS, same frontend.
- React production build and ASP.NET Core Release build PASS.
- Production secret/DB missing negative checks PASS, no model migration drift.

**ERP-0019–0020 are complete only for WP01-owned traceability/foundation surfaces.** Downstream mandatory SRS acceptance cases (purchases, inventory, sales, returns, accounting, audit, printing) are still pending their owners and are NOT included in this sign-off.
