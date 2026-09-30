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

## Review 005 — 2026-09-30, ERP-0006

**Inspected:** EF `ApplicationDbContext` and initial SQL Server migration; Django core/accounts/Company models; current Package 01 tracker/configuration documents.

- **Design decision:** requirement map, scope decisions and AT-01–AT-13 are version-controlled engineering metadata, not runtime ERP records. No EF/Django entity or SQL Server migration is warranted; `docs/ERP_0006_DATA_DESIGN.md` is the canonical design evidence.
- **IDs:** persisted ERP application IDs remain numeric auto-increment. ASP.NET Company/User/Role keys are BIGINT/long and Django business migrations use BigAutoField. No UUID/GUID/public ID added. Framework claim INT IDs remain DB-002 rather than being changed unsafely here.
- **Integrity/parity:** no new FK, unique constraint or index is required because no runtime table is introduced. DB-001 and DB-004 remain open. Existing Company indexes are unchanged.
- **Unicode/money/transactions:** no new text or monetary columns. DB-003 remains open; stock/financial DECIMAL precision, posting atomicity, reconciliation and immutable audit are not implemented or signed off.
- **Safety:** no migration, production SQL, data overwrite or destructive operation. DB-005/DB-006 remain open Company defects owned by later implementation gates.

**Runtime limitation:** SQL Server migration/readback, application builds and E2E were not run because ERP-0006 is a documentation-only N/A schema design decision; none are reported as passing.

## Review 006 — 2026-09-30, ERP-0007

**Inspected:** Company EF model/configuration, current SQL Server migration, Django Company model and React Company form, plus Package 01 traceability configuration.

- **Constraints/status:** ERP-0007 introduces no runtime table. Traceability constraints and allowed statuses are defined in `ERP_0007_CONSTRAINTS.md`; DB constraints are therefore N/A for this metadata step.
- **IDs/FKs/indexes:** persisted ERP IDs remain numeric BIGINT/BigAutoField. No FK/index/unique change. Existing Company tax/registration indexes remain non-unique; uniqueness is not invented without business approval. DB-001/DB-002 remain open.
- **Unicode:** ASP.NET Company migration uses NVARCHAR for bilingual text and React Arabic inputs are RTL; Django strings are Unicode-capable. No live SQL Server Arabic round-trip was executed, so runtime Unicode acceptance remains unverified.
- **Decimals/transactions/audit:** no Package-01 money/stock field exists. DB-003 remains open; future posted money requires explicit fixed precision and atomic posting. No stock/ledger/audit-integrity pass is asserted.
- **Parity/rollback:** DB-004–DB-006 remain open. No migration was created; rollback for this step is a forward documentation correction through Git history, not a destructive DB operation.

**Tests actually run:** source/document inspection only. Application build, SQL migration, concurrency and E2E not run and not required to establish this no-schema constraint definition.

## Review 007 — 2026-09-30, ERP-0008

**Inspected:** ASP.NET ApplicationUser, Company, ApplicationDbContext, LoginRequest, CompanyRequest/Response, auth/company controllers and project dependencies.

- **Schema decision:** Package-01 traceability remains Git-versioned metadata per ERP-0006; no EF entity/API contract/table is appropriate. ERP-0008 records N/A instead of introducing duplicate runtime state.
- **IDs/relationships:** reviewed ASP.NET User/Role/Company application keys use long/BIGINT policy. No new relationship. DB-002 framework claim INT IDs remain unchanged and explicitly open.
- **Constraints/indexes:** existing Company tax/registration indexes unchanged. DB-001 normalized-email uniqueness remains open; no identity migration attempted without duplicate/collation checks.
- **Unicode/decimal:** Company bilingual schema remains Unicode-capable by existing NVARCHAR migration. No money field added; DB-003 remains open.
- **Atomicity/audit/parity:** no stock/financial operation introduced. DB-004–DB-006 and granular authorization/audit gaps remain open and are not fixed by this inventory-contract step.
- **Migration safety:** no schema/migration/data change; production untouched.

