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

## Review 013 — 2026-09-30, ERP-0014 BLOCKED

Server-side permission/audit gate cannot pass: ASP.NET Company uses authentication-only authorization and Django CompanyViewSet uses IsAuthenticated only. Django Role/AccessPermission foundations exist, but endpoint enforcement, branch scope and immutable audit persistence/parity are absent. No schema change is made because an isolated Package-01 permission/audit table would conflict with the later shared authorization architecture. Numeric IDs/Unicode unchanged; DB-001–DB-006 remain open. No runtime denial/audit test was executed, so AT-12 remains pending.

## Review 014 — 2026-10-04, ERP-0014 sequencing correction

Dependency review confirmed WP01 owns no runtime permission/audit schema. No early permission, branch or audit table/migration is created to satisfy generic wording.

- DB-001–DB-006 remain open.
- Numeric ID, Unicode, FK/index, money and stock/ledger policies remain unchanged.
- Authorization/branch persistence belongs to WP06–WP09; audit hardening/persistence is finalized in WP46.
- WP23's forward dependency on WP30 was corrected at plan level; warranty sale/invoice linkage remains a later integration, not an early schema fiction.
- No SQL migration, runtime denial test, E2E test or production data operation was performed.

**Schema changed:** no. **Production data touched:** no.


## Review 015 — 2026-10-04, plan residual dependency consistency

No database schema change. Rechecked WP21–WP23 sequencing against future Product/Stock/Sales/Warranty ownership.

- WP21 remains the append-only stock ledger owner; its negative acceptance is now ledger-native and no longer depends on future Sales.
- WP22 serial schema may own unique serial identity, stock location and reservation before Sales; sale/return foreign-key integration is explicitly staged to WP30/WP34.
- WP23 warranty schema may own policy/date/status/serial-ready data before Sales; sold-customer/source-invoice activation is staged to WP30 and final E2E to WP49.
- DB-001–DB-006 remain open. No migration, FK, index, production data, build, SQL or E2E test was run in this plan-text correction.


## Review 016 — 2026-10-04, ERP-0015 React ownership review

ERP-0015 owns no database entity or migration. Reviewed current React API usage against existing Company/Auth schema and previous DB findings.

- No schema/FK/index/ID/DECIMAL change.
- DB-001–DB-006 remain open.
- DB-006 is relevant to current Company UI because React loads the full Company collection and filters locally; the actual pagination/schema/query fix remains WP10/WP48.
- No SQL migration, DB read/write, build, browser E2E or production operation was executed.

## Review 016 — 2026-10-07, ERP-0016

**Inspected:** current Company React form/styles/API shape, ASP.NET Company model/initial SQL Server migration, Django Company model/serializer, SRS bilingual requirements and dependency ownership audit.

- **IDs/FKs/indexes:** no schema change. Company remains numeric BIGINT IDENTITY/BigAutoField; existing indexes/relationships unchanged. DB-001/DB-002 remain open.
- **Unicode/Arabic:** ASP.NET migration uses NVARCHAR for Company bilingual fields; Django/React carry separate English/Arabic values and React Arabic inputs use RTL direction. Live SQL Server Arabic round-trip was not executed, so runtime Unicode acceptance remains pending.
- **Money/date:** WP01 owns no monetary/date runtime surface. DECIMAL/rounding remains DB-003 for financial owners; KWD/date localization is a downstream WP11/transaction integration test, not a reason to add placeholder columns/formatters here.
- **Parity/transactions:** no transaction, stock/ledger or concurrency behavior changed. DB-004–DB-006 remain open. No audit persistence is introduced; WP46 remains the audit/security owner.
- **Responsive/accessibility:** source CSS has a <=900px responsive layout and horizontal table overflow. Browser/device/keyboard/accessibility tests were not executed.
- **Safety:** no migration, production SQL or data mutation.

