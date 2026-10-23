# ERP-0001–ERP-0060 — Source and CI recheck

**Date:** 2026-10-23  
**Branch:** `development`  
**Verified code commit:** `7de114b516b9951a4c09b9bbddd7f9c86e33a35a`  
**CI:** [Run 39915764939](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39915764939) — all five jobs PASS.

## Tracker/source consistency (ERP-0001–ERP-0050)

- Previously completed IDs 0001 through 0050 were sequential, with no missing ID, and all completion flags matched the 1000-step plan.
- All recorded `history[].evidence` paths existed in the current Git tree.
- ERP-0014 has two history entries (initial blocker and subsequent resolution); this is not a second completed step.
- The first 20 steps are SRS traceability/review and initial tests; 0021–0040 are shared backend contract and document numbering; 0041–0060 are developer environment, CI and reproducible build gates. **These are not 60 fully delivered business modules.**

## Rechecked runtime evidence

| Check | Verified result |
|---|---|
| GitHub Actions | 5 of 5 jobs PASS |
| Django on SQL Server 2022 | 33 of 33 tests PASS |
| Django SQLite | 28 PASS; 5 SQL-only tests skipped (33 discovered) |
| ASP.NET Core SQL Server xUnit | 4 of 4 PASS |
| ASP.NET Core API SQL smoke | PASS — admin login, Role CRUD, Company Arabic round-trip, invalid blank payloads |
| Playwright with Django | 4 of 4 PASS |
| Playwright with ASP.NET Core | 3 of 3 PASS |
| React build and ASP.NET Core Release build | PASS |
| Django and EF migration upgrade/rollback/reapply | PASS on disposable SQL Server |
| Negative startup without Django production secret/DB or ASP SQL connection | PASS (startup correctly rejected) |

## ERP-0051–ERP-0060 disposition

| ID | Acceptance / evidence |
|---|---|
| ERP-0051 | Reviewed and documented existing identical auth/Company/Role routes, request formats, success/error shapes and how backend selection is configured. WP03 owns no new runtime API. |
| ERP-0052 | Rechecked ASP.NET Core startup, Identity/antiforgery, EF migrations and number transaction participation. WP03 owns no additional business posting operation; idempotency is deferred to WP24–34. |
| ERP-0053 | Rechecked Django production config, DRF auth/error handling, SQL transaction scope and migrations. WP03 owns no additional business posting operation. |
| ERP-0054 | Verified present Admin-only Company writes/Role API. Company/branch scoping and immutable audit remain WP06–09/WP46; no premature tables or role models introduced here. |
| ERP-0055 | React shared API client now shows safe JSON detail messages. Same Vite frontend verified on Django and ASP.NET without source changes. |
| ERP-0056 | Arabic Company CRUD tested against both backends; narrow-screen Role Master navigation tested in Playwright. Full translation, RTL documents, KWD/date display require WP11/WP44. |
| ERP-0057 | ASP.NET Core Release build, missing connection-string startup negative check, 4/4 xUnit SQL tests and 3/3 Playwright ASP browser tests PASS. |
| ERP-0058 | Django missing SECRET_KEY/DB_NAME negative checks, migration model drift, SQLite 28 PASS/5 SQL-only skips and SQL Server 33/33 PASS. |
| ERP-0059 | Ephemeral SQL Server migration/rollback/concurrency and Role/Company HTTP smoke PASS on both backends; Playwright Django 4/4 and ASP 3/3 PASS. Only current WP03/WP02 surfaces claimed. |
| ERP-0060 | Re-read foundational code, test coverage and open security/performance limitations; updated API docs and audit/tracker. No production secrets or data accessed. |

## Known limitations and next owners

- **DB-001:** ASP normalized email uniqueness upgrade still needs safe existing-data review (WP05/WP08).
- **DB-002:** ASP Identity framework role/user claim IDs use INT even though ERP business keys use BIGINT; decision/migration still open (WP04).
- **DB-003:** Sales/Purchase/Inventory/Accounting schema, DECIMAL precision, stock/ledger posting and idempotency are not implemented yet (WP18–WP37).
- **DB-004:** Framework-specific auth schemas legitimately differ; API parity requires continued regression checks (WP05/WP49).
- **DB-005:** Company logo filesystem/DB atomicity is unresolved (WP10/WP48).
- **DB-006:** Company listings are unpaginated (WP10/WP48).
- SQL Server tests use **SQL Server 2022**, not the intended initial **SQL Server 2019** production version. Production compatibility and performance are not certified.
- Complete per-user permissions, tenant/branch-scoped access and immutable audit remain WP06–WP09/WP46.
- Full bilingual interface/RTL, monetary/date presentation, printing, purchase-to-stock, sales and receivables remain downstream owner tasks. Document number formatting is pending business decision DEC-05.
- No deployment, business data migration or production database mutation was performed.

**Outcome:** Foundation/contract/CI steps 0001–0060 are now complete **within their defined packages**. Whole-ERP functional and production acceptance is **not** complete. Next task is ERP-0061 (WP04) and then business masters/transactions.
