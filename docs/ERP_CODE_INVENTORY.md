# ERP-0002 — current code inventory

**SRS:** https://docs.google.com/document/d/1Gb_pMJAN14UY0scLJjGBGiuRZdlXOWJARB1aLkzIobc/edit?usp=sharing. **Reviewed development HEAD:** `c35b46803ec7bf0cec2dd9e29a0ee402d3677f98`. **Date:** 2026-09-29.
**Source evidence:** complete non-truncated GitHub tree (76 files), plus inspection of authentication, Company, schema/migration, routing and React integration code. No runtime test is claimed.

## aspnet-core — 14 key files

| Source file | Verified source-level behavior |
|---|---|
| `aspnet-core/src/ITRetailERP.Web/Program.cs` | .env loading, SQL Server DbContext, Identity<long>, CSRF and controller middleware |
| `aspnet-core/src/ITRetailERP.Web/Controllers/Api/AuthController.cs` | CSRF, current-user, login and logout endpoints |
| `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CompaniesApiController.cs` | Authenticated Company CRUD and logo handling |
| `aspnet-core/src/ITRetailERP.Web/Contracts/CompanyRequest.cs` | Company form validation and multipart contract |
| `aspnet-core/src/ITRetailERP.Web/Contracts/CompanyResponse.cs` | Company response with long ID and logo URL |
| `aspnet-core/src/ITRetailERP.Web/Models/ApplicationUser.cs` | Numeric Identity user + full name; User Master API absent |
| `aspnet-core/src/ITRetailERP.Web/Models/Company.cs` | Company bilingual fields and audit timestamps |
| `aspnet-core/src/ITRetailERP.Web/Data/ApplicationDbContext.cs` | Identity<long>, Companies DbSet, tax/registration indexes |
| `aspnet-core/src/ITRetailERP.Web/Data/IdentitySeeder.cs` | Bootstrap admin if DB/configuration available |
| `aspnet-core/src/ITRetailERP.Web/Migrations/20260918070000_InitialCreate.cs` | Initial Identity and Company BIGINT IDENTITY tables |
| `aspnet-core/src/ITRetailERP.Web/Migrations/ApplicationDbContextModelSnapshot.cs` | EF baseline snapshot |
| `aspnet-core/src/ITRetailERP.Web/Services/CompanyLogoStorage.cs` | Logo limits, extension filtering and local uploads |
| `aspnet-core/src/ITRetailERP.Web/ITRetailERP.Web.csproj` | .NET 10, Identity/EF/SQL Server/DotNetEnv packages |
| `aspnet-core/src/ITRetailERP.Web/appsettings.json` | Non-secret default configuration |

## django — 12 key files

| Source file | Verified source-level behavior |
|---|---|
| `django/config/api_urls.py` | Only Auth and Company REST URLs |
| `django/config/settings.py` | SQL Server ODBC/env and BigAutoField |
| `django/apps/accounts/api.py` | Session/CSRF login, logout and me |
| `django/apps/accounts/authentication.py` | DRF session authentication |
| `django/apps/accounts/models.py` | User, Role and AccessPermission models; management APIs absent |
| `django/apps/accounts/migrations/0001_initial.py` | Numeric account/role/permission schema |
| `django/apps/companies/api.py` | Authenticated Company ModelViewSet |
| `django/apps/companies/models.py` | Company bilingual fields and indexed tax/registration |
| `django/apps/companies/serializers.py` | CamelCase Company serializer and logo validation |
| `django/apps/companies/migrations/0001_initial.py` | Numeric Company PK migration |
| `django/apps/core/models.py` | Timestamp abstract base |
| `django/requirements.txt` | Django, DRF, SQL Server and file dependencies |

## frontend — 13 key files

| Source file | Verified source-level behavior |
|---|---|
| `frontend/src/App.tsx` | Session check; Login or Company page only |
| `frontend/src/api/client.ts` | Same-origin requests and CSRF token |
| `frontend/src/api/auth.ts` | Authentication API requests |
| `frontend/src/api/companies.ts` | Company API multipart CRUD |
| `frontend/src/components/Login.tsx` | Login form |
| `frontend/src/components/AppShell.tsx` | Company-only sidebar |
| `frontend/src/components/Companies.tsx` | Company CRUD and filtered list |
| `frontend/src/components/CompanyForm.tsx` | Company fields and logo editor |
| `frontend/src/components/CompanyTable.tsx` | Company table and row actions |
| `frontend/src/main.tsx` | React bootstrapping |
| `frontend/src/styles.css` | Shared and responsive styling |
| `frontend/vite.config.ts` | Selected backend proxy |
| `frontend/package.json` | React/Vite/TypeScript scripts |

## Verified feature boundaries

| Feature | ASP.NET | Django | React | Status |
|---|---|---|---|---|
| Authentication | Identity login/logout/me/CSRF | Django session login/logout/me/CSRF | Login/client | Source implementation present; runtime parity unverified |
| Company Master | Company CRUD, validation and file storage | Company CRUD, serializer and file storage | Form, list, search, edit/delete | Source implementation present; end-to-end validation pending |
| User/Role/Permission Master | Identity foundations only | User/Role/AccessPermission models only | No master page | Pending APIs, enforcement and UI |
| Customer/Supplier/Product/Tax | Not found in tree | Not found in tree | Not found in tree | Pending |
| Purchase/Inventory/Serial/Warranty | Not found in tree | Not found in tree | Not found in tree | Pending |
| Quotation/Sales/POS/Payment/Return | Not found in tree | Not found in tree | Not found in tree | Pending |
| Service/Reports/Printing/Backup | Not found in tree | Not found in tree | Not found in tree | Pending |

## Review notes for ERP-0003

- `GET /api/companies` materializes the whole list in ASP.NET (`ToListAsync`); no server-side pagination appears. Django exposes the full Company queryset without an explicit pagination contract. Evaluate against SRS scale requirements.
- Company logo and database writes occur in separate operations; evaluate consistency and rollback if upload or second database save fails.
- Authentication uses session cookies/CSRF, but ERP role/action permissions are not yet exposed or enforced for specific business operations.
- No tracked unit/integration/E2E test suite appears in the reviewed repository tree; latest build, actual migrations and browser behavior require execution.
- Existing User/Role/Company schema must not be mistaken for completed master workflows.

**Verification type:** source inspection/tree presence and SRS inventory cross-check only. Actual .NET/Django builds, SQL migrations and React/E2E tests not run in this inventory step.
