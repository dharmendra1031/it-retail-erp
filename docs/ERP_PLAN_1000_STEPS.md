# IT Retail ERP — 1000-step executable implementation plan

**SRS:** https://docs.google.com/document/d/1Gb_pMJAN14UY0scLJjGBGiuRZdlXOWJARB1aLkzIobc/edit?usp=sharing
**Repository:** `dharmendra1031/it-retail-erp`; **work branch:** `development`; **baseline reviewed:** `9e799d915008840d377d7c948d13da78486a9073` (2026-09-20).
**Architecture:** one React/TypeScript frontend, interchangeable ASP.NET Core (.NET 10) and Django REST backends, SQL Server; numeric auto-increment entity IDs.
**Scope:** 50 work packages × 20 individually gated steps = exactly 1000 steps; ten phases × 100 steps. This is a plan, not a claim that its code/tasks already pass.
**SRS numbering note:** source has no section 64 and uses section 65 twice (`MINIMUM ACCEPTANCE CRITERIA` and `IMPORTANT DEVELOPER NOTES`); preserve titles when tracing either.

## Mandatory step-completion rule

Read this plan and `docs/ERP_EXECUTION_PROTOCOL.md`, load `docs/ERP_PROGRESS.json`, inspect current `development` HEAD and referenced implementation. For the first incomplete step, verify actual source code before editing, fix deficiencies and bugs, run available relevant tests, record evidence and update the tracker in the same commit. Never skip a blocked step, falsely mark it complete, or advance because a file merely exists. Do not merge into `main` without explicit approval.

## Initial observed baseline (not execution sign-off)

- Source tree contains login/auth/CSRF endpoints and React login, Company Master CRUD/React form/table, SQL migrations, numerical .NET Identity IDs and Django BigAutoField models.
- Django Role and AccessPermission models exist, but equivalent exposed Role/User/Permission CRUD APIs and React screens were not found in the reviewed source tree.
- Supplier, customer, product, purchase, inventory, quotation, sales, service, reporting and backup functional modules are not implemented in the reviewed repository tree.
- Previous user terminal output shows ASP.NET restored and started on port 5000 before the latest `.env` change; latest dependencies/migration, Django, React and end-to-end tests are **not** independently verified.
- All 1000 steps remain pending until their own code/documentation evidence and applicable checks meet the gate. Inspect current code each hour; do not rely on this snapshot after new commits.

## Phases and individually tracked steps

## Phase 1: Requirements, architecture and build foundation

### Package 01: SRS baseline and delivery boundaries — ERP-0001 to ERP-0020
**SRS sections:** 1, 2, 55, 65, 66, 67, 68. **Deliverable:** Versioned requirement-to-implementation map, scope decisions and 13 acceptance cases.
**Dependencies:** packages None; first execution step. **Invariant:** Every requirement has owner, evidence and explicit in/out-of-scope disposition.
**Happy-path proof:** Trace one SRS requirement to its implementation and test. **Negative proof:** Flag a requirement with no owner or missing evidence.

- [x] **ERP-0001** (01/20) Extract SRS baseline and delivery boundaries acceptance details from SRS §§1, 2, 55, 65, 66, 67, 68; record assumptions and exclusions.
- [x] **ERP-0002** (02/20) Inspect ASP.NET feature/code inventory, Django feature/code inventory and React feature/screen inventory; record actual files and current behavior.
- [x] **ERP-0003** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [x] **ERP-0004** (04/20) Specify the happy-path acceptance: Trace one SRS requirement to its implementation and test.
- [x] **ERP-0005** (05/20) Specify the negative/authorization case: Flag a requirement with no owner or missing evidence.
- [x] **ERP-0006** (06/20) Design data, configuration and numeric BIGINT IDs for Versioned requirement-to-implementation map, scope decisions and 13 acceptance cases; record N/A with evidence if schema unchanged.
- [x] **ERP-0007** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Every requirement has owner, evidence and explicit in/out-of-scope disposition.
- [x] **ERP-0008** (08/20) Implement or repair ASP.NET entities/configuration/contracts for ASP.NET feature/code inventory.
- [ ] **ERP-0009** (09/20) Implement or repair Django models/serializers/configuration for Django feature/code inventory.
- [ ] **ERP-0010** (10/20) Create/review SQL Server migrations and indexes for SRS baseline and delivery boundaries; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0011** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Versioned requirement-to-implementation map, scope decisions and 13 acceptance cases.
- [ ] **ERP-0012** (12/20) Implement or repair ASP.NET business operations and idempotency for SRS baseline and delivery boundaries.
- [ ] **ERP-0013** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for SRS baseline and delivery boundaries.
- [ ] **ERP-0014** (14/20) Enforce role/branch/action permissions and record audit events for SRS baseline and delivery boundaries; prove server-side denial.
- [ ] **ERP-0015** (15/20) Implement or repair React API integration, screens and user feedback for React feature/screen inventory.
- [ ] **ERP-0016** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for SRS baseline and delivery boundaries.
- [ ] **ERP-0017** (17/20) Run/add ASP.NET unit and validation tests for Trace one SRS requirement to its implementation and test; fix every failure.
- [ ] **ERP-0018** (18/20) Run/add Django unit and parity tests for Flag a requirement with no owner or missing evidence; fix every failure.
- [ ] **ERP-0019** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Every requirement has owner, evidence and explicit in/out-of-scope disposition.
- [ ] **ERP-0020** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 02: Shared architecture, numbering and API contract — ERP-0021 to ERP-0040
**SRS sections:** 46, 54, 55, 56, 57, 58, 60, 61, 63. **Deliverable:** Interchangeable /api behavior, document-number rules and lifecycle conventions.
**Dependencies:** packages 01. **Invariant:** Both backends return the same errors, amounts, statuses and document references.
**Happy-path proof:** Switch VITE_PROXY_TARGET without changing the UI. **Negative proof:** Reject divergent endpoint schemas or duplicate document numbers.

- [ ] **ERP-0021** (01/20) Extract Shared architecture, numbering and API contract acceptance details from SRS §§46, 54, 55, 56, 57, 58, 60, 61, 63; record assumptions and exclusions.
- [ ] **ERP-0022** (02/20) Inspect ASP.NET route conventions, DTOs and transaction design, DRF routes, serializers and transaction design and Vite proxy, shared API client and navigation; record actual files and current behavior.
- [ ] **ERP-0023** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0024** (04/20) Specify the happy-path acceptance: Switch VITE_PROXY_TARGET without changing the UI.
- [ ] **ERP-0025** (05/20) Specify the negative/authorization case: Reject divergent endpoint schemas or duplicate document numbers.
- [ ] **ERP-0026** (06/20) Design data, configuration and numeric BIGINT IDs for Interchangeable /api behavior, document-number rules and lifecycle conventions; record N/A with evidence if schema unchanged.
- [ ] **ERP-0027** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Both backends return the same errors, amounts, statuses and document references.
- [ ] **ERP-0028** (08/20) Implement or repair ASP.NET entities/configuration/contracts for ASP.NET route conventions, DTOs and transaction design.
- [ ] **ERP-0029** (09/20) Implement or repair Django models/serializers/configuration for DRF routes, serializers and transaction design.
- [ ] **ERP-0030** (10/20) Create/review SQL Server migrations and indexes for Shared architecture, numbering and API contract; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0031** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Interchangeable /api behavior, document-number rules and lifecycle conventions.
- [ ] **ERP-0032** (12/20) Implement or repair ASP.NET business operations and idempotency for Shared architecture, numbering and API contract.
- [ ] **ERP-0033** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Shared architecture, numbering and API contract.
- [ ] **ERP-0034** (14/20) Enforce role/branch/action permissions and record audit events for Shared architecture, numbering and API contract; prove server-side denial.
- [ ] **ERP-0035** (15/20) Implement or repair React API integration, screens and user feedback for Vite proxy, shared API client and navigation.
- [ ] **ERP-0036** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Shared architecture, numbering and API contract.
- [ ] **ERP-0037** (17/20) Run/add ASP.NET unit and validation tests for Switch VITE_PROXY_TARGET without changing the UI; fix every failure.
- [ ] **ERP-0038** (18/20) Run/add Django unit and parity tests for Reject divergent endpoint schemas or duplicate document numbers; fix every failure.
- [ ] **ERP-0039** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Both backends return the same errors, amounts, statuses and document references.
- [ ] **ERP-0040** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 03: Developer environment, CI and reproducible builds — ERP-0041 to ERP-0060
**SRS sections:** 56, 59, 62, 65, 66. **Deliverable:** Repeatable local setup, .env templates, CI lint/build/test and clean configuration.
**Dependencies:** packages 01–02. **Invariant:** No secrets committed; both backends start from documented configuration.
**Happy-path proof:** Fresh clone, restore, migrate and run selected backend plus React. **Negative proof:** Fail clearly on missing tool, DB or environment variable.

- [ ] **ERP-0041** (01/20) Extract Developer environment, CI and reproducible builds acceptance details from SRS §§56, 59, 62, 65, 66; record assumptions and exclusions.
- [ ] **ERP-0042** (02/20) Inspect net10 SDK, DotNetEnv, LocalDB, dotnet-ef, startup checks, Python dependencies, mssql ODBC, settings and migrations and Node/Vite env, npm build and local proxy; record actual files and current behavior.
- [ ] **ERP-0043** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0044** (04/20) Specify the happy-path acceptance: Fresh clone, restore, migrate and run selected backend plus React.
- [ ] **ERP-0045** (05/20) Specify the negative/authorization case: Fail clearly on missing tool, DB or environment variable.
- [ ] **ERP-0046** (06/20) Design data, configuration and numeric BIGINT IDs for Repeatable local setup, .env templates, CI lint/build/test and clean configuration; record N/A with evidence if schema unchanged.
- [ ] **ERP-0047** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: No secrets committed; both backends start from documented configuration.
- [ ] **ERP-0048** (08/20) Implement or repair ASP.NET entities/configuration/contracts for net10 SDK, DotNetEnv, LocalDB, dotnet-ef, startup checks.
- [ ] **ERP-0049** (09/20) Implement or repair Django models/serializers/configuration for Python dependencies, mssql ODBC, settings and migrations.
- [ ] **ERP-0050** (10/20) Create/review SQL Server migrations and indexes for Developer environment, CI and reproducible builds; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0051** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Repeatable local setup, .env templates, CI lint/build/test and clean configuration.
- [ ] **ERP-0052** (12/20) Implement or repair ASP.NET business operations and idempotency for Developer environment, CI and reproducible builds.
- [ ] **ERP-0053** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Developer environment, CI and reproducible builds.
- [ ] **ERP-0054** (14/20) Enforce role/branch/action permissions and record audit events for Developer environment, CI and reproducible builds; prove server-side denial.
- [ ] **ERP-0055** (15/20) Implement or repair React API integration, screens and user feedback for Node/Vite env, npm build and local proxy.
- [ ] **ERP-0056** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Developer environment, CI and reproducible builds.
- [ ] **ERP-0057** (17/20) Run/add ASP.NET unit and validation tests for Fresh clone, restore, migrate and run selected backend plus React; fix every failure.
- [ ] **ERP-0058** (18/20) Run/add Django unit and parity tests for Fail clearly on missing tool, DB or environment variable; fix every failure.
- [ ] **ERP-0059** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile No secrets committed; both backends start from documented configuration.
- [ ] **ERP-0060** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 04: SQL Server schema, numeric IDs and migrations — ERP-0061 to ERP-0080
**SRS sections:** 56, 57, 59, 65. **Deliverable:** BIGINT IDENTITY/BigAutoField schema, decimal currency, NVARCHAR and indexed integrity.
**Dependencies:** packages 01–03. **Invariant:** No UUID application IDs, invalid FK or silent float money conversion.
**Happy-path proof:** Create, migrate and query records from both implementations. **Negative proof:** Reject duplicate business keys and orphan records.

- [ ] **ERP-0061** (01/20) Extract SQL Server schema, numeric IDs and migrations acceptance details from SRS §§56, 57, 59, 65; record assumptions and exclusions.
- [ ] **ERP-0062** (02/20) Inspect EF models, initial migrations and migration snapshots, Django models, migrations and mssql compatibility and Numeric-ID handling and safe decimal serialization; record actual files and current behavior.
- [ ] **ERP-0063** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0064** (04/20) Specify the happy-path acceptance: Create, migrate and query records from both implementations.
- [ ] **ERP-0065** (05/20) Specify the negative/authorization case: Reject duplicate business keys and orphan records.
- [ ] **ERP-0066** (06/20) Design data, configuration and numeric BIGINT IDs for BIGINT IDENTITY/BigAutoField schema, decimal currency, NVARCHAR and indexed integrity; record N/A with evidence if schema unchanged.
- [ ] **ERP-0067** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: No UUID application IDs, invalid FK or silent float money conversion.
- [ ] **ERP-0068** (08/20) Implement or repair ASP.NET entities/configuration/contracts for EF models, initial migrations and migration snapshots.
- [ ] **ERP-0069** (09/20) Implement or repair Django models/serializers/configuration for Django models, migrations and mssql compatibility.
- [ ] **ERP-0070** (10/20) Create/review SQL Server migrations and indexes for SQL Server schema, numeric IDs and migrations; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0071** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for BIGINT IDENTITY/BigAutoField schema, decimal currency, NVARCHAR and indexed integrity.
- [ ] **ERP-0072** (12/20) Implement or repair ASP.NET business operations and idempotency for SQL Server schema, numeric IDs and migrations.
- [ ] **ERP-0073** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for SQL Server schema, numeric IDs and migrations.
- [ ] **ERP-0074** (14/20) Enforce role/branch/action permissions and record audit events for SQL Server schema, numeric IDs and migrations; prove server-side denial.
- [ ] **ERP-0075** (15/20) Implement or repair React API integration, screens and user feedback for Numeric-ID handling and safe decimal serialization.
- [ ] **ERP-0076** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for SQL Server schema, numeric IDs and migrations.
- [ ] **ERP-0077** (17/20) Run/add ASP.NET unit and validation tests for Create, migrate and query records from both implementations; fix every failure.
- [ ] **ERP-0078** (18/20) Run/add Django unit and parity tests for Reject duplicate business keys and orphan records; fix every failure.
- [ ] **ERP-0079** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile No UUID application IDs, invalid FK or silent float money conversion.
- [ ] **ERP-0080** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 05: Authentication, session lifecycle and CSRF — ERP-0081 to ERP-0100
**SRS sections:** 6, 7, 57, 59. **Deliverable:** Login/logout/me/CSRF contract with lockout, timeout and bootstrap admin.
**Dependencies:** packages 02–04. **Invariant:** Unauthorized requests are denied and state changes require CSRF.
**Happy-path proof:** Login as seeded administrator and access permitted Company API. **Negative proof:** Deny invalid password, expired session and missing CSRF.

- [ ] **ERP-0081** (01/20) Extract Authentication, session lifecycle and CSRF acceptance details from SRS §§6, 7, 57, 59; record assumptions and exclusions.
- [ ] **ERP-0082** (02/20) Inspect Identity<long>, cookie, anti-forgery and admin seeding, Django sessions, CSRF and user auth and Login, logout, remember-me, expired-session handling; record actual files and current behavior.
- [ ] **ERP-0083** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0084** (04/20) Specify the happy-path acceptance: Login as seeded administrator and access permitted Company API.
- [ ] **ERP-0085** (05/20) Specify the negative/authorization case: Deny invalid password, expired session and missing CSRF.
- [ ] **ERP-0086** (06/20) Design data, configuration and numeric BIGINT IDs for Login/logout/me/CSRF contract with lockout, timeout and bootstrap admin; record N/A with evidence if schema unchanged.
- [ ] **ERP-0087** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Unauthorized requests are denied and state changes require CSRF.
- [ ] **ERP-0088** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Identity<long>, cookie, anti-forgery and admin seeding.
- [ ] **ERP-0089** (09/20) Implement or repair Django models/serializers/configuration for Django sessions, CSRF and user auth.
- [ ] **ERP-0090** (10/20) Create/review SQL Server migrations and indexes for Authentication, session lifecycle and CSRF; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0091** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Login/logout/me/CSRF contract with lockout, timeout and bootstrap admin.
- [ ] **ERP-0092** (12/20) Implement or repair ASP.NET business operations and idempotency for Authentication, session lifecycle and CSRF.
- [ ] **ERP-0093** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Authentication, session lifecycle and CSRF.
- [ ] **ERP-0094** (14/20) Enforce role/branch/action permissions and record audit events for Authentication, session lifecycle and CSRF; prove server-side denial.
- [ ] **ERP-0095** (15/20) Implement or repair React API integration, screens and user feedback for Login, logout, remember-me, expired-session handling.
- [ ] **ERP-0096** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Authentication, session lifecycle and CSRF.
- [ ] **ERP-0097** (17/20) Run/add ASP.NET unit and validation tests for Login as seeded administrator and access permitted Company API; fix every failure.
- [ ] **ERP-0098** (18/20) Run/add Django unit and parity tests for Deny invalid password, expired session and missing CSRF; fix every failure.
- [ ] **ERP-0099** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Unauthorized requests are denied and state changes require CSRF.
- [ ] **ERP-0100** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Phase 2: Authorization, organization and Company Master

### Package 06: Permission catalog and action policies — ERP-0101 to ERP-0120
**SRS sections:** 7, 57, 58, 59, 63. **Deliverable:** Module/action permission keys for View, Add, Edit, Delete, Print, Export, Approve, Cancel, Post and Reverse.
**Dependencies:** packages 05. **Invariant:** UI hiding never replaces server-side enforcement.
**Happy-path proof:** Allow an authorized action through both backends. **Negative proof:** Deny forbidden post, reverse and delete actions.