**Outcome:** ERP-0016 can complete as a dependency-aware source verification/acceptance-contract gate; WP11 owns full localization/RTL, WP44 printing, WP49 final E2E.

## Review 017 — 2026-10-07, ERP-0017

**Inspected:** ASP.NET repository/test inventory plus CompanyRequest/LoginRequest validation contracts. No `aspnet-core/tests` project exists at current HEAD.

- No DB schema change belongs to WP01 test traceability; numeric BIGINT IDs, existing FK/index/delete behavior and NVARCHAR Company fields remain unchanged.
- DB-001/DB-002 remain open. DB-003 financial DECIMAL/stock transaction/reconciliation/concurrency work remains future-owned. DB-004–DB-006 remain open.
- Arabic SQL round-trip, logo failure atomicity, pagination, authorization and audit runtime tests are explicitly retained for their owning packages.
- WP03 owns reusable dev/test infrastructure. No one-off WP01 test harness or test-only schema is introduced.
- No `dotnet test`, SQL migration or runtime DB test was executed; none is claimed passed. Production data untouched.

**Outcome:** ERP-0017 satisfies its dependency-aware test-specification gate; executable ASP.NET tests remain pending the WP03 harness and relevant feature owners.


## Review 018 — 2026-10-23, ERP-0018

Inspected Django `Role`/`User` models and migrations, ASP.NET Core Identity<long>/RoleManager, Company write authorization, and both existing Company schemas. Roles use numeric BigAutoField/BIGINT IDENTITY. The new Django `accounts.0002_admin_role` data migration inserts the reserved Admin role only if absent; no table/column/FK/index schema change. ASP.NET IdentitySeeder now creates/assigns the Admin role for the configured administrator. Role delete is blocked while assigned to users. Company writes now require an administrator on both backends; reads still require login.

GitHub Actions run 39905510876: Django 22/22 unit tests PASS on isolated SQLite; ASP.NET Core Release build PASS (0 warnings, 0 errors); React production build PASS. Real SQL Server migration, Unicode round trip, database concurrency, backend parity and browser E2E are **not run**, owned by ERP-0019/WP02/WP49. DB-001 through DB-006 remain subject to their existing owner work packages. No production database or secrets touched.


## Review 019 — 2026-10-23, ERP-0019–ERP-0020 (WP01)

GitHub Actions [39911998441](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39911998441) verified Django SQLite and SQL Server tests, SQL Server schema/Unicode concurrency, ASP.NET Core EF migration/auth/Role/Company CRUD, Playwright on both APIs, .NET document-sequence unit tests, and Python/.NET migration rollback checks. Current core keys use BIGINT. No production database was touched. Remaining DB-001–DB-006 remain tracked by their owner packages; full SRS business acceptance still depends on later modules.

## Review 020 — 2026-10-23, ERP-0021–ERP-0040 (WP02)

Added `core_documentsequence` and `DocumentSequences` tables (Django and ASP.NET independently) with numeric BIGINT IDENTITY/BigAutoField, series NVARCHAR/varchar equivalent (20 chars), fiscal year integer, branch scope BIGINT (0 reserved for default single-site), last number BIGINT. Unique constraint/index on (series, fiscalYear, branchId), with SQL Server `sp_getapplock` transaction-based allocator, prevents duplicate sequence numbers under concurrent allocations. Django 5-thread, ASP.NET 6-request concurrency tests passed. EF and Django down/up tested on disposable SQL Server, no existing business data. Branch FK, final formatted prefix/number policy and in-document transaction binding deferred DEC-05 and WP09/WP24–34. Company Arabic Unicode tested in both backends. Financial DECIMAL and stock/ledger integrity remain future-owned DB-003.

## Review 021 — 2026-10-23, ERP-0041–ERP-0050 (WP03)

