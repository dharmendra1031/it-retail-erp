# ERP-0018 — Django unit verification

**Branch:** `development`  
**Status:** COMPLETE for current WP01 scope on 2026-10-23  
**Verified code commit:** `ecfaa0887be2d197467567a1416e84c6ce5aa7cd`

## Actual execution evidence

[GitHub Actions run 39905510876](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39905510876):

- `python manage.py check` — PASS.
- `DJANGO_SETTINGS_MODULE=config.settings_test python manage.py test apps.accounts apps.companies --verbosity 2` — **22/22 PASS** in isolated SQLite (not SQL Server).
- ASP.NET Core `dotnet build --configuration Release` — PASS, 0 warnings and 0 errors.
- React `npm run build` — PASS (TypeScript and Vite).

Django tests cover Role Master CRUD, duplicate/invalid names, superuser/Admin-role authorization, forbidden non-admin access, assigned and protected roles, Company validation, routes, and Company create/update/delete restrictions. Production SQL Server data was not modified.

## Scope and deferred acceptance

WP01 tracks SRS ownership and evidence in version-controlled files; no runtime requirement-owner table or endpoint is owned here. WP02/WP49 owns cross-backend API parity and browser acceptance. WP03 owns the shared test harness. WP05 owns full auth and CSRF negative-case coverage, WP10 owns Company/Logo runtime acceptance, WP06–WP09 own the complete permission and company/branch scoping system. **None of these tests is claimed passed here.**

Pending integration includes SQL Server migrations and SQL-side numeric ID/Unicode verification, logo persistence failure recovery, login throttle/CSRF regression, company-scoped access and missing-evidence audit trails. Those remain explicitly outside this WP01 gate; ERP-0019 owns next applicable SQL/concurrency/E2E checks.

The role data migration `accounts.0002_admin_role` adds the initial reserved Admin role with `get_or_create`; no new business table is added. See `docs/ERP_DATABASE_REVIEW.md` review 018.
