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