Environment/CI steps add **no WP03 schema or migration**. Tested existing Django/EF migrations, rollback/reapply of WP02 sequence tables, schema drift checks (`makemigrations --check`, EF `has-pending-model-changes`). SQL Server integration uses generated CI-only SA/admin credentials and disposable databases, not production. Missing environment config negative tests execute. Numeric IDs, FK/index design and Unicode remain unchanged. DB-001–DB-006 remain pending appropriate downstream owner decisions and live-data-safe migrations.


## Review 022 — 2026-10-23, ERP-0001–ERP-0060 recheck (WP03 final gate)

Verified current Django models/migrations and ASP.NET EF snapshots: Role/User/Company/DocumentSequence business PKs remain BIGINT autoincrement; sequence composite unique series/fiscal-year/branch index exists on both SQL Server schemas. SQL Server CI run [39915764939](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39915764939): Django SQL 33/33 PASS; .NET xUnit 4/4 PASS including enclosing transaction rollback; both backends' migrations/sequence down-up rehearse cleanly. Current shared UI Arabic Company round-trip and Role CRUD verified on both backends (Playwright Django 4/4, ASP 3/3). Read/validate changed source for white-space Company/Role required field rejection; errors normalized without framework exception dumps. Developer environment missing-secret/DB errors are verified. No production DB touched.

**Open** DB-001 unique normalized email, DB-002 Identity claim INT IDs, DB-003 future financial/stock DECIMAL and FK/transaction schema, DB-004 framework auth schema/API semantics, DB-005 logo/database atomicity, DB-006 Company pagination. Production SQL Server 2019 validation, multi-branch FK/tenant scope, invoice posting atomicity, audit/stock and currency/RTL acceptance remain future-owned. WP03 requires no further schema migration.


## Review 023 — 2026-10-23, ERP-0061–ERP-0100

Verified source `88b05638831778d48b21ee8f83a95a2e40bf4419` and [CI run 39920485489](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39920485489): Django 47/47 disposable SQL Server tests, ASP.NET xUnit 4/4, API+CSRF+lockout SQL smoke, Django Playwright 9/9 and ASP.NET Playwright 8/8; frontend and .NET Release builds PASS. Company/User/Role/DocumentSequence ERP PKs remain BIGINT auto-increment; unique ASP normalized-email filtered index now checks duplicates and refuses unsafe migration; Django login lockout migration adds failed counter and expiry, no UUID PK. FK orphan relations rejected and Arabic values round-trip. Explicit JS safe-integer rejection prevents silent numeric JSON ID rounding. No transaction-money schema exists in this package: KWD DECIMAL precision, posting/stock/ledger FK design and printed financial documents remain business owner packages. Framework-owned Identity claim IDs remain INT and require a separate compatibility decision. Source environments target SQL Server 2019 but CI runs SQL Server 2022; **production compatibility not claimed**. No production database or data touched.


## Review 023 — 2026-10-23, WP06–WP10 (ERP-0101–ERP-0200)

Verified [CI run 39979943571](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39979943571) after Permission/User/Branch/Company changes. **5/5 jobs PASS**: Django 60 SQL tests, ASP.NET 4 xUnit, Django browser 13, ASP browser 11, migrations on disposable SQL Server. New permission catalog is Django AccessPermission seeded by migration `accounts.0004` and ASP.NET built-in Identity role claim storage, with no duplicate permissions table. User adds Django mobile (`accounts.0005`) and branch FK (`accounts.0006`) and ASP IsActive/branch FK migrations. Branch and Warehouse use BIGINT IDENTITY/BigAutoField, CompanyId and BranchId restrictive FKs and scoped unique (CompanyId,Code)/(BranchId,Code); proper delete-denial tested. Company remains bilingual NVARCHAR/Unicode, has an optional logo path without an extra DB column; logo storage relies on randomized file names, SQL transactions and best-effort file cleanup. Invalid MIME, oversize and bad signatures rejected in current tests. No production schema or data touched.

Outstanding constraints: no real stock/finance transaction branch enforcement until those entities are built; .NET logo format header verification is not equivalent to full image decoder validation; deeper image checks and production 2019 compatibility remain to be qualified. No new financial DECIMAL or ledger tables are introduced by these packages.

