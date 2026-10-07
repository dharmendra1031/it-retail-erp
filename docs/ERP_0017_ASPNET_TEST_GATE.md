# ERP-0017 — ASP.NET unit/validation test gate

**Reviewed development HEAD:** `15f9aff05b4f7f576727b3dc51579c00f14341ea`

## Test inventory

The repository currently has no `aspnet-core/tests` test project. The ASP.NET tree contains `src` plus configuration/readme files. Existing request validation was inspected in `CompanyRequest` and `LoginRequest`.

WP01 owns the version-controlled SRS/requirement/acceptance traceability deliverable; it owns no ASP.NET runtime business feature. Per the dependency audit, the shared dev/test environment and reusable test harness belong to **WP03**. Creating a one-off WP01 test project would duplicate that future architecture.

## Required downstream ASP.NET tests

When WP03 supplies the test harness, retain these contracts:
- Company request requires `NameEn` and enforces current max lengths.
- Company email and website validation reject malformed values consistently with the shared API contract.
- Login request requires valid email and password.
- Company bilingual values, including Arabic, survive API + SQL Server round-trip unchanged.
- Backend-switch/API parity tests belong to WP02/WP49; permission denial belongs to WP06–WP09/WP49.
- DB-005 logo failure injection and DB-006 pagination tests belong to WP10/WP48.

## Execution

No `dotnet test` was executed because no ASP.NET test project exists at this HEAD. No test is reported passing. This is a valid dependency-aware specification gate for WP01, not a runtime test pass.

No application code, schema, migration or production data is changed.