- [ ] **ERP-0101** (01/20) Extract Permission catalog and action policies acceptance details from SRS §§7, 57, 58, 59, 63; record assumptions and exclusions.
- [ ] **ERP-0102** (02/20) Inspect Permission entities, policy handlers and authorization filters, AccessPermission catalog and action permission classes and Permission Master and actionable error states; record actual files and current behavior.
- [ ] **ERP-0103** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0104** (04/20) Specify the happy-path acceptance: Allow an authorized action through both backends.
- [ ] **ERP-0105** (05/20) Specify the negative/authorization case: Deny forbidden post, reverse and delete actions.
- [ ] **ERP-0106** (06/20) Design data, configuration and numeric BIGINT IDs for Module/action permission keys for View, Add, Edit, Delete, Print, Export, Approve, Cancel, Post and Reverse; record N/A with evidence if schema unchanged.
- [ ] **ERP-0107** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: UI hiding never replaces server-side enforcement.
- [ ] **ERP-0108** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Permission entities, policy handlers and authorization filters.
- [ ] **ERP-0109** (09/20) Implement or repair Django models/serializers/configuration for AccessPermission catalog and action permission classes.
- [ ] **ERP-0110** (10/20) Create/review SQL Server migrations and indexes for Permission catalog and action policies; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0111** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Module/action permission keys for View, Add, Edit, Delete, Print, Export, Approve, Cancel, Post and Reverse.
- [ ] **ERP-0112** (12/20) Implement or repair ASP.NET business operations and idempotency for Permission catalog and action policies.
- [ ] **ERP-0113** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Permission catalog and action policies.
- [ ] **ERP-0114** (14/20) Enforce role/branch/action permissions and record audit events for Permission catalog and action policies; prove server-side denial.
- [ ] **ERP-0115** (15/20) Implement or repair React API integration, screens and user feedback for Permission Master and actionable error states.
- [ ] **ERP-0116** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Permission catalog and action policies.
- [ ] **ERP-0117** (17/20) Run/add ASP.NET unit and validation tests for Allow an authorized action through both backends; fix every failure.
- [ ] **ERP-0118** (18/20) Run/add Django unit and parity tests for Deny forbidden post, reverse and delete actions; fix every failure.
- [ ] **ERP-0119** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile UI hiding never replaces server-side enforcement.
- [ ] **ERP-0120** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 07: Role Master and permission assignment — ERP-0121 to ERP-0140
**SRS sections:** 6, 7, 59, 63. **Deliverable:** CRUD roles and permission matrix with safe default roles.
**Dependencies:** packages 06. **Invariant:** Role edit cannot silently grant privileges outside caller authority.
**Happy-path proof:** Assign Sales role with limited invoice permissions. **Negative proof:** Reject privilege escalation and orphan role mapping.

- [ ] **ERP-0121** (01/20) Extract Role Master and permission assignment acceptance details from SRS §§6, 7, 59, 63; record assumptions and exclusions.
- [ ] **ERP-0122** (02/20) Inspect IdentityRole<long> extensions, role-permission persistence and APIs, Role permissions mapping, serializers and APIs and Role form, matrix, list and edit flow; record actual files and current behavior.
- [ ] **ERP-0123** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0124** (04/20) Specify the happy-path acceptance: Assign Sales role with limited invoice permissions.
- [ ] **ERP-0125** (05/20) Specify the negative/authorization case: Reject privilege escalation and orphan role mapping.
- [ ] **ERP-0126** (06/20) Design data, configuration and numeric BIGINT IDs for CRUD roles and permission matrix with safe default roles; record N/A with evidence if schema unchanged.
- [ ] **ERP-0127** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Role edit cannot silently grant privileges outside caller authority.
- [ ] **ERP-0128** (08/20) Implement or repair ASP.NET entities/configuration/contracts for IdentityRole<long> extensions, role-permission persistence and APIs.
- [ ] **ERP-0129** (09/20) Implement or repair Django models/serializers/configuration for Role permissions mapping, serializers and APIs.
- [ ] **ERP-0130** (10/20) Create/review SQL Server migrations and indexes for Role Master and permission assignment; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0131** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for CRUD roles and permission matrix with safe default roles.
- [ ] **ERP-0132** (12/20) Implement or repair ASP.NET business operations and idempotency for Role Master and permission assignment.
- [ ] **ERP-0133** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Role Master and permission assignment.
- [ ] **ERP-0134** (14/20) Enforce role/branch/action permissions and record audit events for Role Master and permission assignment; prove server-side denial.
- [ ] **ERP-0135** (15/20) Implement or repair React API integration, screens and user feedback for Role form, matrix, list and edit flow.
- [ ] **ERP-0136** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Role Master and permission assignment.
- [ ] **ERP-0137** (17/20) Run/add ASP.NET unit and validation tests for Assign Sales role with limited invoice permissions; fix every failure.
- [ ] **ERP-0138** (18/20) Run/add Django unit and parity tests for Reject privilege escalation and orphan role mapping; fix every failure.
- [ ] **ERP-0139** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Role edit cannot silently grant privileges outside caller authority.
- [ ] **ERP-0140** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 08: User Master and role membership — ERP-0141 to ERP-0160
**SRS sections:** 6, 7, 59, 63. **Deliverable:** Username, employee, email, mobile, role, branch, status and secure password workflows.
**Dependencies:** packages 05–07. **Invariant:** No plaintext password exposure and no disabled-user login.
**Happy-path proof:** Create a sales user and confirm limited access. **Negative proof:** Deny duplicate login and unauthorized role changes.

- [ ] **ERP-0141** (01/20) Extract User Master and role membership acceptance details from SRS §§6, 7, 59, 63; record assumptions and exclusions.
- [ ] **ERP-0142** (02/20) Inspect Identity user DTOs, lifecycle endpoints and reset flow, Custom User API, role assignment and secure password handling and User list/create/edit/deactivate and role selector; record actual files and current behavior.
- [ ] **ERP-0143** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0144** (04/20) Specify the happy-path acceptance: Create a sales user and confirm limited access.
- [ ] **ERP-0145** (05/20) Specify the negative/authorization case: Deny duplicate login and unauthorized role changes.
- [ ] **ERP-0146** (06/20) Design data, configuration and numeric BIGINT IDs for Username, employee, email, mobile, role, branch, status and secure password workflows; record N/A with evidence if schema unchanged.
- [ ] **ERP-0147** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: No plaintext password exposure and no disabled-user login.
- [ ] **ERP-0148** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Identity user DTOs, lifecycle endpoints and reset flow.
- [ ] **ERP-0149** (09/20) Implement or repair Django models/serializers/configuration for Custom User API, role assignment and secure password handling.
- [ ] **ERP-0150** (10/20) Create/review SQL Server migrations and indexes for User Master and role membership; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0151** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Username, employee, email, mobile, role, branch, status and secure password workflows.
- [ ] **ERP-0152** (12/20) Implement or repair ASP.NET business operations and idempotency for User Master and role membership.
- [ ] **ERP-0153** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for User Master and role membership.
- [ ] **ERP-0154** (14/20) Enforce role/branch/action permissions and record audit events for User Master and role membership; prove server-side denial.
- [ ] **ERP-0155** (15/20) Implement or repair React API integration, screens and user feedback for User list/create/edit/deactivate and role selector.
- [ ] **ERP-0156** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for User Master and role membership.
- [ ] **ERP-0157** (17/20) Run/add ASP.NET unit and validation tests for Create a sales user and confirm limited access; fix every failure.
- [ ] **ERP-0158** (18/20) Run/add Django unit and parity tests for Deny duplicate login and unauthorized role changes; fix every failure.
- [ ] **ERP-0159** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile No plaintext password exposure and no disabled-user login.
- [ ] **ERP-0160** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 09: Branch and warehouse access foundation — ERP-0161 to ERP-0180
**SRS sections:** 6, 46, 47, 57, 59. **Deliverable:** Branch/warehouse references, data scoping and single-shop defaults.
**Dependencies:** packages 07–08. **Invariant:** Every scoped transaction resolves to an authorized branch.
**Happy-path proof:** Assign a user to one branch and restrict data correctly. **Negative proof:** Deny cross-branch record access or transfer.

- [ ] **ERP-0161** (01/20) Extract Branch and warehouse access foundation acceptance details from SRS §§6, 46, 47, 57, 59; record assumptions and exclusions.
- [ ] **ERP-0162** (02/20) Inspect Branch/warehouse entities and scoped queries, Equivalent models and scoped query rules and Branch/warehouse selectors where needed; record actual files and current behavior.
- [ ] **ERP-0163** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0164** (04/20) Specify the happy-path acceptance: Assign a user to one branch and restrict data correctly.
- [ ] **ERP-0165** (05/20) Specify the negative/authorization case: Deny cross-branch record access or transfer.
- [ ] **ERP-0166** (06/20) Design data, configuration and numeric BIGINT IDs for Branch/warehouse references, data scoping and single-shop defaults; record N/A with evidence if schema unchanged.
- [ ] **ERP-0167** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Every scoped transaction resolves to an authorized branch.
- [ ] **ERP-0168** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Branch/warehouse entities and scoped queries.
- [ ] **ERP-0169** (09/20) Implement or repair Django models/serializers/configuration for Equivalent models and scoped query rules.
- [ ] **ERP-0170** (10/20) Create/review SQL Server migrations and indexes for Branch and warehouse access foundation; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0171** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Branch/warehouse references, data scoping and single-shop defaults.
- [ ] **ERP-0172** (12/20) Implement or repair ASP.NET business operations and idempotency for Branch and warehouse access foundation.
- [ ] **ERP-0173** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Branch and warehouse access foundation.
- [ ] **ERP-0174** (14/20) Enforce role/branch/action permissions and record audit events for Branch and warehouse access foundation; prove server-side denial.
- [ ] **ERP-0175** (15/20) Implement or repair React API integration, screens and user feedback for Branch/warehouse selectors where needed.
- [ ] **ERP-0176** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Branch and warehouse access foundation.
- [ ] **ERP-0177** (17/20) Run/add ASP.NET unit and validation tests for Assign a user to one branch and restrict data correctly; fix every failure.
- [ ] **ERP-0178** (18/20) Run/add Django unit and parity tests for Deny cross-branch record access or transfer; fix every failure.
- [ ] **ERP-0179** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Every scoped transaction resolves to an authorized branch.
- [ ] **ERP-0180** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 10: Company Master completion and logo lifecycle — ERP-0181 to ERP-0200
**SRS sections:** 4, 5, 40, 59, 63. **Deliverable:** Bilingual Company CRUD, logo validation, document headers and business identity.
**Dependencies:** packages 03–09. **Invariant:** No orphan logo or invalid upload; consistent company identity on documents.
**Happy-path proof:** Add/edit company and print its bilingual identity. **Negative proof:** Reject oversized logo, bad MIME type and unauthorized delete.

- [ ] **ERP-0181** (01/20) Extract Company Master completion and logo lifecycle acceptance details from SRS §§4, 5, 40, 59, 63; record assumptions and exclusions.
- [ ] **ERP-0182** (02/20) Inspect Existing CompaniesApiController, CompanyLogoStorage and validation audit, Existing CompanyViewSet, serializer and logo lifecycle audit and Existing CompanyForm/Table, image preview and validation audit; record actual files and current behavior.
- [ ] **ERP-0183** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0184** (04/20) Specify the happy-path acceptance: Add/edit company and print its bilingual identity.
- [ ] **ERP-0185** (05/20) Specify the negative/authorization case: Reject oversized logo, bad MIME type and unauthorized delete.
- [ ] **ERP-0186** (06/20) Design data, configuration and numeric BIGINT IDs for Bilingual Company CRUD, logo validation, document headers and business identity; record N/A with evidence if schema unchanged.
- [ ] **ERP-0187** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: No orphan logo or invalid upload; consistent company identity on documents.
- [ ] **ERP-0188** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Existing CompaniesApiController, CompanyLogoStorage and validation audit.
- [ ] **ERP-0189** (09/20) Implement or repair Django models/serializers/configuration for Existing CompanyViewSet, serializer and logo lifecycle audit.
- [ ] **ERP-0190** (10/20) Create/review SQL Server migrations and indexes for Company Master completion and logo lifecycle; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0191** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Bilingual Company CRUD, logo validation, document headers and business identity.
- [ ] **ERP-0192** (12/20) Implement or repair ASP.NET business operations and idempotency for Company Master completion and logo lifecycle.
- [ ] **ERP-0193** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Company Master completion and logo lifecycle.
- [ ] **ERP-0194** (14/20) Enforce role/branch/action permissions and record audit events for Company Master completion and logo lifecycle; prove server-side denial.
- [ ] **ERP-0195** (15/20) Implement or repair React API integration, screens and user feedback for Existing CompanyForm/Table, image preview and validation audit.
- [ ] **ERP-0196** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Company Master completion and logo lifecycle.
- [ ] **ERP-0197** (17/20) Run/add ASP.NET unit and validation tests for Add/edit company and print its bilingual identity; fix every failure.
- [ ] **ERP-0198** (18/20) Run/add Django unit and parity tests for Reject oversized logo, bad MIME type and unauthorized delete; fix every failure.
- [ ] **ERP-0199** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile No orphan logo or invalid upload; consistent company identity on documents.
- [ ] **ERP-0200** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Phase 3: Bilingual operational master data

### Package 11: English/Arabic interface and RTL foundation — ERP-0201 to ERP-0220
**SRS sections:** 3, 4, 40, 41, 62, 65. **Deliverable:** Language toggle, Unicode data, RTL layout, locale dates and bilingual printing.
**Dependencies:** packages 01–10. **Invariant:** Arabic survives save/search/print without replacement or truncation.
**Happy-path proof:** Switch language and render an Arabic quotation correctly. **Negative proof:** Catch mixed-direction and missing-translation defects.

- [ ] **ERP-0201** (01/20) Extract English/Arabic interface and RTL foundation acceptance details from SRS §§3, 4, 40, 41, 62, 65; record assumptions and exclusions.
- [ ] **ERP-0202** (02/20) Inspect Localized validation, Unicode persistence and translated document data, Localized serializer errors, Unicode and translated document data and Language switch, RTL-aware UI and accessible responsive navigation; record actual files and current behavior.
- [ ] **ERP-0203** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0204** (04/20) Specify the happy-path acceptance: Switch language and render an Arabic quotation correctly.
- [ ] **ERP-0205** (05/20) Specify the negative/authorization case: Catch mixed-direction and missing-translation defects.
- [ ] **ERP-0206** (06/20) Design data, configuration and numeric BIGINT IDs for Language toggle, Unicode data, RTL layout, locale dates and bilingual printing; record N/A with evidence if schema unchanged.
- [ ] **ERP-0207** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Arabic survives save/search/print without replacement or truncation.
- [ ] **ERP-0208** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Localized validation, Unicode persistence and translated document data.
- [ ] **ERP-0209** (09/20) Implement or repair Django models/serializers/configuration for Localized serializer errors, Unicode and translated document data.
- [ ] **ERP-0210** (10/20) Create/review SQL Server migrations and indexes for English/Arabic interface and RTL foundation; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0211** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Language toggle, Unicode data, RTL layout, locale dates and bilingual printing.
- [ ] **ERP-0212** (12/20) Implement or repair ASP.NET business operations and idempotency for English/Arabic interface and RTL foundation.
- [ ] **ERP-0213** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for English/Arabic interface and RTL foundation.
- [ ] **ERP-0214** (14/20) Enforce role/branch/action permissions and record audit events for English/Arabic interface and RTL foundation; prove server-side denial.
- [ ] **ERP-0215** (15/20) Implement or repair React API integration, screens and user feedback for Language switch, RTL-aware UI and accessible responsive navigation.
- [ ] **ERP-0216** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for English/Arabic interface and RTL foundation.
- [ ] **ERP-0217** (17/20) Run/add ASP.NET unit and validation tests for Switch language and render an Arabic quotation correctly; fix every failure.
- [ ] **ERP-0218** (18/20) Run/add Django unit and parity tests for Catch mixed-direction and missing-translation defects; fix every failure.
- [ ] **ERP-0219** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Arabic survives save/search/print without replacement or truncation.
- [ ] **ERP-0220** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 12: Customer Master and secured documents — ERP-0221 to ERP-0240
**SRS sections:** 4, 8, 9, 51, 52, 57. **Deliverable:** Customer code, bilingual names, ID, types, terms, credit and attachments.
**Dependencies:** packages 06–11. **Invariant:** Unique customer code and no unauthorized access to civil ID/files.
**Happy-path proof:** Create credit customer with Arabic address and payment terms. **Negative proof:** Reject duplicate code, invalid limit and disallowed attachment.

- [ ] **ERP-0221** (01/20) Extract Customer Master and secured documents acceptance details from SRS §§4, 8, 9, 51, 52, 57; record assumptions and exclusions.
- [ ] **ERP-0222** (02/20) Inspect Customer model/API, uniqueness, attachment authorization, Equivalent customer model/serializer/API and protected media and Customer form, searchable list and secure attachment UI; record actual files and current behavior.
- [ ] **ERP-0223** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0224** (04/20) Specify the happy-path acceptance: Create credit customer with Arabic address and payment terms.
- [ ] **ERP-0225** (05/20) Specify the negative/authorization case: Reject duplicate code, invalid limit and disallowed attachment.
- [ ] **ERP-0226** (06/20) Design data, configuration and numeric BIGINT IDs for Customer code, bilingual names, ID, types, terms, credit and attachments; record N/A with evidence if schema unchanged.
- [ ] **ERP-0227** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Unique customer code and no unauthorized access to civil ID/files.
- [ ] **ERP-0228** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Customer model/API, uniqueness, attachment authorization.
- [ ] **ERP-0229** (09/20) Implement or repair Django models/serializers/configuration for Equivalent customer model/serializer/API and protected media.
- [ ] **ERP-0230** (10/20) Create/review SQL Server migrations and indexes for Customer Master and secured documents; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0231** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Customer code, bilingual names, ID, types, terms, credit and attachments.
- [ ] **ERP-0232** (12/20) Implement or repair ASP.NET business operations and idempotency for Customer Master and secured documents.
- [ ] **ERP-0233** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Customer Master and secured documents.
- [ ] **ERP-0234** (14/20) Enforce role/branch/action permissions and record audit events for Customer Master and secured documents; prove server-side denial.
- [ ] **ERP-0235** (15/20) Implement or repair React API integration, screens and user feedback for Customer form, searchable list and secure attachment UI.
- [ ] **ERP-0236** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Customer Master and secured documents.
- [ ] **ERP-0237** (17/20) Run/add ASP.NET unit and validation tests for Create credit customer with Arabic address and payment terms; fix every failure.
- [ ] **ERP-0238** (18/20) Run/add Django unit and parity tests for Reject duplicate code, invalid limit and disallowed attachment; fix every failure.
- [ ] **ERP-0239** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Unique customer code and no unauthorized access to civil ID/files.
- [ ] **ERP-0240** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 13: Supplier Master and secured documents — ERP-0241 to ERP-0260
**SRS sections:** 4, 10, 11, 50, 52, 57. **Deliverable:** Supplier codes, bilingual names, contacts, terms, opening balances and files.
**Dependencies:** packages 06–11. **Invariant:** Unique supplier code and secure supplier-document access.
**Happy-path proof:** Create supplier and later link first purchase. **Negative proof:** Reject duplicate supplier code and unauthorized file access.