## Review 024 — 2026-10-23, ERP-0201 WP11 SRS extraction

Reviewed original SRS §§3, 4, 40, 41, 62, 65 against existing Django/ASP.NET/React bilingual master contracts. Requirement-extraction step ERP-0201 introduces **no new table, index or migration**. Existing Company/Customer/Supplier/Category/Brand fields retain independent Unicode strings and numeric BIGINT primary keys; monetary fields remain DECIMAL(18,3), not formatted Javascript posting amounts. [CI run 40001241106](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40001241106) was 5/5 PASS on disposable CI SQL Server and browser suites after partner-email validation fix. New partner fields use additive Django and EF migrations; no production DB was touched. Future quotation, invoice, statement and paper-size print acceptance remains owned by WP27/WP30/WP44 and cannot be verified at this step.

## Review 025 — 2026-10-24, ERP-0202 localization source inspection

Reviewed commit `b8d966147840c4e4a92ea3f5ec3b9f88dcc71b51` and [CI run 40002127807](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40002127807) (5/5 PASS; disposable SQL Server Django 72/72, ASP.NET SQL xUnit 4/4, Django 16 and ASP.NET 14 Playwright). Company, Customer, Supplier, Category, Brand and Product have separate Unicode EN/AR fields in Django and .NET; numeric BIGINT identity remains, SQL Server NVARCHAR fields and decimal(18,3) partner amounts persist from existing migrations. WP11 language-switch rendering is React-only: no new table, index or data migration is necessary for ERP-0202. Source inspection found no basis for changing production DB. Follow-on ERP-0203 must record untranslated DRF field errors and remaining mixed-direction/accessibility gaps. Quotation/invoice/report printing, receipt layout and physical A4/A5/thermal tests remain WP27/WP30/WP44, not a claim from Company identity preview.

## Review 026 — 2026-10-24, ERP-0203 SRS/source gap comparison

Inspected code vs SRS §§3,4,40,41,62,65 using the ERP-0202 inventory. WP11 locale switching is client-side only: no DB table, numeric-ID change, index or migration is warranted. Source parity discrepancy recorded for WP12–WP13: Django PartnerSerializer code validator allows non-ASCII alphabetic Unicode, while ASP.NET PartnerValidation regular expression restricts codes to `[A-Z0-9_-]`; this is a **code field rule**, not a restriction on Arabic display names or their Unicode storage. Company/Partner/Catalog bilingual strings remain on separate NVARCHAR/Unicode columns; partner monetary values remain SQL DECIMAL(18,3). Untranslated field-level API errors are presentation/contract gaps, not schema changes. Existing 5/5 green CI [40002127807](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40002127807) has real disposable SQL Server coverage but not full Arabic quotation/thermal printing. No migrations, production DB operations, new authorizations or stock/ledger postings were made here.

## Review 027 — 2026-10-24, ERP-0204 happy-path contract

ERP-0204 specified language switching, Unicode save/reload and Arabic quotation rendering acceptance from the existing WP11 source evidence. No quotation, invoice or printing database model exists in WP11. Existing Company/Partner/Catalog primary keys remain numeric BIGINT identity/BigAutoField; EN/AR columns remain Unicode, partner amounts remain DECIMAL(18,3), action permissions are locale-neutral. Existing migrations, FK/indexes and DB-001–DB-006 owners are unchanged. No new schema, migration, production DB operation, finance calculation or physical print test was performed. RTL quotation output remains an executable gate at WP27/WP44, not a WP11 implementation claim. New frontend error handling changes HTTP-400 UI feedback only and cannot change persisted monetary values.

## Review 028 — 2026-10-24, ERP-0205 mixed-direction negative-case specification

