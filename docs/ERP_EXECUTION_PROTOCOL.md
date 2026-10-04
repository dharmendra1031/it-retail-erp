# ERP hourly execution protocol

**Authoritative scope:** [Original SRS](https://docs.google.com/document/d/1Gb_pMJAN14UY0scLJjGBGiuRZdlXOWJARB1aLkzIobc/edit?usp=sharing) and [1000-step plan](ERP_PLAN_1000_STEPS.md).
**Work branch:** `development` only. **Progress tracker:** [ERP_PROGRESS.json](ERP_PROGRESS.json). **Database design review log:** [ERP_DATABASE_REVIEW.md](ERP_DATABASE_REVIEW.md).
**No claim of autonomous background execution unless a scheduled task actually runs; an hourly run must produce traceable evidence.**

## Every hourly run: strict sequence

1. Read the latest SRS, plan, tracker and latest `development` commit; reconcile changed requirements before work.
2. Select the first incomplete step by numeric ID. If a prior step is blocked, resume it; do not skip.
3. Open the exact existing ASP.NET, Django, React, SQL migration, contract and test files relevant to that step. Evidence for an existing implementation must come from real code, not README/commit messages.
4. Compare code with this step's SRS reference, deliverable, dependencies, happy/negative case and invariants. Record missing functionality and bugs before editing.
**Dependency gate:** Before declaring a blocker, resolve ownership. If a needed capability is owned by a later work package, record its contract/acceptance and downstream owner and defer runtime implementation. Do not create duplicate placeholder architecture and do not block the current step solely because a future-owned capability is missing. Block only when the missing capability belongs to the current package or an already-due dependency.
5. **On every run, review database design:** inspect relevant EF/Django entities and migrations, numeric IDs, FK/index/unique constraints, Unicode, DECIMAL precision, schema parity, transaction atomicity, audit and upgrade/rollback safety. Update `ERP_DATABASE_REVIEW.md` with findings and exact test evidence. Fix verified defects using safe migrations and tests when possible; otherwise retain an explicit blocker.
6. Implement the smallest idiomatic change that satisfies the step on both backend implementations and the shared UI when applicable. Keep SQL Server and numeric BIGINT IDs; preserve state transitions, Unicode, decimals and API parity.
7. Audit for duplicated/dead code, missing validation, authorization bypass, CSRF, unsafe file handling, idempotency, transaction/stock/ledger errors, migration drift, incorrect monetary rounding and regression risks. Fix defects before moving on.
8. Run applicable `.NET build/test`, Django checks/tests, migrations in safe test environment, React build/tests and cross-backend/API/MSSQL/E2E checks. If a runtime is unavailable, label validation unverified and do not mark the step complete when that test is required.
9. Re-read the changed code and diffs. Record failing/passing commands, acceptance evidence and exact changed paths in the tracker. Never report a test as passed without executing it.
10. Commit source + tests + tracker/doc updates to `development` with a professional descriptive message; reread remote HEAD. Never commit `.env`, passwords, DB dumps, generated binaries or tokens.
11. Mark a step complete only when every applicable acceptance criterion and required checks pass. For blocked steps, preserve its ID, code/commit/evidence and blocker; do not advance. Start the next step only in a later iteration after the preceding gate passes.
12. Report short status: step ID, verified existing code, changes, bug fixes, tests actually run, commit SHA, next step or exact blocker.

## Acceptance and stop conditions

- Existing functionality may satisfy a task, but it still requires concrete code evidence, applicable tests and a tracker update.
- Reject false green results, fabricated commits, guessed repository paths, skipped permission checks or bypassed tests.
- Respect production safety: no destructive DB operation, restore, deployment, payment processing, branch merge or external integration without necessary authorization and safe environment.
- Prefer narrow tested commits; keep ASP.NET and Django behavior and shared React request/response contracts aligned.
- When blocked by missing access, secrets, business policy, environment, failing tests, or a missing capability owned by the current/already-due package, keep the same step open and report exact remedial action. A later-package dependency must be recorded and deferred, not treated as a blocker by itself.
- This file defines **what to do when the hourly task runs**. The scheduler and GitHub permissions determine whether unattended execution can act; verify actual completed commits in the repository.