- [ ] **ERP-0241** (01/20) Extract Supplier Master and secured documents acceptance details from SRS §§4, 10, 11, 50, 52, 57; record assumptions and exclusions.
- [ ] **ERP-0242** (02/20) Inspect Supplier models, APIs and secure document endpoints, Equivalent supplier serializers, models and document rules and Supplier CRUD and bilingual list; record actual files and current behavior.
- [ ] **ERP-0243** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0244** (04/20) Specify the happy-path acceptance: Create supplier and later link first purchase.
- [ ] **ERP-0245** (05/20) Specify the negative/authorization case: Reject duplicate supplier code and unauthorized file access.
- [ ] **ERP-0246** (06/20) Design data, configuration and numeric BIGINT IDs for Supplier codes, bilingual names, contacts, terms, opening balances and files; record N/A with evidence if schema unchanged.
- [ ] **ERP-0247** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Unique supplier code and secure supplier-document access.
- [ ] **ERP-0248** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Supplier models, APIs and secure document endpoints.
- [ ] **ERP-0249** (09/20) Implement or repair Django models/serializers/configuration for Equivalent supplier serializers, models and document rules.
- [ ] **ERP-0250** (10/20) Create/review SQL Server migrations and indexes for Supplier Master and secured documents; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0251** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Supplier codes, bilingual names, contacts, terms, opening balances and files.
- [ ] **ERP-0252** (12/20) Implement or repair ASP.NET business operations and idempotency for Supplier Master and secured documents.
- [ ] **ERP-0253** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Supplier Master and secured documents.
- [ ] **ERP-0254** (14/20) Enforce role/branch/action permissions and record audit events for Supplier Master and secured documents; prove server-side denial.
- [ ] **ERP-0255** (15/20) Implement or repair React API integration, screens and user feedback for Supplier CRUD and bilingual list.
- [ ] **ERP-0256** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Supplier Master and secured documents.
- [ ] **ERP-0257** (17/20) Run/add ASP.NET unit and validation tests for Create supplier and later link first purchase; fix every failure.
- [ ] **ERP-0258** (18/20) Run/add Django unit and parity tests for Reject duplicate supplier code and unauthorized file access; fix every failure.
- [ ] **ERP-0259** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Unique supplier code and secure supplier-document access.
- [ ] **ERP-0260** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 14: Category and subcategory hierarchy — ERP-0261 to ERP-0280
**SRS sections:** 4, 12, 14, 43, 63. **Deliverable:** Bilingual product categories, hierarchy, status and filtered search.
**Dependencies:** packages 11. **Invariant:** Prevent cycles, duplicate siblings and deletion while referenced.
**Happy-path proof:** Create category/subcategory and assign a product. **Negative proof:** Reject cyclic hierarchy and deleting a referenced category.

- [ ] **ERP-0261** (01/20) Extract Category and subcategory hierarchy acceptance details from SRS §§4, 12, 14, 43, 63; record assumptions and exclusions.
- [ ] **ERP-0262** (02/20) Inspect Category and subcategory entities, endpoints and indexes, Equivalent category models, serializers and filters and Category tree, edit and selection controls; record actual files and current behavior.
- [ ] **ERP-0263** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0264** (04/20) Specify the happy-path acceptance: Create category/subcategory and assign a product.
- [ ] **ERP-0265** (05/20) Specify the negative/authorization case: Reject cyclic hierarchy and deleting a referenced category.
- [ ] **ERP-0266** (06/20) Design data, configuration and numeric BIGINT IDs for Bilingual product categories, hierarchy, status and filtered search; record N/A with evidence if schema unchanged.
- [ ] **ERP-0267** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Prevent cycles, duplicate siblings and deletion while referenced.
- [ ] **ERP-0268** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Category and subcategory entities, endpoints and indexes.
- [ ] **ERP-0269** (09/20) Implement or repair Django models/serializers/configuration for Equivalent category models, serializers and filters.
- [ ] **ERP-0270** (10/20) Create/review SQL Server migrations and indexes for Category and subcategory hierarchy; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0271** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Bilingual product categories, hierarchy, status and filtered search.
- [ ] **ERP-0272** (12/20) Implement or repair ASP.NET business operations and idempotency for Category and subcategory hierarchy.
- [ ] **ERP-0273** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Category and subcategory hierarchy.
- [ ] **ERP-0274** (14/20) Enforce role/branch/action permissions and record audit events for Category and subcategory hierarchy; prove server-side denial.
- [ ] **ERP-0275** (15/20) Implement or repair React API integration, screens and user feedback for Category tree, edit and selection controls.
- [ ] **ERP-0276** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Category and subcategory hierarchy.
- [ ] **ERP-0277** (17/20) Run/add ASP.NET unit and validation tests for Create category/subcategory and assign a product; fix every failure.
- [ ] **ERP-0278** (18/20) Run/add Django unit and parity tests for Reject cyclic hierarchy and deleting a referenced category; fix every failure.
- [ ] **ERP-0279** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Prevent cycles, duplicate siblings and deletion while referenced.
- [ ] **ERP-0280** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 15: Brand and unit masters — ERP-0281 to ERP-0300
**SRS sections:** 4, 12, 14, 63. **Deliverable:** Bilingual brand names and controlled product units.
**Dependencies:** packages 11,14. **Invariant:** Referenced units and brands remain consistent.
**Happy-path proof:** Add brand and unit then use in an item. **Negative proof:** Reject duplicate normalized brand or invalid unit.

- [ ] **ERP-0281** (01/20) Extract Brand and unit masters acceptance details from SRS §§4, 12, 14, 63; record assumptions and exclusions.
- [ ] **ERP-0282** (02/20) Inspect Brand/unit entities, validation and CRUD endpoints, Equivalent brand/unit models and CRUD and Brand/unit list, forms and product selectors; record actual files and current behavior.
- [ ] **ERP-0283** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0284** (04/20) Specify the happy-path acceptance: Add brand and unit then use in an item.
- [ ] **ERP-0285** (05/20) Specify the negative/authorization case: Reject duplicate normalized brand or invalid unit.
- [ ] **ERP-0286** (06/20) Design data, configuration and numeric BIGINT IDs for Bilingual brand names and controlled product units; record N/A with evidence if schema unchanged.
- [ ] **ERP-0287** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Referenced units and brands remain consistent.
- [ ] **ERP-0288** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Brand/unit entities, validation and CRUD endpoints.
- [ ] **ERP-0289** (09/20) Implement or repair Django models/serializers/configuration for Equivalent brand/unit models and CRUD.
- [ ] **ERP-0290** (10/20) Create/review SQL Server migrations and indexes for Brand and unit masters; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0291** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Bilingual brand names and controlled product units.
- [ ] **ERP-0292** (12/20) Implement or repair ASP.NET business operations and idempotency for Brand and unit masters.
- [ ] **ERP-0293** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Brand and unit masters.
- [ ] **ERP-0294** (14/20) Enforce role/branch/action permissions and record audit events for Brand and unit masters; prove server-side denial.
- [ ] **ERP-0295** (15/20) Implement or repair React API integration, screens and user feedback for Brand/unit list, forms and product selectors.
- [ ] **ERP-0296** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Brand and unit masters.
- [ ] **ERP-0297** (17/20) Run/add ASP.NET unit and validation tests for Add brand and unit then use in an item; fix every failure.
- [ ] **ERP-0298** (18/20) Run/add Django unit and parity tests for Reject duplicate normalized brand or invalid unit; fix every failure.
- [ ] **ERP-0299** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Referenced units and brands remain consistent.
- [ ] **ERP-0300** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Phase 4: Products, pricing, tax and transaction rules

### Package 16: Product/Item Master and classification — ERP-0301 to ERP-0320
**SRS sections:** 4, 12, 13, 14, 42, 43. **Deliverable:** Item code/SKU/barcode, EN/AR fields, prices, tax, reorder, status.
**Dependencies:** packages 14–15. **Invariant:** Unique identifiers and correct type-specific validation.
**Happy-path proof:** Create stock item with bilingual description and barcode. **Negative proof:** Reject duplicate SKU, bad price and missing required category.

- [ ] **ERP-0301** (01/20) Extract Product/Item Master and classification acceptance details from SRS §§4, 12, 13, 14, 42, 43; record assumptions and exclusions.
- [ ] **ERP-0302** (02/20) Inspect Product entity, normalized indexes, CRUD and search, Equivalent Product model, serializer, filters and DB indexes and Product form, list, category/brand selectors and pagination; record actual files and current behavior.
- [ ] **ERP-0303** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0304** (04/20) Specify the happy-path acceptance: Create stock item with bilingual description and barcode.
- [ ] **ERP-0305** (05/20) Specify the negative/authorization case: Reject duplicate SKU, bad price and missing required category.
- [ ] **ERP-0306** (06/20) Design data, configuration and numeric BIGINT IDs for Item code/SKU/barcode, EN/AR fields, prices, tax, reorder, status; record N/A with evidence if schema unchanged.
- [ ] **ERP-0307** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Unique identifiers and correct type-specific validation.
- [ ] **ERP-0308** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Product entity, normalized indexes, CRUD and search.
- [ ] **ERP-0309** (09/20) Implement or repair Django models/serializers/configuration for Equivalent Product model, serializer, filters and DB indexes.
- [ ] **ERP-0310** (10/20) Create/review SQL Server migrations and indexes for Product/Item Master and classification; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0311** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Item code/SKU/barcode, EN/AR fields, prices, tax, reorder, status.
- [ ] **ERP-0312** (12/20) Implement or repair ASP.NET business operations and idempotency for Product/Item Master and classification.
- [ ] **ERP-0313** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Product/Item Master and classification.
- [ ] **ERP-0314** (14/20) Enforce role/branch/action permissions and record audit events for Product/Item Master and classification; prove server-side denial.
- [ ] **ERP-0315** (15/20) Implement or repair React API integration, screens and user feedback for Product form, list, category/brand selectors and pagination.
- [ ] **ERP-0316** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Product/Item Master and classification.
- [ ] **ERP-0317** (17/20) Run/add ASP.NET unit and validation tests for Create stock item with bilingual description and barcode; fix every failure.
- [ ] **ERP-0318** (18/20) Run/add Django unit and parity tests for Reject duplicate SKU, bad price and missing required category; fix every failure.
- [ ] **ERP-0319** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Unique identifiers and correct type-specific validation.
- [ ] **ERP-0320** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 17: Stock, non-stock and digital license products — ERP-0321 to ERP-0340
**SRS sections:** 12, 13, 15, 16, 57. **Deliverable:** Type-specific inventory behavior and secure optional license lifecycle.
**Dependencies:** packages 16. **Invariant:** Non-stock never changes quantity and digital keys are permission-protected.
**Happy-path proof:** Sell non-stock service and provision a digital license. **Negative proof:** Reject stock movement for non-stock and duplicated active key.

- [ ] **ERP-0321** (01/20) Extract Stock, non-stock and digital license products acceptance details from SRS §§12, 13, 15, 16, 57; record assumptions and exclusions.
- [ ] **ERP-0322** (02/20) Inspect Product-type rules, license entities and validation APIs, Equivalent type-specific model and license lifecycle and Type selector, masked license input and expiry display; record actual files and current behavior.
- [ ] **ERP-0323** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0324** (04/20) Specify the happy-path acceptance: Sell non-stock service and provision a digital license.
- [ ] **ERP-0325** (05/20) Specify the negative/authorization case: Reject stock movement for non-stock and duplicated active key.
- [ ] **ERP-0326** (06/20) Design data, configuration and numeric BIGINT IDs for Type-specific inventory behavior and secure optional license lifecycle; record N/A with evidence if schema unchanged.
- [ ] **ERP-0327** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Non-stock never changes quantity and digital keys are permission-protected.
- [ ] **ERP-0328** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Product-type rules, license entities and validation APIs.
- [ ] **ERP-0329** (09/20) Implement or repair Django models/serializers/configuration for Equivalent type-specific model and license lifecycle.
- [ ] **ERP-0330** (10/20) Create/review SQL Server migrations and indexes for Stock, non-stock and digital license products; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0331** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Type-specific inventory behavior and secure optional license lifecycle.
- [ ] **ERP-0332** (12/20) Implement or repair ASP.NET business operations and idempotency for Stock, non-stock and digital license products.
- [ ] **ERP-0333** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Stock, non-stock and digital license products.
- [ ] **ERP-0334** (14/20) Enforce role/branch/action permissions and record audit events for Stock, non-stock and digital license products; prove server-side denial.
- [ ] **ERP-0335** (15/20) Implement or repair React API integration, screens and user feedback for Type selector, masked license input and expiry display.
- [ ] **ERP-0336** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Stock, non-stock and digital license products.
- [ ] **ERP-0337** (17/20) Run/add ASP.NET unit and validation tests for Sell non-stock service and provision a digital license; fix every failure.
- [ ] **ERP-0338** (18/20) Run/add Django unit and parity tests for Reject stock movement for non-stock and duplicated active key; fix every failure.
- [ ] **ERP-0339** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Non-stock never changes quantity and digital keys are permission-protected.
- [ ] **ERP-0340** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 18: Configurable tax and decimal calculation engine — ERP-0341 to ERP-0360
**SRS sections:** 12, 18, 23, 28, 35, 57. **Deliverable:** Tax categories and precise gross/discount/tax/total calculations.
**Dependencies:** packages 04,16. **Invariant:** No hard-coded Kuwait tax rate; accountant confirms live tax treatment.
**Happy-path proof:** Compute taxable, exempt and zero-rate invoice lines. **Negative proof:** Reject invalid rate and cross-backend rounding mismatch.

- [ ] **ERP-0341** (01/20) Extract Configurable tax and decimal calculation engine acceptance details from SRS §§12, 18, 23, 28, 35, 57; record assumptions and exclusions.
- [ ] **ERP-0342** (02/20) Inspect Decimal-only money/tax calculators and tax settings, Decimal parity calculators, category APIs and migrations and Tax config screen and transparent calculation preview; record actual files and current behavior.
- [ ] **ERP-0343** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0344** (04/20) Specify the happy-path acceptance: Compute taxable, exempt and zero-rate invoice lines.
- [ ] **ERP-0345** (05/20) Specify the negative/authorization case: Reject invalid rate and cross-backend rounding mismatch.
- [ ] **ERP-0346** (06/20) Design data, configuration and numeric BIGINT IDs for Tax categories and precise gross/discount/tax/total calculations; record N/A with evidence if schema unchanged.
- [ ] **ERP-0347** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: No hard-coded Kuwait tax rate; accountant confirms live tax treatment.
- [ ] **ERP-0348** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Decimal-only money/tax calculators and tax settings.
- [ ] **ERP-0349** (09/20) Implement or repair Django models/serializers/configuration for Decimal parity calculators, category APIs and migrations.
- [ ] **ERP-0350** (10/20) Create/review SQL Server migrations and indexes for Configurable tax and decimal calculation engine; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0351** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Tax categories and precise gross/discount/tax/total calculations.
- [ ] **ERP-0352** (12/20) Implement or repair ASP.NET business operations and idempotency for Configurable tax and decimal calculation engine.
- [ ] **ERP-0353** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Configurable tax and decimal calculation engine.
- [ ] **ERP-0354** (14/20) Enforce role/branch/action permissions and record audit events for Configurable tax and decimal calculation engine; prove server-side denial.
- [ ] **ERP-0355** (15/20) Implement or repair React API integration, screens and user feedback for Tax config screen and transparent calculation preview.
- [ ] **ERP-0356** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Configurable tax and decimal calculation engine.
- [ ] **ERP-0357** (17/20) Run/add ASP.NET unit and validation tests for Compute taxable, exempt and zero-rate invoice lines; fix every failure.
- [ ] **ERP-0358** (18/20) Run/add Django unit and parity tests for Reject invalid rate and cross-backend rounding mismatch; fix every failure.
- [ ] **ERP-0359** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile No hard-coded Kuwait tax rate; accountant confirms live tax treatment.
- [ ] **ERP-0360** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 19: Payment methods and payment terms — ERP-0361 to ERP-0380
**SRS sections:** 23, 26, 50, 56. **Deliverable:** Cash, KNET, card, transfer, cheque and customizable due dates.
**Dependencies:** packages 12–13,18. **Invariant:** Posting uses enabled methods and reproducible due dates.
**Happy-path proof:** Configure 30-day terms and KNET metadata. **Negative proof:** Reject disabled method and inconsistent due date.