Source review of React Company/Partner/Catalog forms found English identifiers and numeric inputs inherited RTL from the root when Arabic UI was selected, despite Arabic-name inputs having an explicit RTL direction. Narrow field-level LTR attributes were added to English fields, codes, emails, tax references and decimal amounts; no database schema, SQL API, PK/FK/index, decimal precision or authorization path changed. Numeric BIGINT IDs and existing Unicode EN/AR persistence remain unchanged. No migration, rollback or production query was run. RTL layout/browser checks in the new Playwright test require CI evidence before the implementation change can be called verified. Future invoice-print directionality remains WP27/WP44.

## Review 029 — 2026-10-24, ERP-0206 localization/config schema decision

Inspected Company, Customer, Supplier, Category, Brand and Product Django models and their ASP.NET counterparts, plus `frontend/src/i18n.tsx` and locale formatting. The persisted bilingual data has separate Unicode English/Arabic columns and existing numeric BIGINT identities; existing partner monetary columns are decimal(18,3). Language selection is browser state, not a new database entity. No WP11 schema migration or additional index/FK is warranted. DB-001–DB-006 remain with their recorded owners; no production database touched, no SQL runtime test/rollback performed (design-only task). Future quotation/document printing designs remain WP27/WP30/WP44, where migrations and printable template configuration must be designed against real entities.

## Review 030 — 2026-10-24 ERP-0207

Existing models retain BIGINT auto-increment IDs, separate SQL Unicode EN/AR fields, DECIMAL(18,3) partner money, unchanged FK/index constraints and authorization. No new WP11 persistence, schema update, migration, SQL data write or physical printer test. Arabic diacritics and mixed-script round-trip regression authored (commit 80cd7c1); awaiting CI verification. UI rollback requires deployment rollback only, leaving stored Arabic rows unchanged. DB-001–DB-006 remain with existing owners.

## ERP-0208 — Database source review

ASP.NET CompanyRequest/PartnerRequest and Company/Customer/Supplier entities already carry separate EN/AR bounded strings. SQL Server uses nvarchar; long BIGINT identity unchanged. Existing controller validation returns language-neutral detail, and React now translates it. No WP11 ASP.NET schema or contract repair needed. Financial print contracts belong WP27/WP30/WP44. No new migration, FK/index, monetary precision or ID change. Existing BIGINT and DECIMAL rules retained, DB-001–DB-006 previously tracked. No production SQL data read or modified.

## ERP-0209 — Database source review

Django CompanySerializer, PartnerSerializer and catalog NamedSerializer expose independent source-mapped English/Arabic fields with appropriate lengths. DRF emits field-error objects on 400; shared React now maps unmatched errors to localized safe invalidRequest. No locale-specific serializer or database table should be added. Product quotation/print flows belong later modules. No new migration, FK/index, monetary precision or ID change. Existing BIGINT and DECIMAL rules retained, DB-001–DB-006 previously tracked. No production SQL data read or modified.

## Review 031 — ERP-0210 migration decision

No new schema for React translations, document lang/dir or localized presentation. Existing Django/EF Company/Partner/Catalog Unicode columns, BIGINT identity, DECIMAL(18,3), indexes and FKs remain. No migration, live SQL, rollback or data modifications executed. DB-001–DB-006 retained.

## Review 032 — ERP-0211 shared API contract

API language is independent of stored schema and PK. ASP.NET/Django expose existing bilingual Unicode fields, BIGINT identity and DECIMAL(18,3) partner amounts through existing /api routes. No DB model or migration changed. DRF 400 field error shape differs from ASP.NET but frontend safely localizes the visible fallback. There is no locale column, cross-tenant query or financial posting introduced. No production DB touched.

## ERP-0212 — Database ownership review

CompaniesApiController CRUD persists EN/AR values without server locale conversion; Customers/Suppliers APIs retain binary permission codes and numeric IDs. No WP11 business transaction or locale-specific idempotency token is needed. Financial quotation/printing transactions and retry safety remain WP27/WP30/WP44. Existing BIGINT, EN/AR NVARCHAR and monetary DECIMAL precision remain. No migration/schema/index changes or production SQL operations.

