# ERP-0004 — happy-path acceptance specification

**SRS trace:** §5 Company Master; §3–4 English/Arabic master data; §59 authenticated access. **Plan:** Package 01, ERP-0004. **Status:** specification only; no runtime pass asserted.

## Trace HP-01: Create and retrieve a bilingual Company

| Link | Requirement and concrete evidence |
|---|---|
| Requirement | SRS §5 requires Company name, address, contacts, registration/tax information, logo and document identity; §§3–4 require Arabic Unicode. |
| ASP.NET | `aspnet-core/src/ITRetailERP.Web/Models/Company.cs`; `Data/ApplicationDbContext.cs`; `Controllers/Api/CompaniesApiController.cs` (`POST /api/companies`, `GET /api/companies/{id}`). |
| Django | `django/apps/companies/models.py`, `migrations/0001_initial.py`, `api.py` (`CompanyViewSet`); confirm registered `/api/companies` route before execution. |
| Shared UI | `frontend/src/components/Companies.tsx` calls `createCompany` and `getCompanies`; `CompanyForm` and `frontend/src/api/companies.ts` must be checked during execution. |
| Database | ASP.NET initial migration: `Companies.Id bigint IDENTITY`, `NameEn/NameAr nvarchar(200)`; Django migration: `BigAutoField`, `name_en/name_ar CharField`. |
| Test ownership | ASP.NET Company API integration test; Django Company API integration test; React browser test against each backend; SQL Server migration/readback test. These are proposed tests, not existing passing evidence. |

### Preconditions
1. Separate disposable SQL Server test databases for each backend, with migrations applied and a test administrator authenticated; do not run against production.
2. A CSRF token/session obtained through the backend's documented auth flow; the same frontend request contract works with either `VITE_PROXY_TARGET`.
3. Test input: unique English name `ERP Acceptance Company`, Arabic name `شركة اختبار النظام`, English/Arabic addresses, valid contact information and a unique test registration number. Logo is optional for the initial deterministic trace; test logo separately after DB-005 is repaired.

### Execution and expected assertions
1. Open Company Master in React as an authorized test administrator; fill English/Arabic names and save.
2. Assert the request reaches `POST /api/companies` and returns a successful creation response with a **numeric** positive ID; no UUID/public ID.
3. Fetch `GET /api/companies/{id}`; assert exact persisted English/Arabic names, active status and equivalent response fields for both backends.
4. Query the corresponding SQL Server test database; assert the row exists once, its primary key is BIGINT auto-generated and Arabic characters round-trip unchanged.
5. Reload the Company Master screen; assert the company appears and the user sees no save error. Compare the backend-specific response shapes and validation behavior.
6. Remove test data only from the disposable test database after capturing evidence. Do not alter production.

### Completion gate
Record test file paths, commands, output, backend selection, SQL Server migration/readback evidence and React E2E evidence. A static source trace establishes only that the intended route exists; **HP-01 remains unverified** until the actual integration/E2E checks pass. Authorization denial is the separate ERP-0005 negative-case specification; granular Company permissions are not yet implemented.

### Known blockers and boundaries
- DB-005: logo file and database persistence are not failure-atomic; exclude logo upload from this initial trace until fixed and regression-tested.
- DB-006: Company list pagination is missing; use a small isolated fixture for this acceptance case, not as performance sign-off.
- Current Company APIs enforce authentication, not action-specific permissions. Do not claim the eventual SRS authorization acceptance case passes.
- No money/stock transaction is part of this trace; financial DECIMAL and stock/ledger atomicity remain pending their owning packages.