- [ ] **ERP-0361** (01/20) Extract Payment methods and payment terms acceptance details from SRS §§23, 26, 50, 56; record assumptions and exclusions.
- [ ] **ERP-0362** (02/20) Inspect Payment method/terms masters and due-date rules, Equivalent method/terms models and validation and Method and terms settings with transaction selectors; record actual files and current behavior.
- [ ] **ERP-0363** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0364** (04/20) Specify the happy-path acceptance: Configure 30-day terms and KNET metadata.
- [ ] **ERP-0365** (05/20) Specify the negative/authorization case: Reject disabled method and inconsistent due date.
- [ ] **ERP-0366** (06/20) Design data, configuration and numeric BIGINT IDs for Cash, KNET, card, transfer, cheque and customizable due dates; record N/A with evidence if schema unchanged.
- [ ] **ERP-0367** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Posting uses enabled methods and reproducible due dates.
- [ ] **ERP-0368** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Payment method/terms masters and due-date rules.
- [ ] **ERP-0369** (09/20) Implement or repair Django models/serializers/configuration for Equivalent method/terms models and validation.
- [ ] **ERP-0370** (10/20) Create/review SQL Server migrations and indexes for Payment methods and payment terms; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0371** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Cash, KNET, card, transfer, cheque and customizable due dates.
- [ ] **ERP-0372** (12/20) Implement or repair ASP.NET business operations and idempotency for Payment methods and payment terms.
- [ ] **ERP-0373** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Payment methods and payment terms.
- [ ] **ERP-0374** (14/20) Enforce role/branch/action permissions and record audit events for Payment methods and payment terms; prove server-side denial.
- [ ] **ERP-0375** (15/20) Implement or repair React API integration, screens and user feedback for Method and terms settings with transaction selectors.
- [ ] **ERP-0376** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Payment methods and payment terms.
- [ ] **ERP-0377** (17/20) Run/add ASP.NET unit and validation tests for Configure 30-day terms and KNET metadata; fix every failure.
- [ ] **ERP-0378** (18/20) Run/add Django unit and parity tests for Reject disabled method and inconsistent due date; fix every failure.
- [ ] **ERP-0379** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Posting uses enabled methods and reproducible due dates.
- [ ] **ERP-0380** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 20: Price lists, promotions and discount authorization — ERP-0381 to ERP-0400
**SRS sections:** 12, 23, 48, 49, 51, 57. **Deliverable:** Retail/wholesale/corporate/special prices, item/invoice discount limits.
**Dependencies:** packages 06–08,16,18–19. **Invariant:** Minimum selling price and per-role discounts enforced on server.
**Happy-path proof:** Apply authorized special price and fixed/percentage discount. **Negative proof:** Deny unauthorized discount and stale price selection.

- [ ] **ERP-0381** (01/20) Extract Price lists, promotions and discount authorization acceptance details from SRS §§12, 23, 48, 49, 51, 57; record assumptions and exclusions.
- [ ] **ERP-0382** (02/20) Inspect Price list models, effective dates and approval rules, Equivalent price/discount rules and serializers and Price list CRUD, applied-price and approval UI; record actual files and current behavior.
- [ ] **ERP-0383** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0384** (04/20) Specify the happy-path acceptance: Apply authorized special price and fixed/percentage discount.
- [ ] **ERP-0385** (05/20) Specify the negative/authorization case: Deny unauthorized discount and stale price selection.
- [ ] **ERP-0386** (06/20) Design data, configuration and numeric BIGINT IDs for Retail/wholesale/corporate/special prices, item/invoice discount limits; record N/A with evidence if schema unchanged.
- [ ] **ERP-0387** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Minimum selling price and per-role discounts enforced on server.
- [ ] **ERP-0388** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Price list models, effective dates and approval rules.
- [ ] **ERP-0389** (09/20) Implement or repair Django models/serializers/configuration for Equivalent price/discount rules and serializers.
- [ ] **ERP-0390** (10/20) Create/review SQL Server migrations and indexes for Price lists, promotions and discount authorization; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0391** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Retail/wholesale/corporate/special prices, item/invoice discount limits.
- [ ] **ERP-0392** (12/20) Implement or repair ASP.NET business operations and idempotency for Price lists, promotions and discount authorization.
- [ ] **ERP-0393** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Price lists, promotions and discount authorization.
- [ ] **ERP-0394** (14/20) Enforce role/branch/action permissions and record audit events for Price lists, promotions and discount authorization; prove server-side denial.
- [ ] **ERP-0395** (15/20) Implement or repair React API integration, screens and user feedback for Price list CRUD, applied-price and approval UI.
- [ ] **ERP-0396** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Price lists, promotions and discount authorization.
- [ ] **ERP-0397** (17/20) Run/add ASP.NET unit and validation tests for Apply authorized special price and fixed/percentage discount; fix every failure.
- [ ] **ERP-0398** (18/20) Run/add Django unit and parity tests for Deny unauthorized discount and stale price selection; fix every failure.
- [ ] **ERP-0399** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Minimum selling price and per-role discounts enforced on server.
- [ ] **ERP-0400** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Phase 5: Stock foundations and purchase posting

### Package 21: Stock ledger and opening inventory — ERP-0401 to ERP-0420
**SRS sections:** 12, 17, 18, 29, 34, 56, 57. **Deliverable:** Append-only stock transaction ledger, opening quantities and on-hand projection.
**Dependencies:** packages 04,09,16. **Invariant:** Exactly one stock movement per valid posting; no negative stock by default.
**Happy-path proof:** Post opening stock and verify on-hand. **Negative proof:** Block double posting and selling beyond available stock.

- [ ] **ERP-0401** (01/20) Extract Stock ledger and opening inventory acceptance details from SRS §§12, 17, 18, 29, 34, 56, 57; record assumptions and exclusions.
- [ ] **ERP-0402** (02/20) Inspect StockMovement entities, atomic posting and quantity read models, Equivalent stock ledger and transaction boundaries and Opening stock and current-stock views; record actual files and current behavior.
- [ ] **ERP-0403** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0404** (04/20) Specify the happy-path acceptance: Post opening stock and verify on-hand.
- [ ] **ERP-0405** (05/20) Specify the negative/authorization case: Block double posting and selling beyond available stock.
- [ ] **ERP-0406** (06/20) Design data, configuration and numeric BIGINT IDs for Append-only stock transaction ledger, opening quantities and on-hand projection; record N/A with evidence if schema unchanged.
- [ ] **ERP-0407** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Exactly one stock movement per valid posting; no negative stock by default.
- [ ] **ERP-0408** (08/20) Implement or repair ASP.NET entities/configuration/contracts for StockMovement entities, atomic posting and quantity read models.
- [ ] **ERP-0409** (09/20) Implement or repair Django models/serializers/configuration for Equivalent stock ledger and transaction boundaries.
- [ ] **ERP-0410** (10/20) Create/review SQL Server migrations and indexes for Stock ledger and opening inventory; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0411** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Append-only stock transaction ledger, opening quantities and on-hand projection.
- [ ] **ERP-0412** (12/20) Implement or repair ASP.NET business operations and idempotency for Stock ledger and opening inventory.
- [ ] **ERP-0413** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Stock ledger and opening inventory.
- [ ] **ERP-0414** (14/20) Enforce role/branch/action permissions and record audit events for Stock ledger and opening inventory; prove server-side denial.
- [ ] **ERP-0415** (15/20) Implement or repair React API integration, screens and user feedback for Opening stock and current-stock views.
- [ ] **ERP-0416** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Stock ledger and opening inventory.
- [ ] **ERP-0417** (17/20) Run/add ASP.NET unit and validation tests for Post opening stock and verify on-hand; fix every failure.
- [ ] **ERP-0418** (18/20) Run/add Django unit and parity tests for Block double posting and selling beyond available stock; fix every failure.
- [ ] **ERP-0419** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Exactly one stock movement per valid posting; no negative stock by default.
- [ ] **ERP-0420** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 22: Serial number ownership and history — ERP-0421 to ERP-0440
**SRS sections:** 15, 16, 18, 23, 29, 43, 57. **Deliverable:** Unique serial intake, reservations, sale, return and complete provenance.
**Dependencies:** packages 16,21. **Invariant:** Same serial cannot occupy two sellable states or be sold twice.
**Happy-path proof:** Receive serial then sell exact serial to one customer. **Negative proof:** Deny duplicate serial, wrong warehouse and second sale.

- [ ] **ERP-0421** (01/20) Extract Serial number ownership and history acceptance details from SRS §§15, 16, 18, 23, 29, 43, 57; record assumptions and exclusions.
- [ ] **ERP-0422** (02/20) Inspect Serial entities, indexed uniqueness and state transitions, Equivalent serial lifecycle and locking and Serial capture/selection and history viewer; record actual files and current behavior.
- [ ] **ERP-0423** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0424** (04/20) Specify the happy-path acceptance: Receive serial then sell exact serial to one customer.
- [ ] **ERP-0425** (05/20) Specify the negative/authorization case: Deny duplicate serial, wrong warehouse and second sale.
- [ ] **ERP-0426** (06/20) Design data, configuration and numeric BIGINT IDs for Unique serial intake, reservations, sale, return and complete provenance; record N/A with evidence if schema unchanged.
- [ ] **ERP-0427** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Same serial cannot occupy two sellable states or be sold twice.
- [ ] **ERP-0428** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Serial entities, indexed uniqueness and state transitions.
- [ ] **ERP-0429** (09/20) Implement or repair Django models/serializers/configuration for Equivalent serial lifecycle and locking.
- [ ] **ERP-0430** (10/20) Create/review SQL Server migrations and indexes for Serial number ownership and history; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0431** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Unique serial intake, reservations, sale, return and complete provenance.
- [ ] **ERP-0432** (12/20) Implement or repair ASP.NET business operations and idempotency for Serial number ownership and history.
- [ ] **ERP-0433** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Serial number ownership and history.
- [ ] **ERP-0434** (14/20) Enforce role/branch/action permissions and record audit events for Serial number ownership and history; prove server-side denial.
- [ ] **ERP-0435** (15/20) Implement or repair React API integration, screens and user feedback for Serial capture/selection and history viewer.
- [ ] **ERP-0436** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Serial number ownership and history.
- [ ] **ERP-0437** (17/20) Run/add ASP.NET unit and validation tests for Receive serial then sell exact serial to one customer; fix every failure.
- [ ] **ERP-0438** (18/20) Run/add Django unit and parity tests for Deny duplicate serial, wrong warehouse and second sale; fix every failure.
- [ ] **ERP-0439** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Same serial cannot occupy two sellable states or be sold twice.
- [ ] **ERP-0440** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 23: Warranty tracking and expiry — ERP-0441 to ERP-0460
**SRS sections:** 15, 16, 37, 39, 53. **Deliverable:** Supplier/company warranty, start/end, invoice and customer association.
**Dependencies:** packages 22,30. **Invariant:** Warranty binds correct sold serial and source invoice.
**Happy-path proof:** Retrieve active warranty for sold serial. **Negative proof:** Reject warranty without sale or invalid date span.

- [ ] **ERP-0441** (01/20) Extract Warranty tracking and expiry acceptance details from SRS §§15, 16, 37, 39, 53; record assumptions and exclusions.
- [ ] **ERP-0442** (02/20) Inspect Warranty entities, date calculation and trace endpoints, Equivalent warranty models and status computation and Warranty lookup, status and claim links; record actual files and current behavior.
- [ ] **ERP-0443** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0444** (04/20) Specify the happy-path acceptance: Retrieve active warranty for sold serial.
- [ ] **ERP-0445** (05/20) Specify the negative/authorization case: Reject warranty without sale or invalid date span.
- [ ] **ERP-0446** (06/20) Design data, configuration and numeric BIGINT IDs for Supplier/company warranty, start/end, invoice and customer association; record N/A with evidence if schema unchanged.
- [ ] **ERP-0447** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Warranty binds correct sold serial and source invoice.
- [ ] **ERP-0448** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Warranty entities, date calculation and trace endpoints.
- [ ] **ERP-0449** (09/20) Implement or repair Django models/serializers/configuration for Equivalent warranty models and status computation.
- [ ] **ERP-0450** (10/20) Create/review SQL Server migrations and indexes for Warranty tracking and expiry; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0451** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Supplier/company warranty, start/end, invoice and customer association.
- [ ] **ERP-0452** (12/20) Implement or repair ASP.NET business operations and idempotency for Warranty tracking and expiry.
- [ ] **ERP-0453** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Warranty tracking and expiry.
- [ ] **ERP-0454** (14/20) Enforce role/branch/action permissions and record audit events for Warranty tracking and expiry; prove server-side denial.
- [ ] **ERP-0455** (15/20) Implement or repair React API integration, screens and user feedback for Warranty lookup, status and claim links.
- [ ] **ERP-0456** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Warranty tracking and expiry.
- [ ] **ERP-0457** (17/20) Run/add ASP.NET unit and validation tests for Retrieve active warranty for sold serial; fix every failure.
- [ ] **ERP-0458** (18/20) Run/add Django unit and parity tests for Reject warranty without sale or invalid date span; fix every failure.
- [ ] **ERP-0459** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Warranty binds correct sold serial and source invoice.
- [ ] **ERP-0460** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 24: Purchase Order and Goods Receipt — ERP-0461 to ERP-0480
**SRS sections:** 17, 18, 29, 54, 55, 58. **Deliverable:** PO lifecycle, supplier lines, deliveries, receipts and references.
**Dependencies:** packages 08–09,13,16,18,21. **Invariant:** Receiving cannot exceed open ordered quantity without approved variance.
**Happy-path proof:** Approve PO and partially receive items. **Negative proof:** Reject unauthorized approval and duplicate receipt.

- [ ] **ERP-0461** (01/20) Extract Purchase Order and Goods Receipt acceptance details from SRS §§17, 18, 29, 54, 55, 58; record assumptions and exclusions.
- [ ] **ERP-0462** (02/20) Inspect PO/receipt entities, approval and partial receiving handlers, Equivalent PO/receipt models and transactional APIs and PO editor, approval and receipt screens; record actual files and current behavior.
- [ ] **ERP-0463** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0464** (04/20) Specify the happy-path acceptance: Approve PO and partially receive items.
- [ ] **ERP-0465** (05/20) Specify the negative/authorization case: Reject unauthorized approval and duplicate receipt.
- [ ] **ERP-0466** (06/20) Design data, configuration and numeric BIGINT IDs for PO lifecycle, supplier lines, deliveries, receipts and references; record N/A with evidence if schema unchanged.
- [ ] **ERP-0467** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Receiving cannot exceed open ordered quantity without approved variance.
- [ ] **ERP-0468** (08/20) Implement or repair ASP.NET entities/configuration/contracts for PO/receipt entities, approval and partial receiving handlers.
- [ ] **ERP-0469** (09/20) Implement or repair Django models/serializers/configuration for Equivalent PO/receipt models and transactional APIs.
- [ ] **ERP-0470** (10/20) Create/review SQL Server migrations and indexes for Purchase Order and Goods Receipt; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0471** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for PO lifecycle, supplier lines, deliveries, receipts and references.
- [ ] **ERP-0472** (12/20) Implement or repair ASP.NET business operations and idempotency for Purchase Order and Goods Receipt.
- [ ] **ERP-0473** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Purchase Order and Goods Receipt.
- [ ] **ERP-0474** (14/20) Enforce role/branch/action permissions and record audit events for Purchase Order and Goods Receipt; prove server-side denial.
- [ ] **ERP-0475** (15/20) Implement or repair React API integration, screens and user feedback for PO editor, approval and receipt screens.
- [ ] **ERP-0476** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Purchase Order and Goods Receipt.
- [ ] **ERP-0477** (17/20) Run/add ASP.NET unit and validation tests for Approve PO and partially receive items; fix every failure.
- [ ] **ERP-0478** (18/20) Run/add Django unit and parity tests for Reject unauthorized approval and duplicate receipt; fix every failure.
- [ ] **ERP-0479** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Receiving cannot exceed open ordered quantity without approved variance.
- [ ] **ERP-0480** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 25: Purchase Invoice posting and stock increase — ERP-0481 to ERP-0500
**SRS sections:** 18, 28, 29, 54, 55, 57, 58. **Deliverable:** Supplier invoice, costs, tax, serialized intake and single atomic stock/payable post.
**Dependencies:** packages 18,21–24. **Invariant:** Invoice number unique and stock/payable post exactly once.
**Happy-path proof:** Post purchase, increase stock and supplier outstanding. **Negative proof:** Reject duplicate supplier invoice and repeated posting.

- [ ] **ERP-0481** (01/20) Extract Purchase Invoice posting and stock increase acceptance details from SRS §§18, 28, 29, 54, 55, 57, 58; record assumptions and exclusions.
- [ ] **ERP-0482** (02/20) Inspect Purchase invoice/line/post commands with EF transaction, Equivalent invoice/line services and database.atomic and Invoice entry, serial capture, posting and payable preview; record actual files and current behavior.
- [ ] **ERP-0483** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0484** (04/20) Specify the happy-path acceptance: Post purchase, increase stock and supplier outstanding.
- [ ] **ERP-0485** (05/20) Specify the negative/authorization case: Reject duplicate supplier invoice and repeated posting.
- [ ] **ERP-0486** (06/20) Design data, configuration and numeric BIGINT IDs for Supplier invoice, costs, tax, serialized intake and single atomic stock/payable post; record N/A with evidence if schema unchanged.
- [ ] **ERP-0487** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Invoice number unique and stock/payable post exactly once.
- [ ] **ERP-0488** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Purchase invoice/line/post commands with EF transaction.
- [ ] **ERP-0489** (09/20) Implement or repair Django models/serializers/configuration for Equivalent invoice/line services and database.atomic.
- [ ] **ERP-0490** (10/20) Create/review SQL Server migrations and indexes for Purchase Invoice posting and stock increase; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0491** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Supplier invoice, costs, tax, serialized intake and single atomic stock/payable post.
- [ ] **ERP-0492** (12/20) Implement or repair ASP.NET business operations and idempotency for Purchase Invoice posting and stock increase.
- [ ] **ERP-0493** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Purchase Invoice posting and stock increase.
- [ ] **ERP-0494** (14/20) Enforce role/branch/action permissions and record audit events for Purchase Invoice posting and stock increase; prove server-side denial.
- [ ] **ERP-0495** (15/20) Implement or repair React API integration, screens and user feedback for Invoice entry, serial capture, posting and payable preview.
- [ ] **ERP-0496** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Purchase Invoice posting and stock increase.
- [ ] **ERP-0497** (17/20) Run/add ASP.NET unit and validation tests for Post purchase, increase stock and supplier outstanding; fix every failure.
- [ ] **ERP-0498** (18/20) Run/add Django unit and parity tests for Reject duplicate supplier invoice and repeated posting; fix every failure.
- [ ] **ERP-0499** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Invoice number unique and stock/payable post exactly once.
- [ ] **ERP-0500** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Phase 6: Procurement completion and quotation-to-sales

### Package 26: Purchase Return and stock decrease — ERP-0501 to ERP-0520
**SRS sections:** 19, 29, 55, 57, 58. **Deliverable:** Original purchase links, serial return, supplier balance reversal and status.
**Dependencies:** packages 22,25. **Invariant:** Return quantity cannot exceed available received quantity.
**Happy-path proof:** Post return and reduce stock/payable correctly. **Negative proof:** Reject unrelated serial or double returned quantity.

