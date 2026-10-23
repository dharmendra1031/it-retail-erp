# WP02 — Shared architecture, numbering and API contract

**Target:** ERP-0021–ERP-0040. **SRS:** §§46, 54–58, 60, 61, 63. **Status:** scoped WP02 complete with documented downstream deferrals; CI 39911998441 (5/5 PASS).

## Existing architecture

- React/Vite calls relative `/api`, so `VITE_PROXY_TARGET` selects either backend without modifying client code.
- ASP.NET Core 10 uses Identity<long>, EF migrations, antiforgery and controllers. Django 5.2 uses DRF session auth, SQL Server migrations, BigAutoField.
- Shared endpoints: `auth/csrf`, `auth/login`, `auth/me`, `auth/logout`, `companies`, `roles`.
- Company reads require login, mutations require Admin. Roles API requires Admin.
- Runtime stock, financial documents, customer/supplier, branch/warehouse and audit trail belong to their downstream work packages. Do not claim these exist now.

## Numbering design (WP02 owned)

- A *separate* numeric BIGINT IDENTITY/BigAutoField database key is used for `DocumentSequences`.
- A counter is scoped by `series` (1–20 uppercase letters/digits/_/-), `fiscal_year` (2000–9999), and `branch_id` (BIGINT non-negative, **0 = default single-site scope**, pending WP09 real branch FK).
- `last_number` is BIGINT; composite key is unique, with an index on the scoped series. Returning a number is atomic and concurrent-safe on SQL Server using `sp_getapplock` under the caller's transaction boundary.
- No formatted invoice code is assumed. Prefix/padding/year reset and branch display are **unapproved DEC-05** and remain configurable/business-owner decisions.
- Shared internal allocation services: `DocumentNumberService.NextAsync(series, year, branchId)` and `apps.core.numbering.next_number(series, year, branch_id)`. **No public allocate-number API**: future Purchase/Sales/Quotation modules must allocate as part of posting, not via an orphan reservation endpoint.
- Allocations commit their own transaction currently. Future posted-document operation must encompass sequence+invoice persistence in the **same** outer transaction to avoid gaps on failure; integration to WP24–WP34 is deferred. **Never call this a gap-free legally approved numbering engine.**

## Scope/status and acceptance

- WP02's current acceptance: same frontend can sign in and manage Role/Company against both backends; consistent success status/fields, duplicate/permission denials; SQL Server schema and concurrent numbering unique.
- ASP and Django DB schema need not share framework table names. Numeric IDs, English/Arabic company Unicode and strong database uniqueness are invariant.
- Error-body normalization, all validation details, tenant scope, full localized output, posting idempotency and audit remain work to be verified and corrected. They are **not** marked accepted solely from builds.
- Owner gates: WP03 reproducible environment, WP05 CSRF/login hardening, WP06–09 permissions/branches, WP11 localization, WP24–34 business posting, WP46 audit, WP49 full cross-backend browser acceptance.


## ERP-0021–ERP-0040 verification matrix

| Step | Evidence and acceptance |
|---|---|
| ERP-0021 | Mapped source SRS §§46,54–58,60–61,63 to backend interchangeability, numbering invariants and downstream owners. |
| ERP-0022 | Inspected actual net10 EF controllers, Django DRF routing and Vite relative /api proxy source. |
| ERP-0023 | Checked SRS-to-code gaps; branch/warehouse, stock, financial docs and audit remain future-owned. |
| ERP-0024 | Same React admin workflow tested against Django and ASP backend with unchanged UI. |
| ERP-0025 | Duplicate names and concurrent sequence allocation rejected by server/database; matching Role/Company error status contract recorded. |
| ERP-0026 | BIGINT DocumentSequence with composite unique series/year/branch scope in both backends. |
| ERP-0027 | Defined status/data safety, no money floats, Unicode and transaction lock; document format and final posting rollback deferred DEC-05/WP24–34. |
| ERP-0028 | ASP.NET model, DbContext, sequence service and EF migration implemented. |
| ERP-0029 | Django DocumentSequence, sequence allocation and migration implemented. |
| ERP-0030 | Both SQL Server migrations, unique indexes and safe down/up tests completed in isolated CI databases. |
| ERP-0031 | Auth/Company/Role API payloads, statuses, validation/error contract and numbering interface documented. |
| ERP-0032 | ASP.NET DocumentNumberService uses SQL Server sp_getapplock in transaction, tested concurrent/scoped allocation. |
| ERP-0033 | Django number allocation uses atomic transaction and sp_getapplock under SQL Server, tested concurrent/scoped allocation. |
| ERP-0034 | Role/Company admin restrictions verified; future tenant scope and immutable audit owned by WP06–09/WP46. |
| ERP-0035 | One React/Vite app switched between both backends via proxy env, no duplicated frontend. |
| ERP-0036 | Arabic company text round-trip verified in two SQL Server backends; full RTL/currency/printing deferred WP11/WP44. |
| ERP-0037 | ASP.NET SQL-backed numbering xUnit tests 3/3 PASS; React admin parity smoke on ASP PASS. |
| ERP-0038 | Django 32/32 on SQL Server, 27 PASS/5 skipped SQL-only on SQLite, including sequence/role concurrency. |
| ERP-0039 | Ephemeral SQL Server tests plus Playwright React admin journey on ASP and Django; future business E2E remains future-owned. |
| ERP-0040 | Reviewed constraints, API errors, concurrency, schema drift and CI; recorded missing advanced integrations as deferred, not passed. |

**Runtime evidence:** [GitHub Actions run 39911998441](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39911998441). 32/32 Django SQL Server tests, 3/3 ASP.NET xUnit SQL tests, API smoke, Django Playwright 2/2 and ASP Playwright 1/1. No claims about business document posting or finance/stock behavior.
