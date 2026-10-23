# ERP-0018 — Django unit and parity verification gate

**Branch:** `development`
**Baseline reviewed:** `e294bb3d6d1d983d5841b8e41d32873c0f5be0eb`
**Status:** OPEN — static inspection completed; runtime tests not executed.

## Package scope and ownership

WP01 owns version-controlled SRS traceability, gap evidence and test contracts. Shared test harness belongs to WP03; API parity belongs to WP02/WP49; action permissions belong to WP06–WP09/WP49; Company Master runtime issues belong to WP10/WP48. Do not introduce duplicate framework components solely for WP01.

## Verified source inventory

- `django/apps/accounts/api.py`: CSRF token, session login/logout and current-user response.
- `django/apps/accounts/authentication.py`: DRF session authentication.
- `django/apps/accounts/models.py`: User, Role and AccessPermission models.
- `django/apps/companies/api.py`: authenticated Company CRUD without role or company-scope enforcement.
- `django/apps/companies/serializers.py`: Company DTO, bilingual fields, logo validation and file storage.
- `django/apps/companies/models.py`: Company entity and bilingual fields.
- `django/config/api_urls.py`: auth and Company routes without trailing slash.
- `django/config/settings.py`: SQL Server configuration and BigAutoField default.
- `frontend/src/api/client.ts`, `frontend/src/api/companies.ts`: shared request and form-data contract.
- `aspnet-core/src/ITRetailERP.Web/Controllers/Api/AuthController.cs`, `CompaniesApiController.cs`: reference API routes and responses.

## Required Django unit tests (not executed)

1. Login: valid credentials return numeric user ID, name and email; invalid credentials return 401; session logout returns 204.
2. CSRF: missing or invalid token rejects mutating requests; valid token permits authorized requests.
3. Company serializer: required English name, field lengths, bilingual Arabic/English round-trip, optional fields, valid/invalid email and website.
4. Company CRUD: create returns 201, list and get return the shared DTO, update returns 200, delete returns 204, missing entity returns 404.
5. Logo: oversized, unsupported and invalid image content rejected; failure during DB save does not destroy the previous logo.
6. Database: Company/User/Role/Permission IDs are BIGINT auto-increment; migrations apply cleanly to disposable SQL Server database.
7. Authorization: authenticated restricted user cannot modify/delete Company; response 403, no DB mutation and required audit evidence. **Deferred to WP06–WP09/WP49.**

## Required backend parity checks (not executed)

- Same auth endpoints and response keys: `/api/auth/csrf`, `/api/auth/login`, `/api/auth/me`, `/api/auth/logout`.
- Same Company endpoints and response keys: `/api/companies`, `/api/companies/{id}`.
- Compare successful and invalid requests, HTTP statuses, Unicode preservation, null/empty values, upload limits, CSRF and permissions.
- Switch `VITE_PROXY_TARGET` without modifying React UI code. **Execution owned by WP02/WP49.**

## Source-level findings

- `CompanyViewSet.permission_classes = [IsAuthenticated]` does not enforce action-specific or company-scoped authorization.
- `django/config/settings.py` falls back to `dev-only-secret-key`; production must require a real secret.
- Login code has no explicit throttling; ASP.NET Core uses `lockoutOnFailure: true`.
- ASP.NET Core and Django logo handling and validation need equivalent negative-case coverage.
- No verified Django test execution, SQL Server migration run, API parity run or browser E2E run in this review.

## Execution gate

Run `python manage.py check`, Django unit tests, disposable SQL Server migration/integration tests and backend parity tests when a suitable runtime and test database are available. Record exact commands, failures, successes and environment. Do not mark tests passing without execution. Keep ERP-0018 open until the applicable WP01 acceptance evidence is recorded and reviewed.

**Changes:** documentation only. No application code, SQL schema, migration, secrets or production data modified.
