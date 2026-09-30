# ERP-0010 — SQL Server migration and index review

**Reviewed development HEAD:** `9c1b8d5d2bf46b357f8ac8828f97cf2f2ff38845`

## Package-01 migration decision

Package 01 requirement traceability is version-controlled metadata, so it has no SQL Server table and requires no EF or Django migration. This is consistent with ERP-0006 through ERP-0009.

## Existing migration evidence

### ASP.NET
`20260918070000_InitialCreate.cs` and `ApplicationDbContextModelSnapshot.cs` show:
- Company, User and Role primary keys are BIGINT/long; Company uses SQL Server IDENTITY.
- Company English/Arabic fields use NVARCHAR.
- Company TaxNumber and CommercialRegistrationNumber have indexes.
- Identity username/role normalized names have unique indexes.
- NormalizedEmail has `EmailIndex` but it is not unique (DB-001).
- Identity claim support-table IDs are INT IDENTITY (DB-002 policy decision).

### Django
`accounts/migrations/0001_initial.py` and `companies/migrations/0001_initial.py` show:
- User, Role, AccessPermission and Company IDs use BigAutoField.
- User email, username, Role name and AccessPermission code are unique.
- Company tax/registration fields are indexed.
- Company bilingual fields are represented in the SQL Server-backed Django schema.

## Upgrade/rollback

No ERP-0010 migration is generated because there is no Package-01 runtime schema change. Therefore an upgrade/rollback execution for a new migration is N/A.

Existing migrations were reviewed statically only. No live SQL Server database was available through the repository connector, so existing-data duplicate/collation checks, migration application, rollback, schema diff and concurrency tests were **not run**.

DB-001 must not be “fixed” by blindly adding a unique normalized-email index: existing duplicate/null/collation behavior must first be inspected in a disposable/staged SQL Server database, followed by a data-safe migration and concurrency regression test.

## Result

No destructive or speculative schema change. DB-001 through DB-006 remain tracked. Financial/stock precision and transaction indexes remain DB-003 and are owned by their implementation packages.
