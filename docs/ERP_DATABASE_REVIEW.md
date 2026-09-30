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

## Review 002 — 2026-09-30, ERP-0003, baseline `e2755b3f2c9316e10ddf8b150c67c75ff8c66124`

**Scope and source:** SRS-to-code comparison of all 68 source headings; re-read EF Company/Identity models and initial migration, Django Company/Account models and migrations, Company API/serializer and file writers, ASP.NET startup, DRF URL routing, React root/API client and the complete non-truncated repository tree. Documentation-only step; no SQL connection or migration executed.

| Finding | Status and evidence | Safe remediation owner |
|---|---|---|
| DB-001 — normalized email index is non-unique | Still open; EF initial migration creates `EmailIndex` without `unique: true` while Django custom User email is unique. | WP04/WP08: inspect production duplicates/collation; safe filtered unique migration and concurrency tests. |
| DB-002 — Identity claims use INT IDs | Still an open policy decision; EF `AspNetUserClaims.Id` and `AspNetRoleClaims.Id` are INT IDENTITY, though ERP business IDs and User/Role PKs are BIGINT. | WP04: confirm policy for framework support tables before migration. |
| DB-003 — no financial/stock schema | Open prerequisite; only Identity/Company tables exist in the EF and Django application migrations. | WP18/WP21–WP37: define DECIMAL precision, FK graph, constraints, serial/document uniqueness, costing and atomic rollback before posting. |
| DB-004 — auth framework schemas differ | Tracked, not inherently a defect; ASP.NET Identity and Django auth are different frameworks. | WP02/WP05–WP08: require identical business/API behavior rather than identical internal table names. |
| DB-005 — Company logo file overwrite precedes durable DB update | Confirmed code defect risk: ASP.NET `CompanyLogoStorage.SaveAsync` opens `company-{id}{ext}` with `FileMode.Create` before saving the new path; Django `CompanySerializer._save_logo` deletes existing file first. Failed DB save can lose original media and create/update may leave orphan record/file. | WP10: unique staged path, safe promotion/reference, on-commit cleanup, failure injection and regression tests before schema/file changes. |
| DB-006 — Company API query lacks explicit pagination | Confirmed source-level scalability gap: EF Companies list uses unbounded `ToListAsync`; DRF `CompanyViewSet` uses a queryset without explicit page policy. | WP10/WP48: matching paginated contract, stable indexed ordering and React paging; validate large dataset. |

**Schema cross-check:** current ERP user/role/company PKs remain numeric BIGINT/BigAutoField; EF Company bilingual columns are NVARCHAR; Django Company fields and migration exist. Existing Company tax and registration indexes exist but business uniqueness rules need approval. **Not verified:** live DB collation/duplicates, EF/DRF migration execution, schema diff on deployed DB, decimal calculations, stock/ledger transaction safety and SQL Server concurrency.

**Change decision:** ERP-0003 creates requirements/bug traceability and updates this review. No production schema alteration, migration, payment, or file overwrite is performed without a safe test DB and failure/regression tests. Fixes are assigned to their implementation packages; this mapping step does not assert those defects are resolved.

## Review 003 — 2026-09-30, ERP-0004, reviewed HEAD `1f980fef746512c950098cc2a2378cfbd11a5ac0`

**Inspection:** Re-read ASP.NET `Company.cs` and initial EF `20260918070000_InitialCreate.cs`; Django `companies/models.py` and `companies/migrations/0001_initial.py`. Reviewed [ERP-0004 happy-path acceptance](ERP_0004_ACCEPTANCE.md) and previous database findings.

- **IDs and Unicode:** `Companies.Id` remains `BIGINT IDENTITY` in ASP.NET and `BigAutoField` in Django; .NET `NameEn/NameAr` use `NVARCHAR(200)`. English/Arabic round-trip is specified in `HP-01` but not yet tested against a live SQL Server database.
- **Relationships and indexes:** Existing Company tax/registration indexes and Identity foreign keys were previously checked; `DB-001` (unique email), `DB-002` (Identity claim IDs) and `DB-004` (framework schema differences) remain open or decision-gated. No new FK is required for this documentation-only step.
- **Stock/finance:** `DB-003` remains open: stock/payable ledger tables do not exist, and DECIMAL precision, referential constraints and atomic posting must be reviewed before implementing purchase/sale.
- **Company file consistency:** `DB-005` is still open; `HP-01` explicitly excludes a logo to avoid claiming file/DB atomicity. `DB-006` unpaginated Company lists remain a separate performance acceptance gate.
- **Migration safety:** No models, SQL schema or migration changed here. SQL Server connection, migration forward/rollback and runtime concurrency tests **not run**; production data was not touched.

**Outcome:** Existing DB-001–DB-006 retained and test owners preserved. No schema fix is falsely reported complete.

## Review 004 — 2026-09-30, ERP-0005

Inspected Company authorization in ASP.NET and Django plus the existing requirement-gap matrix. This step changes no database schema.

- Company/User/Role application IDs remain numeric; no UUID/public ID was added.
- Company mutation endpoints currently require authentication but do not enforce ERP action permissions. ERP-0005 specifies the required authenticated 403 denial and no-data-change check; implementation and runtime proof remain pending.
- DB-001 through DB-006 remain open. No live SQL Server migration, concurrency, rollback, stock, ledger or production-data operation was performed.

**Outcome:** database design unchanged; action-level permission enforcement and audit remain prerequisites before AT-12 can pass.
