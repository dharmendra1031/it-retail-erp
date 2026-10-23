# WP02 — Shared architecture, numbering and API contract

**Target:** ERP-0021–ERP-0040. **SRS:** §§46, 54–58, 60, 61, 63. **Status:** implementation and tests in progress.

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