- [ ] **ERP-0501** (01/20) Extract Purchase Return and stock decrease acceptance details from SRS §§19, 29, 55, 57, 58; record assumptions and exclusions.
- [ ] **ERP-0502** (02/20) Inspect PurchaseReturn entities and atomic reverse movements, Equivalent return posting and reversal APIs and Purchase return form and source-line selection; record actual files and current behavior.
- [ ] **ERP-0503** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0504** (04/20) Specify the happy-path acceptance: Post return and reduce stock/payable correctly.
- [ ] **ERP-0505** (05/20) Specify the negative/authorization case: Reject unrelated serial or double returned quantity.
- [ ] **ERP-0506** (06/20) Design data, configuration and numeric BIGINT IDs for Original purchase links, serial return, supplier balance reversal and status; record N/A with evidence if schema unchanged.
- [ ] **ERP-0507** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Return quantity cannot exceed available received quantity.
- [ ] **ERP-0508** (08/20) Implement or repair ASP.NET entities/configuration/contracts for PurchaseReturn entities and atomic reverse movements.
- [ ] **ERP-0509** (09/20) Implement or repair Django models/serializers/configuration for Equivalent return posting and reversal APIs.
- [ ] **ERP-0510** (10/20) Create/review SQL Server migrations and indexes for Purchase Return and stock decrease; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0511** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Original purchase links, serial return, supplier balance reversal and status.
- [ ] **ERP-0512** (12/20) Implement or repair ASP.NET business operations and idempotency for Purchase Return and stock decrease.
- [ ] **ERP-0513** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Purchase Return and stock decrease.
- [ ] **ERP-0514** (14/20) Enforce role/branch/action permissions and record audit events for Purchase Return and stock decrease; prove server-side denial.
- [ ] **ERP-0515** (15/20) Implement or repair React API integration, screens and user feedback for Purchase return form and source-line selection.
- [ ] **ERP-0516** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Purchase Return and stock decrease.
- [ ] **ERP-0517** (17/20) Run/add ASP.NET unit and validation tests for Post return and reduce stock/payable correctly; fix every failure.
- [ ] **ERP-0518** (18/20) Run/add Django unit and parity tests for Reject unrelated serial or double returned quantity; fix every failure.
- [ ] **ERP-0519** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Return quantity cannot exceed available received quantity.
- [ ] **ERP-0520** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 27: Supplier payment, allocation and ledger — ERP-0521 to ERP-0540
**SRS sections:** 10, 11, 19, 26, 50, 55, 57. **Deliverable:** Supplier payments, invoice allocation, outstanding and statement entries.
**Dependencies:** packages 13,19,25–26. **Invariant:** Allocated total never exceeds payment or allowed invoice balance.
**Happy-path proof:** Partially pay supplier invoice and reconcile ledger. **Negative proof:** Reject duplicate reference and over-allocation.

- [ ] **ERP-0521** (01/20) Extract Supplier payment, allocation and ledger acceptance details from SRS §§10, 11, 19, 26, 50, 55, 57; record assumptions and exclusions.
- [ ] **ERP-0522** (02/20) Inspect Supplier payment, allocation and ledger queries, Equivalent payment/ledger models and APIs and Payables, payment entry and supplier statement; record actual files and current behavior.
- [ ] **ERP-0523** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0524** (04/20) Specify the happy-path acceptance: Partially pay supplier invoice and reconcile ledger.
- [ ] **ERP-0525** (05/20) Specify the negative/authorization case: Reject duplicate reference and over-allocation.
- [ ] **ERP-0526** (06/20) Design data, configuration and numeric BIGINT IDs for Supplier payments, invoice allocation, outstanding and statement entries; record N/A with evidence if schema unchanged.
- [ ] **ERP-0527** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Allocated total never exceeds payment or allowed invoice balance.
- [ ] **ERP-0528** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Supplier payment, allocation and ledger queries.
- [ ] **ERP-0529** (09/20) Implement or repair Django models/serializers/configuration for Equivalent payment/ledger models and APIs.
- [ ] **ERP-0530** (10/20) Create/review SQL Server migrations and indexes for Supplier payment, allocation and ledger; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0531** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Supplier payments, invoice allocation, outstanding and statement entries.
- [ ] **ERP-0532** (12/20) Implement or repair ASP.NET business operations and idempotency for Supplier payment, allocation and ledger.
- [ ] **ERP-0533** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Supplier payment, allocation and ledger.
- [ ] **ERP-0534** (14/20) Enforce role/branch/action permissions and record audit events for Supplier payment, allocation and ledger; prove server-side denial.
- [ ] **ERP-0535** (15/20) Implement or repair React API integration, screens and user feedback for Payables, payment entry and supplier statement.
- [ ] **ERP-0536** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Supplier payment, allocation and ledger.
- [ ] **ERP-0537** (17/20) Run/add ASP.NET unit and validation tests for Partially pay supplier invoice and reconcile ledger; fix every failure.
- [ ] **ERP-0538** (18/20) Run/add Django unit and parity tests for Reject duplicate reference and over-allocation; fix every failure.
- [ ] **ERP-0539** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Allocated total never exceeds payment or allowed invoice balance.
- [ ] **ERP-0540** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 28: Quotation creation, approval and bilingual print — ERP-0541 to ERP-0560
**SRS sections:** 20, 21, 40, 41, 54, 55, 58. **Deliverable:** Draft/Sent/Approved/Rejected/Expired/Converted states and valid-until.
**Dependencies:** packages 08,11–12,16,18,20. **Invariant:** Expired/rejected quotes cannot silently be approved/converted.
**Happy-path proof:** Create bilingual quotation and approve with correct total. **Negative proof:** Reject expired approval or unauthorized price override.

- [ ] **ERP-0541** (01/20) Extract Quotation creation, approval and bilingual print acceptance details from SRS §§20, 21, 40, 41, 54, 55, 58; record assumptions and exclusions.
- [ ] **ERP-0542** (02/20) Inspect Quotation models, totals, approvals and preview endpoint, Equivalent quotation models, status and serializer rules and Quotation form, approval, bilingual preview and print; record actual files and current behavior.
- [ ] **ERP-0543** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0544** (04/20) Specify the happy-path acceptance: Create bilingual quotation and approve with correct total.
- [ ] **ERP-0545** (05/20) Specify the negative/authorization case: Reject expired approval or unauthorized price override.
- [ ] **ERP-0546** (06/20) Design data, configuration and numeric BIGINT IDs for Draft/Sent/Approved/Rejected/Expired/Converted states and valid-until; record N/A with evidence if schema unchanged.
- [ ] **ERP-0547** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Expired/rejected quotes cannot silently be approved/converted.
- [ ] **ERP-0548** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Quotation models, totals, approvals and preview endpoint.
- [ ] **ERP-0549** (09/20) Implement or repair Django models/serializers/configuration for Equivalent quotation models, status and serializer rules.
- [ ] **ERP-0550** (10/20) Create/review SQL Server migrations and indexes for Quotation creation, approval and bilingual print; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0551** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Draft/Sent/Approved/Rejected/Expired/Converted states and valid-until.
- [ ] **ERP-0552** (12/20) Implement or repair ASP.NET business operations and idempotency for Quotation creation, approval and bilingual print.
- [ ] **ERP-0553** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Quotation creation, approval and bilingual print.
- [ ] **ERP-0554** (14/20) Enforce role/branch/action permissions and record audit events for Quotation creation, approval and bilingual print; prove server-side denial.
- [ ] **ERP-0555** (15/20) Implement or repair React API integration, screens and user feedback for Quotation form, approval, bilingual preview and print.
- [ ] **ERP-0556** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Quotation creation, approval and bilingual print.
- [ ] **ERP-0557** (17/20) Run/add ASP.NET unit and validation tests for Create bilingual quotation and approve with correct total; fix every failure.
- [ ] **ERP-0558** (18/20) Run/add Django unit and parity tests for Reject expired approval or unauthorized price override; fix every failure.
- [ ] **ERP-0559** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Expired/rejected quotes cannot silently be approved/converted.
- [ ] **ERP-0560** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 29: Quotation-to-invoice conversion — ERP-0561 to ERP-0580
**SRS sections:** 20, 22, 23, 54, 55, 57, 58. **Deliverable:** Atomic conversion preserving quotation reference, items, totals and unique link.
**Dependencies:** packages 28. **Invariant:** One quotation cannot create duplicate invoices.
**Happy-path proof:** Convert approved quote and verify item/reference parity. **Negative proof:** Block double conversion and stale quote price mutation.

- [ ] **ERP-0561** (01/20) Extract Quotation-to-invoice conversion acceptance details from SRS §§20, 22, 23, 54, 55, 57, 58; record assumptions and exclusions.
- [ ] **ERP-0562** (02/20) Inspect Conversion handler with idempotency and transaction, Equivalent atomic conversion and unique relationship and Convert action, confirmation and invoice navigation; record actual files and current behavior.
- [ ] **ERP-0563** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0564** (04/20) Specify the happy-path acceptance: Convert approved quote and verify item/reference parity.
- [ ] **ERP-0565** (05/20) Specify the negative/authorization case: Block double conversion and stale quote price mutation.
- [ ] **ERP-0566** (06/20) Design data, configuration and numeric BIGINT IDs for Atomic conversion preserving quotation reference, items, totals and unique link; record N/A with evidence if schema unchanged.
- [ ] **ERP-0567** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: One quotation cannot create duplicate invoices.
- [ ] **ERP-0568** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Conversion handler with idempotency and transaction.
- [ ] **ERP-0569** (09/20) Implement or repair Django models/serializers/configuration for Equivalent atomic conversion and unique relationship.
- [ ] **ERP-0570** (10/20) Create/review SQL Server migrations and indexes for Quotation-to-invoice conversion; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0571** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Atomic conversion preserving quotation reference, items, totals and unique link.
- [ ] **ERP-0572** (12/20) Implement or repair ASP.NET business operations and idempotency for Quotation-to-invoice conversion.
- [ ] **ERP-0573** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Quotation-to-invoice conversion.
- [ ] **ERP-0574** (14/20) Enforce role/branch/action permissions and record audit events for Quotation-to-invoice conversion; prove server-side denial.
- [ ] **ERP-0575** (15/20) Implement or repair React API integration, screens and user feedback for Convert action, confirmation and invoice navigation.
- [ ] **ERP-0576** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Quotation-to-invoice conversion.
- [ ] **ERP-0577** (17/20) Run/add ASP.NET unit and validation tests for Convert approved quote and verify item/reference parity; fix every failure.
- [ ] **ERP-0578** (18/20) Run/add Django unit and parity tests for Block double conversion and stale quote price mutation; fix every failure.
- [ ] **ERP-0579** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile One quotation cannot create duplicate invoices.
- [ ] **ERP-0580** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 30: Direct Sales Invoice and stock posting — ERP-0581 to ERP-0600
**SRS sections:** 22, 23, 24, 25, 29, 54, 55, 57, 58. **Deliverable:** Direct invoice, cash/credit totals, typed lines and atomic stock decrease.
**Dependencies:** packages 18–22,29. **Invariant:** Posted stock and financial entries are consistent and idempotent.
**Happy-path proof:** Post direct stock sale and see on-hand decrease. **Negative proof:** Reject insufficient stock, invalid serial and duplicate invoice number.

- [ ] **ERP-0581** (01/20) Extract Direct Sales Invoice and stock posting acceptance details from SRS §§22, 23, 24, 25, 29, 54, 55, 57, 58; record assumptions and exclusions.
- [ ] **ERP-0582** (02/20) Inspect Sales invoice models, posting rules and EF transaction, Equivalent invoice models and atomic posting and Invoice editor, draft, payment summary and post UI; record actual files and current behavior.
- [ ] **ERP-0583** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0584** (04/20) Specify the happy-path acceptance: Post direct stock sale and see on-hand decrease.
- [ ] **ERP-0585** (05/20) Specify the negative/authorization case: Reject insufficient stock, invalid serial and duplicate invoice number.
- [ ] **ERP-0586** (06/20) Design data, configuration and numeric BIGINT IDs for Direct invoice, cash/credit totals, typed lines and atomic stock decrease; record N/A with evidence if schema unchanged.
- [ ] **ERP-0587** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Posted stock and financial entries are consistent and idempotent.
- [ ] **ERP-0588** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Sales invoice models, posting rules and EF transaction.
- [ ] **ERP-0589** (09/20) Implement or repair Django models/serializers/configuration for Equivalent invoice models and atomic posting.
- [ ] **ERP-0590** (10/20) Create/review SQL Server migrations and indexes for Direct Sales Invoice and stock posting; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0591** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Direct invoice, cash/credit totals, typed lines and atomic stock decrease.
- [ ] **ERP-0592** (12/20) Implement or repair ASP.NET business operations and idempotency for Direct Sales Invoice and stock posting.
- [ ] **ERP-0593** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Direct Sales Invoice and stock posting.
- [ ] **ERP-0594** (14/20) Enforce role/branch/action permissions and record audit events for Direct Sales Invoice and stock posting; prove server-side denial.
- [ ] **ERP-0595** (15/20) Implement or repair React API integration, screens and user feedback for Invoice editor, draft, payment summary and post UI.
- [ ] **ERP-0596** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Direct Sales Invoice and stock posting.
- [ ] **ERP-0597** (17/20) Run/add ASP.NET unit and validation tests for Post direct stock sale and see on-hand decrease; fix every failure.
- [ ] **ERP-0598** (18/20) Run/add Django unit and parity tests for Reject insufficient stock, invalid serial and duplicate invoice number; fix every failure.
- [ ] **ERP-0599** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Posted stock and financial entries are consistent and idempotent.
- [ ] **ERP-0600** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Phase 7: Payments, receivables, returns and stock counts

### Package 31: Counter POS, cash/credit and credit limits — ERP-0601 to ERP-0620
**SRS sections:** 23, 24, 25, 26, 42, 48, 49, 50, 51. **Deliverable:** Fast scan-to-cart, payment collection, customer limits and credit policy.
**Dependencies:** packages 08,12,18–20,30. **Invariant:** Credit limit checked atomically before posting.
**Happy-path proof:** Cash sale and partial-paid credit sale post correctly. **Negative proof:** Block excess credit or insufficient-stock checkout.

- [ ] **ERP-0601** (01/20) Extract Counter POS, cash/credit and credit limits acceptance details from SRS §§23, 24, 25, 26, 42, 48, 49, 50, 51; record assumptions and exclusions.
- [ ] **ERP-0602** (02/20) Inspect POS pricing/credit checks and payment reconciliation, Equivalent POS/credit policy and invoice API and Scan/cart, KNET/card/cash, balance and limit warning; record actual files and current behavior.
- [ ] **ERP-0603** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0604** (04/20) Specify the happy-path acceptance: Cash sale and partial-paid credit sale post correctly.
- [ ] **ERP-0605** (05/20) Specify the negative/authorization case: Block excess credit or insufficient-stock checkout.
- [ ] **ERP-0606** (06/20) Design data, configuration and numeric BIGINT IDs for Fast scan-to-cart, payment collection, customer limits and credit policy; record N/A with evidence if schema unchanged.
- [ ] **ERP-0607** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Credit limit checked atomically before posting.
- [ ] **ERP-0608** (08/20) Implement or repair ASP.NET entities/configuration/contracts for POS pricing/credit checks and payment reconciliation.
- [ ] **ERP-0609** (09/20) Implement or repair Django models/serializers/configuration for Equivalent POS/credit policy and invoice API.
- [ ] **ERP-0610** (10/20) Create/review SQL Server migrations and indexes for Counter POS, cash/credit and credit limits; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0611** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Fast scan-to-cart, payment collection, customer limits and credit policy.
- [ ] **ERP-0612** (12/20) Implement or repair ASP.NET business operations and idempotency for Counter POS, cash/credit and credit limits.
- [ ] **ERP-0613** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Counter POS, cash/credit and credit limits.
- [ ] **ERP-0614** (14/20) Enforce role/branch/action permissions and record audit events for Counter POS, cash/credit and credit limits; prove server-side denial.
- [ ] **ERP-0615** (15/20) Implement or repair React API integration, screens and user feedback for Scan/cart, KNET/card/cash, balance and limit warning.
- [ ] **ERP-0616** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Counter POS, cash/credit and credit limits.
- [ ] **ERP-0617** (17/20) Run/add ASP.NET unit and validation tests for Cash sale and partial-paid credit sale post correctly; fix every failure.
- [ ] **ERP-0618** (18/20) Run/add Django unit and parity tests for Block excess credit or insufficient-stock checkout; fix every failure.
- [ ] **ERP-0619** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Credit limit checked atomically before posting.
- [ ] **ERP-0620** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 32: Customer receipts and invoice allocations — ERP-0621 to ERP-0640
**SRS sections:** 9, 23, 25, 26, 50, 55, 57. **Deliverable:** Receipt numbers, partial payments, allocations and method metadata.
**Dependencies:** packages 12,19,30–31. **Invariant:** Payment cannot allocate more than available credit or invoice due.
**Happy-path proof:** Receive partial payment and lower outstanding. **Negative proof:** Reject overpayment without allowed credit config.