**Tests actually run:** source/configuration inspection only. No dotnet build/test, SQL migration or E2E was executed; this step does not claim existing runtime features newly pass.

## Review 008 — 2026-09-30, ERP-0009

**Inspected:** Django settings, core/accounts/companies models and migrations, accounts API, Company serializer/viewset and API routing.

- **Schema decision:** Package-01 traceability remains Git metadata. No Django traceability model/serializer/migration is appropriate; adding one would create backend and persistence-source divergence.
- **IDs/FKs:** DEFAULT_AUTO_FIELD is BigAutoField; reviewed User, Role, AccessPermission and Company migrations use BigAutoField. Role-permission/user-role M2M relationships exist. No UUID/GUID introduced.
- **Indexes/uniqueness:** AccessPermission.code, Role.name, User.username/email are unique in Django; Company tax/registration fields are indexed, not unique. ASP.NET Identity normalized-email difference remains DB-001/DB-004; no cross-backend uniqueness policy is invented here.
- **Unicode/decimal:** Django strings are Unicode-capable and Company has English/Arabic fields; live SQL Server Arabic round-trip not run. No money/stock field; DB-003 remains open.
- **Atomicity/audit:** Company serializer performs DB and logo-storage operations separately; DB-005 remains open. CompanyViewSet has IsAuthenticated only and no granular permission/audit proof. DB-006 unbounded listing remains open.
- **Safety:** no schema/migration/data change and no production operation.

**Tests actually run:** source/configuration inspection only. Django checks/tests, SQL migration/readback and E2E were not executed; no runtime pass is claimed.

## Review 009 — 2026-09-30, ERP-0010

**Inspected:** EF initial migration/snapshot and Django accounts/companies initial migrations.

- Package-01 traceability has no runtime table; no new SQL Server migration/index is warranted.
- ASP.NET Company/User/Role application PKs are BIGINT/long; Django User/Role/AccessPermission/Company use BigAutoField. Identity claim support IDs remain INT (DB-002).
- Company bilingual EF columns are NVARCHAR. Company tax/registration indexes exist in both implementations. No money/stock schema exists; DB-003 remains open.
- DB-001 remains material: ASP.NET NormalizedEmail index is non-unique while Django User.email is unique. No unique migration is created without existing-data/collation checks and regression tests.
- DB-004–DB-006 remain open. No stock/financial atomicity or audit-integrity pass is asserted.
- No live SQL Server migration, rollback, schema diff, duplicate scan or concurrency test was available/executed. Production data untouched.

## Review 010 — 2026-09-30, ERP-0011

Reviewed ASP.NET/Django auth and Company API contracts plus React API consumers. No Package-01 traceability runtime endpoint/schema exists or is needed. Numeric IDs and Unicode Company fields unchanged. DB-001–DB-006 remain open; notably validation payload parity is unverified, Company list remains unpaginated and logo persistence semantics remain non-atomic. No money/stock schema or transaction/audit pass. No migration/data change. Runtime API/E2E tests not run.

## Review 011 — 2026-09-30, ERP-0012

Reviewed ASP.NET auth/Company controllers and CompanyLogoStorage. Package-01 traceability has no runtime business operation or idempotency persistence; no schema change is appropriate. Numeric IDs/Unicode unchanged. DB-001–DB-006 remain open; DB-005 is reconfirmed because Company DB and filesystem logo writes are separate. No stock/financial transaction or audit pass. No build/test/migration/E2E executed.

## Review 012 — 2026-09-30, ERP-0013

Reviewed Django auth/Company operations and serializer media writes. Package-01 metadata has no runtime transaction/idempotency persistence. BigAutoField/Unicode design unchanged. DB-005 media/DB failure atomicity reconfirmed; DB-001–DB-006 remain open. No stock/financial/audit pass, migration, data change or runtime test.