## ERP-0213 — Database ownership review

CompanySerializer already wraps logo save and DB mutation in atomic transaction; PartnerSerializer and Catalog serializers store bilingual values directly. Choosing Arabic never creates a separate server transaction, document or sequence. Cross-backend retry semantics for future quotations belong WP27; existing serializers require no additional WP11 operation. Existing BIGINT, EN/AR NVARCHAR and monetary DECIMAL precision remain. No migration/schema/index changes or production SQL operations.

## ERP-0214 — Database review

Current ASP.NET Company writes require named company policies and Django Partner/Catalog views require server-side action permissions. `frontend/src/locale.ts` translates only labels; permission codes remain invariant under EN/AR and root document dir. Current backend branch/warehouses are protected through existing policies; full business-document branch scoping and audit trail remain WP09/WP46 and future transaction owners. No locale-specific audit table, permission bypass or new security layer is justified. Tests for actual financial document rights are deferred; no unauthorized access is claimed verified here. BIGINT keys/Unicode/DECIMAL precision unchanged; no migration or production query.

## ERP-0215 — Database review

React-only presentation/error changes. Existing numeric BIGINT IDs, Unicode and financial DECIMAL unchanged. Full CI 40050867366 passed in disposable environment, not production DB.

## ERP-0216 — DB review

5/5 CI 40051364388 confirms existing disposable SQL Server integration and browser regression following RTL UI changes. Current numeric BIGINT identity, Unicode columns, decimal(18,3) and related FK/index structures unchanged. No production data or migration changed; physical Arabic print remains downstream.

## Review ERP-0217–0220 — WP11 localization closeout

At `dd5ad231`, [CI 40051691145](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40051691145) passed 5/5 on disposable SQL Server and browser E2E. No new localization tables/migrations. Existing Company/Partner/Catalog `NVARCHAR` and Django bilingual fields preserve Unicode; PKs are BIGINT, money is decimal(18,3), permissions are language-neutral. Currency display uses Intl only; financial posting and physical print layout are future-owned. Production databases untouched.

## ERP-0221 — Customer DB review

SRS §§4,8,9,51,52,57 require Customer code, English/Arabic names/address, mobile, civil ID access controls, type, payment terms, opening balance, credit limit, searchable master and confidential attachments. Actual ledger/receivables belong WP32–WP33/WP43; posted invoice rules not owned by WP12. Current SRS baseline AT-02 spans quotation/print owners and cannot pass in WP12.

Existing Customer and PartnerDocument use auto-increment BIGINT, nvarchar/Unicode, CreditLimit/OpeningBalance decimal(18,3), unique code, exclusive owner CHECK, restricted FKs. No migration/production SQL changes in this step.

## ERP-0222 — Customer DB review

ASP.NET Customer long PK, normalized ASCII code, nullable optional email, BIGINT FK-protected binary documents, server-side civilId omission for non-admin; Django CustomerSerializer mirrors bilingual fields, validates mandatory Arabic name/mobile, protects files; React Partners form handles bilingual CRUD/search, optional email, 3-place decimal strings, admin document upload/download. Existing full CI 40056434243 PASSED 5/5; file presence alone does not pass AT-02.

Existing Customer and PartnerDocument use auto-increment BIGINT, nvarchar/Unicode, CreditLimit/OpeningBalance decimal(18,3), unique code, exclusive owner CHECK, restricted FKs. No migration/production SQL changes in this step.

## ERP-0223 — Customer data integrity review

Source shows bilingual Customer API and form, normalized unique code, required Arabic name/mobile, CivilId read omission for nonadmins, documents admin-only and download protection. Remaining scope: full customer statement/receivable posting is WP32–WP33/WP43, quotation and printable output WP28/WP44; no API for these should be invented now. Current customer browsing is in-memory filtering, pagination owner WP48, full file threat scanning is downstream security WP46.