- [ ] **ERP-0621** (01/20) Extract Customer receipts and invoice allocations acceptance details from SRS §§9, 23, 25, 26, 50, 55, 57; record assumptions and exclusions.
- [ ] **ERP-0622** (02/20) Inspect Receipt, allocation and posting models, Equivalent receipt, allocation and API and Receipt entry, invoice allocation and print; record actual files and current behavior.
- [ ] **ERP-0623** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0624** (04/20) Specify the happy-path acceptance: Receive partial payment and lower outstanding.
- [ ] **ERP-0625** (05/20) Specify the negative/authorization case: Reject overpayment without allowed credit config.
- [ ] **ERP-0626** (06/20) Design data, configuration and numeric BIGINT IDs for Receipt numbers, partial payments, allocations and method metadata; record N/A with evidence if schema unchanged.
- [ ] **ERP-0627** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Payment cannot allocate more than available credit or invoice due.
- [ ] **ERP-0628** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Receipt, allocation and posting models.
- [ ] **ERP-0629** (09/20) Implement or repair Django models/serializers/configuration for Equivalent receipt, allocation and API.
- [ ] **ERP-0630** (10/20) Create/review SQL Server migrations and indexes for Customer receipts and invoice allocations; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0631** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Receipt numbers, partial payments, allocations and method metadata.
- [ ] **ERP-0632** (12/20) Implement or repair ASP.NET business operations and idempotency for Customer receipts and invoice allocations.
- [ ] **ERP-0633** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Customer receipts and invoice allocations.
- [ ] **ERP-0634** (14/20) Enforce role/branch/action permissions and record audit events for Customer receipts and invoice allocations; prove server-side denial.
- [ ] **ERP-0635** (15/20) Implement or repair React API integration, screens and user feedback for Receipt entry, invoice allocation and print.
- [ ] **ERP-0636** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Customer receipts and invoice allocations.
- [ ] **ERP-0637** (17/20) Run/add ASP.NET unit and validation tests for Receive partial payment and lower outstanding; fix every failure.
- [ ] **ERP-0638** (18/20) Run/add Django unit and parity tests for Reject overpayment without allowed credit config; fix every failure.
- [ ] **ERP-0639** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Payment cannot allocate more than available credit or invoice due.
- [ ] **ERP-0640** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 33: Customer ledger, statements and aging — ERP-0641 to ERP-0660
**SRS sections:** 8, 9, 23, 25, 26, 39, 51. **Deliverable:** Debits/credits, balances, due dates, payment history and aging buckets.
**Dependencies:** packages 12,30–32. **Invariant:** Ledger balance reconciles to posted invoice/receipt/credit note.
**Happy-path proof:** Reconcile invoice, receipt and balance for a customer. **Negative proof:** Detect mismatched ledger or unposted document in balance.

- [ ] **ERP-0641** (01/20) Extract Customer ledger, statements and aging acceptance details from SRS §§8, 9, 23, 25, 26, 39, 51; record assumptions and exclusions.
- [ ] **ERP-0642** (02/20) Inspect Customer ledger projections and statement endpoints, Equivalent ledger/aging queries and pagination and Ledger, aging filter, customer statement; record actual files and current behavior.
- [ ] **ERP-0643** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0644** (04/20) Specify the happy-path acceptance: Reconcile invoice, receipt and balance for a customer.
- [ ] **ERP-0645** (05/20) Specify the negative/authorization case: Detect mismatched ledger or unposted document in balance.
- [ ] **ERP-0646** (06/20) Design data, configuration and numeric BIGINT IDs for Debits/credits, balances, due dates, payment history and aging buckets; record N/A with evidence if schema unchanged.
- [ ] **ERP-0647** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Ledger balance reconciles to posted invoice/receipt/credit note.
- [ ] **ERP-0648** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Customer ledger projections and statement endpoints.
- [ ] **ERP-0649** (09/20) Implement or repair Django models/serializers/configuration for Equivalent ledger/aging queries and pagination.
- [ ] **ERP-0650** (10/20) Create/review SQL Server migrations and indexes for Customer ledger, statements and aging; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0651** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Debits/credits, balances, due dates, payment history and aging buckets.
- [ ] **ERP-0652** (12/20) Implement or repair ASP.NET business operations and idempotency for Customer ledger, statements and aging.
- [ ] **ERP-0653** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Customer ledger, statements and aging.
- [ ] **ERP-0654** (14/20) Enforce role/branch/action permissions and record audit events for Customer ledger, statements and aging; prove server-side denial.
- [ ] **ERP-0655** (15/20) Implement or repair React API integration, screens and user feedback for Ledger, aging filter, customer statement.
- [ ] **ERP-0656** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Customer ledger, statements and aging.
- [ ] **ERP-0657** (17/20) Run/add ASP.NET unit and validation tests for Reconcile invoice, receipt and balance for a customer; fix every failure.
- [ ] **ERP-0658** (18/20) Run/add Django unit and parity tests for Detect mismatched ledger or unposted document in balance; fix every failure.
- [ ] **ERP-0659** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Ledger balance reconciles to posted invoice/receipt/credit note.
- [ ] **ERP-0660** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 34: Sales Return, Credit Note and refund — ERP-0661 to ERP-0680
**SRS sections:** 9, 27, 29, 55, 57, 58. **Deliverable:** Original invoice, return quantities, serialized stock-in and refund/credit.
**Dependencies:** packages 22,30–33. **Invariant:** Cannot return more than originally sold; audit survives reversal.
**Happy-path proof:** Return sold item, increase stock and reduce receivable. **Negative proof:** Reject second return of same serial and unapproved refund.

- [ ] **ERP-0661** (01/20) Extract Sales Return, Credit Note and refund acceptance details from SRS §§9, 27, 29, 55, 57, 58; record assumptions and exclusions.
- [ ] **ERP-0662** (02/20) Inspect Credit note transaction and serial/stock reversal handlers, Equivalent return, refund and idempotency APIs and Credit note form, refund and adjustment selector; record actual files and current behavior.
- [ ] **ERP-0663** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0664** (04/20) Specify the happy-path acceptance: Return sold item, increase stock and reduce receivable.
- [ ] **ERP-0665** (05/20) Specify the negative/authorization case: Reject second return of same serial and unapproved refund.
- [ ] **ERP-0666** (06/20) Design data, configuration and numeric BIGINT IDs for Original invoice, return quantities, serialized stock-in and refund/credit; record N/A with evidence if schema unchanged.
- [ ] **ERP-0667** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Cannot return more than originally sold; audit survives reversal.
- [ ] **ERP-0668** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Credit note transaction and serial/stock reversal handlers.
- [ ] **ERP-0669** (09/20) Implement or repair Django models/serializers/configuration for Equivalent return, refund and idempotency APIs.
- [ ] **ERP-0670** (10/20) Create/review SQL Server migrations and indexes for Sales Return, Credit Note and refund; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0671** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Original invoice, return quantities, serialized stock-in and refund/credit.
- [ ] **ERP-0672** (12/20) Implement or repair ASP.NET business operations and idempotency for Sales Return, Credit Note and refund.
- [ ] **ERP-0673** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Sales Return, Credit Note and refund.
- [ ] **ERP-0674** (14/20) Enforce role/branch/action permissions and record audit events for Sales Return, Credit Note and refund; prove server-side denial.
- [ ] **ERP-0675** (15/20) Implement or repair React API integration, screens and user feedback for Credit note form, refund and adjustment selector.
- [ ] **ERP-0676** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Sales Return, Credit Note and refund.
- [ ] **ERP-0677** (17/20) Run/add ASP.NET unit and validation tests for Return sold item, increase stock and reduce receivable; fix every failure.
- [ ] **ERP-0678** (18/20) Run/add Django unit and parity tests for Reject second return of same serial and unapproved refund; fix every failure.
- [ ] **ERP-0679** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Cannot return more than originally sold; audit survives reversal.
- [ ] **ERP-0680** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 35: Adjustments and physical stock count — ERP-0681 to ERP-0700
**SRS sections:** 29, 30, 32, 57, 58. **Deliverable:** Authorized adjustment reasons, count sheet, variance and approval.
**Dependencies:** packages 06–09,21–22. **Invariant:** Counts retain snapshot and stock is changed only after approval.
**Happy-path proof:** Count 9 vs 10 and post approved -1 adjustment. **Negative proof:** Block unauthorized adjustment and duplicate approval.

- [ ] **ERP-0681** (01/20) Extract Adjustments and physical stock count acceptance details from SRS §§29, 30, 32, 57, 58; record assumptions and exclusions.
- [ ] **ERP-0682** (02/20) Inspect Count/adjustment entities, approval and stock movements, Equivalent count/adjustment and posting APIs and Count sheet, variance review and adjustment screen; record actual files and current behavior.
- [ ] **ERP-0683** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0684** (04/20) Specify the happy-path acceptance: Count 9 vs 10 and post approved -1 adjustment.
- [ ] **ERP-0685** (05/20) Specify the negative/authorization case: Block unauthorized adjustment and duplicate approval.
- [ ] **ERP-0686** (06/20) Design data, configuration and numeric BIGINT IDs for Authorized adjustment reasons, count sheet, variance and approval; record N/A with evidence if schema unchanged.
- [ ] **ERP-0687** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Counts retain snapshot and stock is changed only after approval.
- [ ] **ERP-0688** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Count/adjustment entities, approval and stock movements.
- [ ] **ERP-0689** (09/20) Implement or repair Django models/serializers/configuration for Equivalent count/adjustment and posting APIs.
- [ ] **ERP-0690** (10/20) Create/review SQL Server migrations and indexes for Adjustments and physical stock count; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0691** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Authorized adjustment reasons, count sheet, variance and approval.
- [ ] **ERP-0692** (12/20) Implement or repair ASP.NET business operations and idempotency for Adjustments and physical stock count.
- [ ] **ERP-0693** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Adjustments and physical stock count.
- [ ] **ERP-0694** (14/20) Enforce role/branch/action permissions and record audit events for Adjustments and physical stock count; prove server-side denial.
- [ ] **ERP-0695** (15/20) Implement or repair React API integration, screens and user feedback for Count sheet, variance review and adjustment screen.
- [ ] **ERP-0696** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Adjustments and physical stock count.
- [ ] **ERP-0697** (17/20) Run/add ASP.NET unit and validation tests for Count 9 vs 10 and post approved -1 adjustment; fix every failure.
- [ ] **ERP-0698** (18/20) Run/add Django unit and parity tests for Block unauthorized adjustment and duplicate approval; fix every failure.
- [ ] **ERP-0699** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Counts retain snapshot and stock is changed only after approval.
- [ ] **ERP-0700** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Phase 8: Warehousing, costing, service and management

### Package 36: Multi-warehouse transfers and branch isolation — ERP-0701 to ERP-0720
**SRS sections:** 29, 31, 46, 47, 57. **Deliverable:** Warehouse balances, transfer lifecycle and matching stock out/in.
**Dependencies:** packages 09,21–22,35. **Invariant:** Total stock conserved by transfer and cross-branch access denied.
**Happy-path proof:** Transfer an item and serial between warehouses. **Negative proof:** Reject same-source destination and double receiving.

- [ ] **ERP-0701** (01/20) Extract Multi-warehouse transfers and branch isolation acceptance details from SRS §§29, 31, 46, 47, 57; record assumptions and exclusions.
- [ ] **ERP-0702** (02/20) Inspect Transfer/warehouse scoped transactions and serial movement, Equivalent transfer transactions and scoped queries and Warehouse balance and transfer request/receive UI; record actual files and current behavior.
- [ ] **ERP-0703** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0704** (04/20) Specify the happy-path acceptance: Transfer an item and serial between warehouses.
- [ ] **ERP-0705** (05/20) Specify the negative/authorization case: Reject same-source destination and double receiving.
- [ ] **ERP-0706** (06/20) Design data, configuration and numeric BIGINT IDs for Warehouse balances, transfer lifecycle and matching stock out/in; record N/A with evidence if schema unchanged.
- [ ] **ERP-0707** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Total stock conserved by transfer and cross-branch access denied.
- [ ] **ERP-0708** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Transfer/warehouse scoped transactions and serial movement.
- [ ] **ERP-0709** (09/20) Implement or repair Django models/serializers/configuration for Equivalent transfer transactions and scoped queries.
- [ ] **ERP-0710** (10/20) Create/review SQL Server migrations and indexes for Multi-warehouse transfers and branch isolation; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0711** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Warehouse balances, transfer lifecycle and matching stock out/in.
- [ ] **ERP-0712** (12/20) Implement or repair ASP.NET business operations and idempotency for Multi-warehouse transfers and branch isolation.
- [ ] **ERP-0713** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Multi-warehouse transfers and branch isolation.
- [ ] **ERP-0714** (14/20) Enforce role/branch/action permissions and record audit events for Multi-warehouse transfers and branch isolation; prove server-side denial.
- [ ] **ERP-0715** (15/20) Implement or repair React API integration, screens and user feedback for Warehouse balance and transfer request/receive UI.
- [ ] **ERP-0716** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Multi-warehouse transfers and branch isolation.
- [ ] **ERP-0717** (17/20) Run/add ASP.NET unit and validation tests for Transfer an item and serial between warehouses; fix every failure.
- [ ] **ERP-0718** (18/20) Run/add Django unit and parity tests for Reject same-source destination and double receiving; fix every failure.
- [ ] **ERP-0719** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Total stock conserved by transfer and cross-branch access denied.
- [ ] **ERP-0720** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 37: Stock valuation and gross profit — ERP-0721 to ERP-0740
**SRS sections:** 12, 18, 29, 34, 35, 39, 57. **Deliverable:** Configured costing method, cost snapshots, return-adjusted margin.
**Dependencies:** packages 18,21,25–26,30,34–36. **Invariant:** Cost method agreed before posting and returns reverse correct cost.
**Happy-path proof:** Reconcile stock value and sale gross profit. **Negative proof:** Catch inconsistent cost layers and negative margin override.

- [ ] **ERP-0721** (01/20) Extract Stock valuation and gross profit acceptance details from SRS §§12, 18, 29, 34, 35, 39, 57; record assumptions and exclusions.
- [ ] **ERP-0722** (02/20) Inspect Valuation read models and cost calculations, Equivalent costing algorithms and report queries and Inventory valuation and margin analysis; record actual files and current behavior.
- [ ] **ERP-0723** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0724** (04/20) Specify the happy-path acceptance: Reconcile stock value and sale gross profit.
- [ ] **ERP-0725** (05/20) Specify the negative/authorization case: Catch inconsistent cost layers and negative margin override.
- [ ] **ERP-0726** (06/20) Design data, configuration and numeric BIGINT IDs for Configured costing method, cost snapshots, return-adjusted margin; record N/A with evidence if schema unchanged.
- [ ] **ERP-0727** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Cost method agreed before posting and returns reverse correct cost.
- [ ] **ERP-0728** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Valuation read models and cost calculations.
- [ ] **ERP-0729** (09/20) Implement or repair Django models/serializers/configuration for Equivalent costing algorithms and report queries.
- [ ] **ERP-0730** (10/20) Create/review SQL Server migrations and indexes for Stock valuation and gross profit; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0731** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Configured costing method, cost snapshots, return-adjusted margin.
- [ ] **ERP-0732** (12/20) Implement or repair ASP.NET business operations and idempotency for Stock valuation and gross profit.
- [ ] **ERP-0733** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Stock valuation and gross profit.
- [ ] **ERP-0734** (14/20) Enforce role/branch/action permissions and record audit events for Stock valuation and gross profit; prove server-side denial.
- [ ] **ERP-0735** (15/20) Implement or repair React API integration, screens and user feedback for Inventory valuation and margin analysis.
- [ ] **ERP-0736** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Stock valuation and gross profit.
- [ ] **ERP-0737** (17/20) Run/add ASP.NET unit and validation tests for Reconcile stock value and sale gross profit; fix every failure.
- [ ] **ERP-0738** (18/20) Run/add Django unit and parity tests for Catch inconsistent cost layers and negative margin override; fix every failure.
- [ ] **ERP-0739** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Cost method agreed before posting and returns reverse correct cost.
- [ ] **ERP-0740** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 38: Service job cards and technician workflow — ERP-0741 to ERP-0760
**SRS sections:** 13, 16, 36, 37, 53, 54, 55, 58. **Deliverable:** Customer device intake, serial, complaint, accessories, technician and status.
**Dependencies:** packages 08,12,22–23. **Invariant:** Delivered jobs require authorized completion and captured customer handoff.
**Happy-path proof:** Receive device, diagnose, repair, mark ready and deliver. **Negative proof:** Reject illegal status transition and unauthorized reassignment.

- [ ] **ERP-0741** (01/20) Extract Service job cards and technician workflow acceptance details from SRS §§13, 16, 36, 37, 53, 54, 55, 58; record assumptions and exclusions.
- [ ] **ERP-0742** (02/20) Inspect JobCard entity, workflow transitions and assignments, Equivalent job-card models and API lifecycle and Job-card intake, queue, technician and delivery screens; record actual files and current behavior.
- [ ] **ERP-0743** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0744** (04/20) Specify the happy-path acceptance: Receive device, diagnose, repair, mark ready and deliver.
- [ ] **ERP-0745** (05/20) Specify the negative/authorization case: Reject illegal status transition and unauthorized reassignment.
- [ ] **ERP-0746** (06/20) Design data, configuration and numeric BIGINT IDs for Customer device intake, serial, complaint, accessories, technician and status; record N/A with evidence if schema unchanged.
- [ ] **ERP-0747** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Delivered jobs require authorized completion and captured customer handoff.
- [ ] **ERP-0748** (08/20) Implement or repair ASP.NET entities/configuration/contracts for JobCard entity, workflow transitions and assignments.
- [ ] **ERP-0749** (09/20) Implement or repair Django models/serializers/configuration for Equivalent job-card models and API lifecycle.
- [ ] **ERP-0750** (10/20) Create/review SQL Server migrations and indexes for Service job cards and technician workflow; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0751** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Customer device intake, serial, complaint, accessories, technician and status.
- [ ] **ERP-0752** (12/20) Implement or repair ASP.NET business operations and idempotency for Service job cards and technician workflow.
- [ ] **ERP-0753** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Service job cards and technician workflow.
- [ ] **ERP-0754** (14/20) Enforce role/branch/action permissions and record audit events for Service job cards and technician workflow; prove server-side denial.
- [ ] **ERP-0755** (15/20) Implement or repair React API integration, screens and user feedback for Job-card intake, queue, technician and delivery screens.
- [ ] **ERP-0756** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Service job cards and technician workflow.
- [ ] **ERP-0757** (17/20) Run/add ASP.NET unit and validation tests for Receive device, diagnose, repair, mark ready and deliver; fix every failure.
- [ ] **ERP-0758** (18/20) Run/add Django unit and parity tests for Reject illegal status transition and unauthorized reassignment; fix every failure.
- [ ] **ERP-0759** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Delivered jobs require authorized completion and captured customer handoff.
- [ ] **ERP-0760** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 39: Service billing and warranty repair — ERP-0761 to ERP-0780
**SRS sections:** 16, 23, 35, 36, 37, 55, 57. **Deliverable:** Parts usage, service charges, warranty decisions, invoice and service margin.
**Dependencies:** packages 23,30,37–38. **Invariant:** Parts consume stock once; warranty service cannot bill covered labor incorrectly.
**Happy-path proof:** Use one replacement part then issue service invoice. **Negative proof:** Reject duplicate parts consumption or out-of-warranty free service.

