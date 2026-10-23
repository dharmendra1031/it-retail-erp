# ERP-0061–0080: SQL Server keys, schema and migration acceptance

Source: SRS §§56, 57, 59 and 65. Owners: WP04 (database foundation); WP09/WP12 onward (future business tables and branch relations).

## Implementation inventory

- Django `apps.accounts.models.User`, `Role`, `AccessPermission`, `apps.companies.models.Company` and `apps.core.models.DocumentSequence` use numeric BIGINT auto-increment application PKs. Their migrations retain Unicode text columns and relationship FKs.
- ASP.NET Core `ApplicationUser`, `Company`, `IdentityRole<long>` and `DocumentSequence` use `long` / SQL Server `BIGINT IDENTITY`. EF migration/snapshot and Django migrations are inspected and drift-checked in CI.
- Uniqueness: Django login email, username, roles and permission code. ASP.NET normalized username, normalized role name and **new unique filtered normalized email index** `20261023080000_UniqueNormalizedEmail`. Before upgrading, the migration rejects existing duplicate normalized emails rather than modifying data. Rollback restores the prior non-unique email index.
- Orphaned user-role FK insertions are rejected in both SQL Server implementations. Document sequences enforce unique series/fiscal-year/branch and transaction lock safety.
- Company English/Arabic text survives SQL Server round trips in both APIs.

## Decimal and ID safety

No money or stock fields are part of WP04 yet. Their owning packages must use SQL `DECIMAL` with explicitly approved KWD fractional precision, never binary float for balances/posting. **No placeholder sales/ledger schema is created in WP04.** Frontend numeric ID transport is safe only within JavaScript's integer precision and should be reviewed before values approach `Number.MAX_SAFE_INTEGER`.

ASP.NET framework's own Identity claim rows currently have `INT` support IDs; they are not ERP business entity keys. Replacing those framework-generated fields is deferred for an explicit compatibility/migration review. All first-party business IDs are BIGINT. Production SQL Server 2019 compatibility requires a dedicated validation run; current CI databases use SQL Server 2022.

## Verification required

- Run `makemigrations --check --dry-run`; apply/rollback/re-apply EF and Django migrations on disposable SQL Server.
- Verify column identity and FK/unique constraints, Arabic round-trip, duplicate prevention and concurrent numbering.
- Run two-backend role/company APIs and Playwright; don't mark backend parity from builds alone.
- Never mutate production database during test execution.

## Step-wise verified acceptance

| Step | Outcome | Evidence |
|---|---|---|
| ERP-0061 | SRS database/Unicode/numeric-ID acceptance mapped to WP04 | `docs/SRS_BASELINE.md` |
| ERP-0062 | Reviewed EF/Django model definitions, indexes, SQL Server migrations and frontend ID serialization | `docs/ERP_CODE_INVENTORY.md` |
| ERP-0063 | Identified missing email uniqueness (now fixed), claim-table INT support keys and deferred finance decimal schema | `docs/ERP_DATABASE_REVIEW.md` |
| ERP-0064 | Django/EF disposable SQL Server migrations and Company/Role create/query verified | `aspnet-core/tests/smoke_sqlserver.py` |
| ERP-0065 | Filtered email uniqueness and user-role FK orphan rejection verified | `aspnet-core/src/ITRetailERP.Web/Migrations/20261023080000_UniqueNormalizedEmail.cs` |
| ERP-0066 | Existing app keys retained BIGINT Identity/BigAutoField and validated SQL indexes | `aspnet-core/src/ITRetailERP.Web/Data/ApplicationDbContext.cs` |
| ERP-0067 | No float money introduced; SQL DECIMAL KWD policy remains WP18+ decision, Unicode and rollback documented | `docs/ERP_0061_0080_DATABASE.md` |
| ERP-0068 | ASP.NET EF normalized-email unique index/model snapshot and non-destructive migration | `aspnet-core/src/ITRetailERP.Web/Migrations/ApplicationDbContextModelSnapshot.cs` |
| ERP-0069 | Django User/Role/Company numeric ID, Unicode and DB constraints reviewed | `django/apps/accounts/models.py` |
| ERP-0070 | Django and EF migrations forward/backward/reapply tested on disposable SQL Server | `aspnet-core/src/ITRetailERP.Web/Migrations/20261023080000_UniqueNormalizedEmail.cs` |
| ERP-0071 | Shared business API response/validation and numeric-ID transport contract documented | `docs/api-contract.md` |
| ERP-0072 | ASP.NET DocumentNumberService atomic SQL Server scope/concurrency remains owner-implemented | `aspnet-core/src/ITRetailERP.Web/Services/DocumentNumberService.cs` |
| ERP-0073 | Django numbering transactions/uniqueness verified against SQL Server | `django/apps/core/numbering.py` |
| ERP-0074 | Admin-only Company writes and Role access enforced; tenant/branch audit later WP06–09/WP46 | `django/apps/companies/api.py` |
| ERP-0075 | Shared React rejects unsafe JavaScript integers from BIGINT JSON; no money endpoints yet | `frontend/src/api/client.ts` |
| ERP-0076 | English/Arabic Company Unicode in SQL Server and RTL/keyboard Playwright checks | `frontend/e2e/erp.spec.ts` |
| ERP-0077 | ASP.NET migrations, normalized email index and xUnit SQL tests 4/4 PASS | `aspnet-core/tests/ITRetailERP.Tests/DocumentNumberTests.cs` |
| ERP-0078 | Django unique email/orphan relation/concurrency checks PASS on SQL Server | `django/apps/accounts/tests.py` |
| ERP-0079 | SQL Server + React browser suites green for presently implemented masters/auth | `frontend/e2e/erp.spec.ts` |
| ERP-0080 | Schema/review reconciliation; no production database touched, finance/stock deferred | `docs/ERP_DATABASE_REVIEW.md` |

**CI:** [39920485489](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39920485489): all five jobs PASS; Django SQL Server 47/47, ASP.NET SQL xUnit 4/4, Playwright Django 9/9 and ASP.NET 8/8. No production migration. Completion covers this package only, not later inventory, sales, accounts or full Arabic report printing.