Existing BIGINT IDENTITY/BigAutoField, NVARCHAR, DECIMAL(18,3) unique code and exclusive customer/supplier document ownership remain. No new migration or production DB operation.

## ERP-0224 — Customer data integrity review

Create authenticated admin Customer with code C-RTL-001, NameEn Retail, NameAr متجر الكويت, Arabic address, mobile, CreditLimit 2500.750, OpeningBalance 15.250, paymentTermsDays 30, type credit. Expect 201 numeric BIGINT ID, case-normalized code, exact Unicode and decimal string round-trip in GET/list/edit and shared React. New source must not alter monetary figures on UI locale switch. Ledger/quotation cannot be certified before business owners.

Existing BIGINT IDENTITY/BigAutoField, NVARCHAR, DECIMAL(18,3) unique code and exclusive customer/supplier document ownership remain. No new migration or production DB operation.

## ERP-0225 — Customer database review

Reject duplicate case-insensitive code and simultaneous duplicates with HTTP 400; reject blank Arabic name/mobile, invalid credit/decimal/email without saved mutation; deny employee CivilId details, admin-only file upload/list/download and cross-owner document access; reject MIME/extension mismatch; existing protected documents block delete with 409 and private downloads return no-store/nosniff. File scanning and attachment retention policy are WP46.

Existing DECIMAL(18,3), indexed code, BIGINT identities, restricted foreign keys and one-owner check unchanged. No schema migration executed.

## ERP-0226 — Customer database review

Customer/PartnerDocument already use BIGINT IDENTITY/BigAutoField, unique normalized ASCII code, separately stored EN/AR Unicode name/address, positive decimal(18,3) credit and opening balance. PartnerDocument is binary + MIME + 200-char name with exclusive owner CHECK and restrictive FKs. Existing EF Partners/PartnerDetails and Django partners 0001/0002 migration cover all WP12 owned fields; do not add redundant columns or UUIDs. No live data migration warranted at this design step.

Existing DECIMAL(18,3), indexed code, BIGINT identities, restricted foreign keys and one-owner check unchanged. No schema migration executed.

## ERP-0227 Customer DB constraints and rollback

Customer code must normalize to ASCII uppercase, use a DB unique index plus clean 400 on duplicate/concurrent writes; names and Arabic address must preserve Unicode; mandatory NameEn/NameAr/Mobile, 0–365 payment term days, nonnegative DECIMAL(18,3) amounts, no HTML/locale parsing of money. Customer inactive state must remain explicit; no silent deletion if PartnerDocument rows exist. FK PROTECT + check constraint prevent cross-owner or orphan attachment. Downgrade PartnerDetails migration is potentially destructive on existing data, so do not run on production; on disposable SQL CI test migrations and rollback rehearsal, with pre-upgrade backup required for real deployment. No new DDL for step.

## ERP-0228 — Customer database/API review

Existing Customer long ID, bounded EN/AR strings, mandatory NameAr/Mobile server validation, ASCII uppercase code, decimal(18,3), optional email. CustomersApiController policy-gated CRUD catches concurrent unique errors and restricts CivilId/documents to admins; file checks and private no-store/nosniff downloads in place. No extra model or API is necessary.

Existing BIGINT PK, code unique index, EN/AR NVARCHAR, DECIMAL(18,3) and exclusive document FKs unchanged. No new DDL or production SQL.

## ERP-0229 — Customer database/API review

CustomerSerializer mandates Arabic name/mobile and normalized unique code, preserves three-decimal money and suppresses CivilId for non-admin. PartnerViewSet handles database unique failures inside transaction.atomic, enforces admin-only documents and validates extension/MIME/signature. Download response has no-store/nosniff. No WP12 Django schema additions needed.

Existing BIGINT PK, code unique index, EN/AR NVARCHAR, DECIMAL(18,3) and exclusive document FKs unchanged. No new DDL or production SQL.