- [ ] **ERP-0761** (01/20) Extract Service billing and warranty repair acceptance details from SRS §§16, 23, 35, 36, 37, 55, 57; record assumptions and exclusions.
- [ ] **ERP-0762** (02/20) Inspect Repair labor/parts and service invoice integration, Equivalent parts consumption, service invoice and warranty API and Repair estimate, consumed parts, billing and warranty view; record actual files and current behavior.
- [ ] **ERP-0763** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0764** (04/20) Specify the happy-path acceptance: Use one replacement part then issue service invoice.
- [ ] **ERP-0765** (05/20) Specify the negative/authorization case: Reject duplicate parts consumption or out-of-warranty free service.
- [ ] **ERP-0766** (06/20) Design data, configuration and numeric BIGINT IDs for Parts usage, service charges, warranty decisions, invoice and service margin; record N/A with evidence if schema unchanged.
- [ ] **ERP-0767** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Parts consume stock once; warranty service cannot bill covered labor incorrectly.
- [ ] **ERP-0768** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Repair labor/parts and service invoice integration.
- [ ] **ERP-0769** (09/20) Implement or repair Django models/serializers/configuration for Equivalent parts consumption, service invoice and warranty API.
- [ ] **ERP-0770** (10/20) Create/review SQL Server migrations and indexes for Service billing and warranty repair; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0771** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Parts usage, service charges, warranty decisions, invoice and service margin.
- [ ] **ERP-0772** (12/20) Implement or repair ASP.NET business operations and idempotency for Service billing and warranty repair.
- [ ] **ERP-0773** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Service billing and warranty repair.
- [ ] **ERP-0774** (14/20) Enforce role/branch/action permissions and record audit events for Service billing and warranty repair; prove server-side denial.
- [ ] **ERP-0775** (15/20) Implement or repair React API integration, screens and user feedback for Repair estimate, consumed parts, billing and warranty view.
- [ ] **ERP-0776** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Service billing and warranty repair.
- [ ] **ERP-0777** (17/20) Run/add ASP.NET unit and validation tests for Use one replacement part then issue service invoice; fix every failure.
- [ ] **ERP-0778** (18/20) Run/add Django unit and parity tests for Reject duplicate parts consumption or out-of-warranty free service; fix every failure.
- [ ] **ERP-0779** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Parts consume stock once; warranty service cannot bill covered labor incorrectly.
- [ ] **ERP-0780** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 40: Dashboard, low stock and notifications — ERP-0781 to ERP-0800
**SRS sections:** 9, 11, 16, 33, 38, 53, 68. **Deliverable:** Sales/purchases/receivables/stock/quotation/job KPIs and actionable alerts.
**Dependencies:** packages 09,21,25–39. **Invariant:** All KPIs reconcile with posted transactions; no unrestricted cross-branch totals.
**Happy-path proof:** Show low-stock item and current overdue receivable. **Negative proof:** Catch stale aggregation and unauthorized KPI visibility.

- [ ] **ERP-0781** (01/20) Extract Dashboard, low stock and notifications acceptance details from SRS §§9, 11, 16, 33, 38, 53, 68; record assumptions and exclusions.
- [ ] **ERP-0782** (02/20) Inspect Aggregated filtered endpoints and notification rules, Equivalent KPIs and alert query APIs and Dashboard cards, low-stock list and alert panels; record actual files and current behavior.
- [ ] **ERP-0783** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0784** (04/20) Specify the happy-path acceptance: Show low-stock item and current overdue receivable.
- [ ] **ERP-0785** (05/20) Specify the negative/authorization case: Catch stale aggregation and unauthorized KPI visibility.
- [ ] **ERP-0786** (06/20) Design data, configuration and numeric BIGINT IDs for Sales/purchases/receivables/stock/quotation/job KPIs and actionable alerts; record N/A with evidence if schema unchanged.
- [ ] **ERP-0787** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: All KPIs reconcile with posted transactions; no unrestricted cross-branch totals.
- [ ] **ERP-0788** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Aggregated filtered endpoints and notification rules.
- [ ] **ERP-0789** (09/20) Implement or repair Django models/serializers/configuration for Equivalent KPIs and alert query APIs.
- [ ] **ERP-0790** (10/20) Create/review SQL Server migrations and indexes for Dashboard, low stock and notifications; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0791** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Sales/purchases/receivables/stock/quotation/job KPIs and actionable alerts.
- [ ] **ERP-0792** (12/20) Implement or repair ASP.NET business operations and idempotency for Dashboard, low stock and notifications.
- [ ] **ERP-0793** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Dashboard, low stock and notifications.
- [ ] **ERP-0794** (14/20) Enforce role/branch/action permissions and record audit events for Dashboard, low stock and notifications; prove server-side denial.
- [ ] **ERP-0795** (15/20) Implement or repair React API integration, screens and user feedback for Dashboard cards, low-stock list and alert panels.
- [ ] **ERP-0796** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Dashboard, low stock and notifications.
- [ ] **ERP-0797** (17/20) Run/add ASP.NET unit and validation tests for Show low-stock item and current overdue receivable; fix every failure.
- [ ] **ERP-0798** (18/20) Run/add Django unit and parity tests for Catch stale aggregation and unauthorized KPI visibility; fix every failure.
- [ ] **ERP-0799** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile All KPIs reconcile with posted transactions; no unrestricted cross-branch totals.
- [ ] **ERP-0800** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Phase 9: Reporting, printing and search

### Package 41: Sales, purchase, discount and tax reports — ERP-0801 to ERP-0820
**SRS sections:** 28, 35, 38, 39, 44, 68. **Deliverable:** Date/customer/product/category/brand/salesperson filtered sales and purchase datasets.
**Dependencies:** packages 25–34,37,40. **Invariant:** Reports exclude drafts and return consistent period totals.
**Happy-path proof:** Reconcile monthly sales and purchase figures. **Negative proof:** Catch duplicate join rows and unauthorized export.

- [ ] **ERP-0801** (01/20) Extract Sales, purchase, discount and tax reports acceptance details from SRS §§28, 35, 38, 39, 44, 68; record assumptions and exclusions.
- [ ] **ERP-0802** (02/20) Inspect Parameterized, paged sales/purchase reporting endpoints, Equivalent aggregates, filters and report responses and Report filter panel, totals and export action; record actual files and current behavior.
- [ ] **ERP-0803** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0804** (04/20) Specify the happy-path acceptance: Reconcile monthly sales and purchase figures.
- [ ] **ERP-0805** (05/20) Specify the negative/authorization case: Catch duplicate join rows and unauthorized export.
- [ ] **ERP-0806** (06/20) Design data, configuration and numeric BIGINT IDs for Date/customer/product/category/brand/salesperson filtered sales and purchase datasets; record N/A with evidence if schema unchanged.
- [ ] **ERP-0807** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Reports exclude drafts and return consistent period totals.
- [ ] **ERP-0808** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Parameterized, paged sales/purchase reporting endpoints.
- [ ] **ERP-0809** (09/20) Implement or repair Django models/serializers/configuration for Equivalent aggregates, filters and report responses.
- [ ] **ERP-0810** (10/20) Create/review SQL Server migrations and indexes for Sales, purchase, discount and tax reports; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0811** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Date/customer/product/category/brand/salesperson filtered sales and purchase datasets.
- [ ] **ERP-0812** (12/20) Implement or repair ASP.NET business operations and idempotency for Sales, purchase, discount and tax reports.
- [ ] **ERP-0813** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Sales, purchase, discount and tax reports.
- [ ] **ERP-0814** (14/20) Enforce role/branch/action permissions and record audit events for Sales, purchase, discount and tax reports; prove server-side denial.
- [ ] **ERP-0815** (15/20) Implement or repair React API integration, screens and user feedback for Report filter panel, totals and export action.
- [ ] **ERP-0816** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Sales, purchase, discount and tax reports.
- [ ] **ERP-0817** (17/20) Run/add ASP.NET unit and validation tests for Reconcile monthly sales and purchase figures; fix every failure.
- [ ] **ERP-0818** (18/20) Run/add Django unit and parity tests for Catch duplicate join rows and unauthorized export; fix every failure.
- [ ] **ERP-0819** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Reports exclude drafts and return consistent period totals.
- [ ] **ERP-0820** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 42: Inventory, serial and warranty reports — ERP-0821 to ERP-0840
**SRS sections:** 15, 16, 29, 32, 33, 34, 39, 43, 68. **Deliverable:** Current stock, movements, valuation, counts, serial provenance and warranty.
**Dependencies:** packages 21–23,35–37,40. **Invariant:** All stock reports reconcile with underlying movements.
**Happy-path proof:** Trace one serial from supplier through customer warranty. **Negative proof:** Detect missing movement, duplicate serial and valuation drift.

- [ ] **ERP-0821** (01/20) Extract Inventory, serial and warranty reports acceptance details from SRS §§15, 16, 29, 32, 33, 34, 39, 43, 68; record assumptions and exclusions.
- [ ] **ERP-0822** (02/20) Inspect Stock, serial and warranty paged report queries, Equivalent filter, balance and provenance queries and Stock report tables and history drilldowns; record actual files and current behavior.
- [ ] **ERP-0823** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0824** (04/20) Specify the happy-path acceptance: Trace one serial from supplier through customer warranty.
- [ ] **ERP-0825** (05/20) Specify the negative/authorization case: Detect missing movement, duplicate serial and valuation drift.
- [ ] **ERP-0826** (06/20) Design data, configuration and numeric BIGINT IDs for Current stock, movements, valuation, counts, serial provenance and warranty; record N/A with evidence if schema unchanged.
- [ ] **ERP-0827** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: All stock reports reconcile with underlying movements.
- [ ] **ERP-0828** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Stock, serial and warranty paged report queries.
- [ ] **ERP-0829** (09/20) Implement or repair Django models/serializers/configuration for Equivalent filter, balance and provenance queries.
- [ ] **ERP-0830** (10/20) Create/review SQL Server migrations and indexes for Inventory, serial and warranty reports; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0831** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Current stock, movements, valuation, counts, serial provenance and warranty.
- [ ] **ERP-0832** (12/20) Implement or repair ASP.NET business operations and idempotency for Inventory, serial and warranty reports.
- [ ] **ERP-0833** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Inventory, serial and warranty reports.
- [ ] **ERP-0834** (14/20) Enforce role/branch/action permissions and record audit events for Inventory, serial and warranty reports; prove server-side denial.
- [ ] **ERP-0835** (15/20) Implement or repair React API integration, screens and user feedback for Stock report tables and history drilldowns.
- [ ] **ERP-0836** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Inventory, serial and warranty reports.
- [ ] **ERP-0837** (17/20) Run/add ASP.NET unit and validation tests for Trace one serial from supplier through customer warranty; fix every failure.
- [ ] **ERP-0838** (18/20) Run/add Django unit and parity tests for Detect missing movement, duplicate serial and valuation drift; fix every failure.
- [ ] **ERP-0839** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile All stock reports reconcile with underlying movements.
- [ ] **ERP-0840** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 43: Customer, supplier, quotation, service reports — ERP-0841 to ERP-0860
**SRS sections:** 9, 11, 20, 37, 39, 44, 68. **Deliverable:** Statements, aging, outstanding, conversion and repair performance datasets.
**Dependencies:** packages 27–29,32–33,38–40. **Invariant:** Opening+debits-credits equals closing; conversion counts consistent.
**Happy-path proof:** Print customer statement and quotation conversion report. **Negative proof:** Catch report leaked branch data or inconsistent aging buckets.

- [ ] **ERP-0841** (01/20) Extract Customer, supplier, quotation, service reports acceptance details from SRS §§9, 11, 20, 37, 39, 44, 68; record assumptions and exclusions.
- [ ] **ERP-0842** (02/20) Inspect Customer/supplier/quotation/service read models, Equivalent report aggregations and ledger joins and Report selection, drilldown, date/status filters; record actual files and current behavior.
- [ ] **ERP-0843** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0844** (04/20) Specify the happy-path acceptance: Print customer statement and quotation conversion report.
- [ ] **ERP-0845** (05/20) Specify the negative/authorization case: Catch report leaked branch data or inconsistent aging buckets.
- [ ] **ERP-0846** (06/20) Design data, configuration and numeric BIGINT IDs for Statements, aging, outstanding, conversion and repair performance datasets; record N/A with evidence if schema unchanged.
- [ ] **ERP-0847** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Opening+debits-credits equals closing; conversion counts consistent.
- [ ] **ERP-0848** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Customer/supplier/quotation/service read models.
- [ ] **ERP-0849** (09/20) Implement or repair Django models/serializers/configuration for Equivalent report aggregations and ledger joins.
- [ ] **ERP-0850** (10/20) Create/review SQL Server migrations and indexes for Customer, supplier, quotation, service reports; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0851** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Statements, aging, outstanding, conversion and repair performance datasets.
- [ ] **ERP-0852** (12/20) Implement or repair ASP.NET business operations and idempotency for Customer, supplier, quotation, service reports.
- [ ] **ERP-0853** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Customer, supplier, quotation, service reports.
- [ ] **ERP-0854** (14/20) Enforce role/branch/action permissions and record audit events for Customer, supplier, quotation, service reports; prove server-side denial.
- [ ] **ERP-0855** (15/20) Implement or repair React API integration, screens and user feedback for Report selection, drilldown, date/status filters.
- [ ] **ERP-0856** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Customer, supplier, quotation, service reports.
- [ ] **ERP-0857** (17/20) Run/add ASP.NET unit and validation tests for Print customer statement and quotation conversion report; fix every failure.
- [ ] **ERP-0858** (18/20) Run/add Django unit and parity tests for Catch report leaked branch data or inconsistent aging buckets; fix every failure.
- [ ] **ERP-0859** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Opening+debits-credits equals closing; conversion counts consistent.
- [ ] **ERP-0860** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 44: Bilingual document printing and data exports — ERP-0861 to ERP-0880
**SRS sections:** 3, 5, 21, 40, 41, 44, 63, 65. **Deliverable:** A4/A5/thermal layouts for all SRS documents, plus PDF/Excel/CSV.
**Dependencies:** packages 10–11,18,24–34,38–43. **Invariant:** Printed totals match saved totals and logo/RTL render correctly.
**Happy-path proof:** Print bilingual invoice and exported statement. **Negative proof:** Reject wrong currency rounding, missing Arabic glyphs or oversized layout.

- [ ] **ERP-0861** (01/20) Extract Bilingual document printing and data exports acceptance details from SRS §§3, 5, 21, 40, 41, 44, 63, 65; record assumptions and exclusions.
- [ ] **ERP-0862** (02/20) Inspect Server-side data shapes, print/export authorization, Equivalent document payloads and export endpoints and English/Arabic/bilingual print templates, RTL and download UI; record actual files and current behavior.
- [ ] **ERP-0863** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0864** (04/20) Specify the happy-path acceptance: Print bilingual invoice and exported statement.
- [ ] **ERP-0865** (05/20) Specify the negative/authorization case: Reject wrong currency rounding, missing Arabic glyphs or oversized layout.
- [ ] **ERP-0866** (06/20) Design data, configuration and numeric BIGINT IDs for A4/A5/thermal layouts for all SRS documents, plus PDF/Excel/CSV; record N/A with evidence if schema unchanged.
- [ ] **ERP-0867** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Printed totals match saved totals and logo/RTL render correctly.
- [ ] **ERP-0868** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Server-side data shapes, print/export authorization.
- [ ] **ERP-0869** (09/20) Implement or repair Django models/serializers/configuration for Equivalent document payloads and export endpoints.
- [ ] **ERP-0870** (10/20) Create/review SQL Server migrations and indexes for Bilingual document printing and data exports; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0871** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for A4/A5/thermal layouts for all SRS documents, plus PDF/Excel/CSV.
- [ ] **ERP-0872** (12/20) Implement or repair ASP.NET business operations and idempotency for Bilingual document printing and data exports.
- [ ] **ERP-0873** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Bilingual document printing and data exports.
- [ ] **ERP-0874** (14/20) Enforce role/branch/action permissions and record audit events for Bilingual document printing and data exports; prove server-side denial.
- [ ] **ERP-0875** (15/20) Implement or repair React API integration, screens and user feedback for English/Arabic/bilingual print templates, RTL and download UI.
- [ ] **ERP-0876** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Bilingual document printing and data exports.
- [ ] **ERP-0877** (17/20) Run/add ASP.NET unit and validation tests for Print bilingual invoice and exported statement; fix every failure.
- [ ] **ERP-0878** (18/20) Run/add Django unit and parity tests for Reject wrong currency rounding, missing Arabic glyphs or oversized layout; fix every failure.
- [ ] **ERP-0879** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Printed totals match saved totals and logo/RTL render correctly.
- [ ] **ERP-0880** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 45: Barcode workflows and global search — ERP-0881 to ERP-0900
**SRS sections:** 12, 15, 42, 43, 62. **Deliverable:** Scanner item lookup, optional label generation, indexed global reference search.
**Dependencies:** packages 09,16,21–22,30–31. **Invariant:** Exact barcode/serial lookup resolves one authorized record.
**Happy-path proof:** Scan SKU then add valid item to sale. **Negative proof:** Reject ambiguous barcode and cross-branch search leaks.

