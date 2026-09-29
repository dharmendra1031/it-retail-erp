# Mandatory ERP database design review

Every hourly run must inspect relevant actual ASP.NET EF models/migrations, Django models/migrations and SQL Server schema where access is available. Record a dated entry here even for documentation-only steps; include evidence and test limitations.

## Per-run checklist

1. Numeric auto-increment IDs, FK/delete behavior, business-key uniqueness and indexes.
2. Unicode Arabic/English storage and DECIMAL(p,s) money; no float money.
3. ASP.NET/Django ERP entity, migration and API behavior parity.
4. Document/serial uniqueness, transaction states, posting idempotency and concurrency.
5. Stock/ledger atomicity, reconciliation and immutable audit trail.
6. Migration forward/rollback, existing-data safety and runtime checks.
7. Fix proven issues with safe migrations/tests; otherwise record blocker and required evidence; never alter production destructively.

## Review 001 — 2026-09-29, ERP-0002, baseline `c35b46803ec7bf0cec2dd9e29a0ee402d3677f98`

**Inspected:** .NET `ApplicationDbContext`, `ApplicationUser`, `Company`, initial EF migration/snapshot; Django `User`, `Role`, `AccessPermission`, `Company`, their migrations and MSSQL settings.

| Finding | Status | Evidence | Required next action |
|---|---|---|---|
| DB-001: non-unique ASP.NET email index | Open; prioritize before User Master sign-off | EF initial migration has `EmailIndex` without uniqueness; `RequireUniqueEmail` is application-side. Django email field is unique. | Check existing duplicates/collation; design filtered normalized-email UNIQUE EF migration; run concurrency and upgrade tests before applying. |
| DB-002: framework claim PKs use INT IDENTITY | Open design decision | `AspNetUserClaims.Id` and `AspNetRoleClaims.Id` are numeric INT IDENTITY; user/role/company business PKs use BIGINT. | Confirm BIGINT policy applies to Identity framework support tables; if yes, design data-preserving migration with FK/index review. |
| DB-003: financial/stock schema not yet present | Planned prerequisite | Inspected repo migrations contain only identity/company tables. | Before posting modules, approve decimal precision, costing method, FK graph, sequence uniqueness, serial constraints and transaction/ledger rollback rules. |
| DB-004: ASP.NET/Django auth schemas differ | Tracked | ASP.NET uses Identity<long>; Django uses Django auth/custom models. | Preserve ERP business/API parity; framework table names need not be identical. |

**Confirmed in source:** core Company/User/Role IDs are numeric auto-increment; Company bilingual fields and tax/registration indexes exist. **Not verified:** SQL Server migrations execution, existing database contents, DB performance/concurrency, and deployed table correctness.

**Changes in this review:** documentation only. No schema or migration modified because data-safe migration tests and existing data checks are unavailable; the open findings must be revisited at their owning implementation gates.