- [ ] **ERP-0881** (01/20) Extract Barcode workflows and global search acceptance details from SRS §§12, 15, 42, 43, 62; record assumptions and exclusions.
- [ ] **ERP-0882** (02/20) Inspect Barcode and cross-entity search endpoints, indexes, Equivalent search ranking, limits and barcode routes and Scan-to-POS, global search and serial-history navigation; record actual files and current behavior.
- [ ] **ERP-0883** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0884** (04/20) Specify the happy-path acceptance: Scan SKU then add valid item to sale.
- [ ] **ERP-0885** (05/20) Specify the negative/authorization case: Reject ambiguous barcode and cross-branch search leaks.
- [ ] **ERP-0886** (06/20) Design data, configuration and numeric BIGINT IDs for Scanner item lookup, optional label generation, indexed global reference search; record N/A with evidence if schema unchanged.
- [ ] **ERP-0887** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Exact barcode/serial lookup resolves one authorized record.
- [ ] **ERP-0888** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Barcode and cross-entity search endpoints, indexes.
- [ ] **ERP-0889** (09/20) Implement or repair Django models/serializers/configuration for Equivalent search ranking, limits and barcode routes.
- [ ] **ERP-0890** (10/20) Create/review SQL Server migrations and indexes for Barcode workflows and global search; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0891** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Scanner item lookup, optional label generation, indexed global reference search.
- [ ] **ERP-0892** (12/20) Implement or repair ASP.NET business operations and idempotency for Barcode workflows and global search.
- [ ] **ERP-0893** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Barcode workflows and global search.
- [ ] **ERP-0894** (14/20) Enforce role/branch/action permissions and record audit events for Barcode workflows and global search; prove server-side denial.
- [ ] **ERP-0895** (15/20) Implement or repair React API integration, screens and user feedback for Scan-to-POS, global search and serial-history navigation.
- [ ] **ERP-0896** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Barcode workflows and global search.
- [ ] **ERP-0897** (17/20) Run/add ASP.NET unit and validation tests for Scan SKU then add valid item to sale; fix every failure.
- [ ] **ERP-0898** (18/20) Run/add Django unit and parity tests for Reject ambiguous barcode and cross-branch search leaks; fix every failure.
- [ ] **ERP-0899** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Exact barcode/serial lookup resolves one authorized record.
- [ ] **ERP-0900** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Phase 10: Security, operations, acceptance and release

### Package 46: Security, audit trail and protected attachments — ERP-0901 to ERP-0920
**SRS sections:** 7, 27, 52, 57, 58, 59, 63, 65. **Deliverable:** Immutable audit events, restricted operations, safe files and session controls.
**Dependencies:** packages 05–10,12–13,21–45. **Invariant:** Posted financial events remain traceable; no secret/file leaks.
**Happy-path proof:** Audit author, before/after and reason for approved reversal. **Negative proof:** Deny tampered upload, missing permission and audit deletion.

- [ ] **ERP-0901** (01/20) Extract Security, audit trail and protected attachments acceptance details from SRS §§7, 27, 52, 57, 58, 59, 63, 65; record assumptions and exclusions.
- [ ] **ERP-0902** (02/20) Inspect ASP.NET audit interceptors, secure files and role enforcement, Django audit hooks, access checks and protected media and Permission-aware UI and audit viewer; record actual files and current behavior.
- [ ] **ERP-0903** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0904** (04/20) Specify the happy-path acceptance: Audit author, before/after and reason for approved reversal.
- [ ] **ERP-0905** (05/20) Specify the negative/authorization case: Deny tampered upload, missing permission and audit deletion.
- [ ] **ERP-0906** (06/20) Design data, configuration and numeric BIGINT IDs for Immutable audit events, restricted operations, safe files and session controls; record N/A with evidence if schema unchanged.
- [ ] **ERP-0907** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Posted financial events remain traceable; no secret/file leaks.
- [ ] **ERP-0908** (08/20) Implement or repair ASP.NET entities/configuration/contracts for ASP.NET audit interceptors, secure files and role enforcement.
- [ ] **ERP-0909** (09/20) Implement or repair Django models/serializers/configuration for Django audit hooks, access checks and protected media.
- [ ] **ERP-0910** (10/20) Create/review SQL Server migrations and indexes for Security, audit trail and protected attachments; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0911** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Immutable audit events, restricted operations, safe files and session controls.
- [ ] **ERP-0912** (12/20) Implement or repair ASP.NET business operations and idempotency for Security, audit trail and protected attachments.
- [ ] **ERP-0913** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Security, audit trail and protected attachments.
- [ ] **ERP-0914** (14/20) Enforce role/branch/action permissions and record audit events for Security, audit trail and protected attachments; prove server-side denial.
- [ ] **ERP-0915** (15/20) Implement or repair React API integration, screens and user feedback for Permission-aware UI and audit viewer.
- [ ] **ERP-0916** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Security, audit trail and protected attachments.
- [ ] **ERP-0917** (17/20) Run/add ASP.NET unit and validation tests for Audit author, before/after and reason for approved reversal; fix every failure.
- [ ] **ERP-0918** (18/20) Run/add Django unit and parity tests for Deny tampered upload, missing permission and audit deletion; fix every failure.
- [ ] **ERP-0919** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Posted financial events remain traceable; no secret/file leaks.
- [ ] **ERP-0920** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 47: Backup, restore and recovery drills — ERP-0921 to ERP-0940
**SRS sections:** 45, 56, 59. **Deliverable:** Scheduled/manual SQL Server backups, history, retention and restore evidence.
**Dependencies:** packages 03–04,46. **Invariant:** Restore tested in isolated environment; no live destructive restore.
**Happy-path proof:** Run backup then restore verified sample into nonproduction. **Negative proof:** Reject corrupted backup and unauthorized restore.

- [ ] **ERP-0921** (01/20) Extract Backup, restore and recovery drills acceptance details from SRS §§45, 56, 59; record assumptions and exclusions.
- [ ] **ERP-0922** (02/20) Inspect Deployment scripts and ASP.NET operational checks, Django recovery configuration and health checks and Backup history/status screen where operationally permitted; record actual files and current behavior.
- [ ] **ERP-0923** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0924** (04/20) Specify the happy-path acceptance: Run backup then restore verified sample into nonproduction.
- [ ] **ERP-0925** (05/20) Specify the negative/authorization case: Reject corrupted backup and unauthorized restore.
- [ ] **ERP-0926** (06/20) Design data, configuration and numeric BIGINT IDs for Scheduled/manual SQL Server backups, history, retention and restore evidence; record N/A with evidence if schema unchanged.
- [ ] **ERP-0927** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: Restore tested in isolated environment; no live destructive restore.
- [ ] **ERP-0928** (08/20) Implement or repair ASP.NET entities/configuration/contracts for Deployment scripts and ASP.NET operational checks.
- [ ] **ERP-0929** (09/20) Implement or repair Django models/serializers/configuration for Django recovery configuration and health checks.
- [ ] **ERP-0930** (10/20) Create/review SQL Server migrations and indexes for Backup, restore and recovery drills; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0931** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Scheduled/manual SQL Server backups, history, retention and restore evidence.
- [ ] **ERP-0932** (12/20) Implement or repair ASP.NET business operations and idempotency for Backup, restore and recovery drills.
- [ ] **ERP-0933** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Backup, restore and recovery drills.
- [ ] **ERP-0934** (14/20) Enforce role/branch/action permissions and record audit events for Backup, restore and recovery drills; prove server-side denial.
- [ ] **ERP-0935** (15/20) Implement or repair React API integration, screens and user feedback for Backup history/status screen where operationally permitted.
- [ ] **ERP-0936** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Backup, restore and recovery drills.
- [ ] **ERP-0937** (17/20) Run/add ASP.NET unit and validation tests for Run backup then restore verified sample into nonproduction; fix every failure.
- [ ] **ERP-0938** (18/20) Run/add Django unit and parity tests for Reject corrupted backup and unauthorized restore; fix every failure.
- [ ] **ERP-0939** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile Restore tested in isolated environment; no live destructive restore.
- [ ] **ERP-0940** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 48: Performance, observability and integration readiness — ERP-0941 to ERP-0960
**SRS sections:** 46, 56, 60, 61, 62, 65. **Deliverable:** Pagination, large-data indexes, monitoring and future accounting/API contracts.
**Dependencies:** packages 02–04,21–47. **Invariant:** No unbounded queries or financial side effects on retries.
**Happy-path proof:** Page through high-volume transactions and trace one request. **Negative proof:** Detect N+1 queries, lost idempotency and leaked exception details.

- [ ] **ERP-0941** (01/20) Extract Performance, observability and integration readiness acceptance details from SRS §§46, 56, 60, 61, 62, 65; record assumptions and exclusions.
- [ ] **ERP-0942** (02/20) Inspect EF query plans, structured logs and accounting event adapters, ORM query profiling, structured logs and matching events and Responsive paged lists and accessible loading/error states; record actual files and current behavior.
- [ ] **ERP-0943** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0944** (04/20) Specify the happy-path acceptance: Page through high-volume transactions and trace one request.
- [ ] **ERP-0945** (05/20) Specify the negative/authorization case: Detect N+1 queries, lost idempotency and leaked exception details.
- [ ] **ERP-0946** (06/20) Design data, configuration and numeric BIGINT IDs for Pagination, large-data indexes, monitoring and future accounting/API contracts; record N/A with evidence if schema unchanged.
- [ ] **ERP-0947** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: No unbounded queries or financial side effects on retries.
- [ ] **ERP-0948** (08/20) Implement or repair ASP.NET entities/configuration/contracts for EF query plans, structured logs and accounting event adapters.
- [ ] **ERP-0949** (09/20) Implement or repair Django models/serializers/configuration for ORM query profiling, structured logs and matching events.
- [ ] **ERP-0950** (10/20) Create/review SQL Server migrations and indexes for Performance, observability and integration readiness; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0951** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Pagination, large-data indexes, monitoring and future accounting/API contracts.
- [ ] **ERP-0952** (12/20) Implement or repair ASP.NET business operations and idempotency for Performance, observability and integration readiness.
- [ ] **ERP-0953** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Performance, observability and integration readiness.
- [ ] **ERP-0954** (14/20) Enforce role/branch/action permissions and record audit events for Performance, observability and integration readiness; prove server-side denial.
- [ ] **ERP-0955** (15/20) Implement or repair React API integration, screens and user feedback for Responsive paged lists and accessible loading/error states.
- [ ] **ERP-0956** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Performance, observability and integration readiness.
- [ ] **ERP-0957** (17/20) Run/add ASP.NET unit and validation tests for Page through high-volume transactions and trace one request; fix every failure.
- [ ] **ERP-0958** (18/20) Run/add Django unit and parity tests for Detect N+1 queries, lost idempotency and leaked exception details; fix every failure.
- [ ] **ERP-0959** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile No unbounded queries or financial side effects on retries.
- [ ] **ERP-0960** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 49: Thirteen end-to-end SRS acceptance scenarios — ERP-0961 to ERP-0980
**SRS sections:** 3, 7, 15, 16, 18, 21, 22, 23, 25, 26, 27, 29, 39, 57, 59, 65, 67, 68. **Deliverable:** 13 SRS tests on ASP.NET and Django with React, RTL and SQL Server.
**Dependencies:** packages 05–48. **Invariant:** All 13 source acceptance tests pass and failures have reproducible evidence.
**Happy-path proof:** Run all 13 purchase-to-warranty/security/RTL acceptance cases. **Negative proof:** Catch broken parity, repeat posting and unauthorized cancellation.

- [ ] **ERP-0961** (01/20) Extract Thirteen end-to-end SRS acceptance scenarios acceptance details from SRS §§3, 7, 15, 16, 18, 21, 22, 23, 25, 26, 27, 29, 39, 57, 59, 65, 67, 68; record assumptions and exclusions.
- [ ] **ERP-0962** (02/20) Inspect API integration fixtures and negative transaction tests, DRF integration fixtures and equivalent test vectors and React E2E tests against both backend targets; record actual files and current behavior.
- [ ] **ERP-0963** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0964** (04/20) Specify the happy-path acceptance: Run all 13 purchase-to-warranty/security/RTL acceptance cases.
- [ ] **ERP-0965** (05/20) Specify the negative/authorization case: Catch broken parity, repeat posting and unauthorized cancellation.
- [ ] **ERP-0966** (06/20) Design data, configuration and numeric BIGINT IDs for 13 SRS tests on ASP.NET and Django with React, RTL and SQL Server; record N/A with evidence if schema unchanged.
- [ ] **ERP-0967** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: All 13 source acceptance tests pass and failures have reproducible evidence.
- [ ] **ERP-0968** (08/20) Implement or repair ASP.NET entities/configuration/contracts for API integration fixtures and negative transaction tests.
- [ ] **ERP-0969** (09/20) Implement or repair Django models/serializers/configuration for DRF integration fixtures and equivalent test vectors.
- [ ] **ERP-0970** (10/20) Create/review SQL Server migrations and indexes for Thirteen end-to-end SRS acceptance scenarios; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0971** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for 13 SRS tests on ASP.NET and Django with React, RTL and SQL Server.
- [ ] **ERP-0972** (12/20) Implement or repair ASP.NET business operations and idempotency for Thirteen end-to-end SRS acceptance scenarios.
- [ ] **ERP-0973** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Thirteen end-to-end SRS acceptance scenarios.
- [ ] **ERP-0974** (14/20) Enforce role/branch/action permissions and record audit events for Thirteen end-to-end SRS acceptance scenarios; prove server-side denial.
- [ ] **ERP-0975** (15/20) Implement or repair React API integration, screens and user feedback for React E2E tests against both backend targets.
- [ ] **ERP-0976** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Thirteen end-to-end SRS acceptance scenarios.
- [ ] **ERP-0977** (17/20) Run/add ASP.NET unit and validation tests for Run all 13 purchase-to-warranty/security/RTL acceptance cases; fix every failure.
- [ ] **ERP-0978** (18/20) Run/add Django unit and parity tests for Catch broken parity, repeat posting and unauthorized cancellation; fix every failure.
- [ ] **ERP-0979** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile All 13 source acceptance tests pass and failures have reproducible evidence.
- [ ] **ERP-0980** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

### Package 50: Release, deployment, operations and roadmap gates — ERP-0981 to ERP-1000
**SRS sections:** 1, 45, 46, 56, 59, 60, 61, 62, 63, 65, 66, 68. **Deliverable:** Release checklist, branch promotion, rollback, operator docs and explicit phase-4 scope approvals.
**Dependencies:** packages 01–49. **Invariant:** No release without green required tests, backup/rollback and approval.
**Happy-path proof:** Deploy staging and complete smoke/recovery checklist. **Negative proof:** Block release on missing secrets, failing migration or unresolved critical defect.

- [ ] **ERP-0981** (01/20) Extract Release, deployment, operations and roadmap gates acceptance details from SRS §§1, 45, 46, 56, 59, 60, 61, 62, 63, 65, 66, 68; record assumptions and exclusions.
- [ ] **ERP-0982** (02/20) Inspect ASP.NET deployment, health probes and migration safeguards, Django deployment, worker health and migration safeguards and Production builds, mobile/tablet check and user handbook; record actual files and current behavior.
- [ ] **ERP-0983** (03/20) Compare source requirements with existing implementation; mark each gap with code evidence, not guesses.
- [ ] **ERP-0984** (04/20) Specify the happy-path acceptance: Deploy staging and complete smoke/recovery checklist.
- [ ] **ERP-0985** (05/20) Specify the negative/authorization case: Block release on missing secrets, failing migration or unresolved critical defect.
- [ ] **ERP-0986** (06/20) Design data, configuration and numeric BIGINT IDs for Release checklist, branch promotion, rollback, operator docs and explicit phase-4 scope approvals; record N/A with evidence if schema unchanged.
- [ ] **ERP-0987** (07/20) Define constraints, decimal/Unicode handling, statuses and rollback around: No release without green required tests, backup/rollback and approval.
- [ ] **ERP-0988** (08/20) Implement or repair ASP.NET entities/configuration/contracts for ASP.NET deployment, health probes and migration safeguards.
- [ ] **ERP-0989** (09/20) Implement or repair Django models/serializers/configuration for Django deployment, worker health and migration safeguards.
- [ ] **ERP-0990** (10/20) Create/review SQL Server migrations and indexes for Release, deployment, operations and roadmap gates; test upgrade/rollback or document why not applicable.
- [ ] **ERP-0991** (11/20) Document identical ASP.NET/Django /api paths, request shapes, responses, validation and error codes for Release checklist, branch promotion, rollback, operator docs and explicit phase-4 scope approvals.
- [ ] **ERP-0992** (12/20) Implement or repair ASP.NET business operations and idempotency for Release, deployment, operations and roadmap gates.
- [ ] **ERP-0993** (13/20) Implement or repair Django parity, transaction boundaries and idempotency for Release, deployment, operations and roadmap gates.
- [ ] **ERP-0994** (14/20) Enforce role/branch/action permissions and record audit events for Release, deployment, operations and roadmap gates; prove server-side denial.
- [ ] **ERP-0995** (15/20) Implement or repair React API integration, screens and user feedback for Production builds, mobile/tablet check and user handbook.
- [ ] **ERP-0996** (16/20) Verify English/Arabic Unicode, RTL, date/currency formatting, accessibility and responsive behavior for Release, deployment, operations and roadmap gates.
- [ ] **ERP-0997** (17/20) Run/add ASP.NET unit and validation tests for Deploy staging and complete smoke/recovery checklist; fix every failure.
- [ ] **ERP-0998** (18/20) Run/add Django unit and parity tests for Block release on missing secrets, failing migration or unresolved critical defect; fix every failure.
- [ ] **ERP-0999** (19/20) Run SQL Server integration, concurrency and React E2E checks; reconcile No release without green required tests, backup/rollback and approval.
- [ ] **ERP-1000** (20/20) Review duplication/security/performance, fix regressions, update API docs and record test + commit evidence before next step.

## Source SRS acceptance cases (13 mandatory)

All 13 must pass against **both** backends through the same React UI and SQL Server test data:
1. Product → purchase → stock increases.
2. Customer → quotation → printable quotation.
3. Quotation → sales invoice conversion.
4. Direct sales invoice → stock decreases.
5. Credit invoice → customer outstanding increases.
6. Customer payment → outstanding decreases.
7. Sales return → stock increases.
8. Purchase return → stock decreases.
9. Purchased serial → sold serial → customer warranty.
10. English and Arabic documents print correctly.
11. Low stock → dashboard alert.
12. Unauthorized action is blocked by the API.
13. Cancelled financial transaction retains its audit trail.

Tax treatment and any active Kuwait statutory rate require accountant/legal verification before release; never hard-code rates. Phase-4 integrations need credentials and business approvals, not fictional production connections.
