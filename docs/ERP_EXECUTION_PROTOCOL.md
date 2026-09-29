# ERP hourly execution protocol

**Authoritative scope:** [Original SRS](https://docs.google.com/document/d/1Gb_pMJAN14UY0scLJjGBGiuRZdlXOWJARB1aLkzIobc/edit?usp=sharing) and [1000-step plan](ERP_PLAN_1000_STEPS.md).
**Work branch:** `development` only. **Progress tracker:** [ERP_PROGRESS.json](ERP_PROGRESS.json).
**No claim of autonomous background execution unless a scheduled task actually runs; an hourly run must produce traceable evidence.**

## Every hourly run: strict sequence

1. Read the latest SRS, plan, tracker and latest `development` commit; reconcile changed requirements before work.
2. Select the first incomplete step by numeric ID. If a prior step is blocked, resume it; do not skip.
3. Open the exact existing ASP.NET, Django, React, SQL migration, contract and test files relevant to that step. Evidence for an existing implementation must come from real code, not README/commit messages.
4. Compare code with this step's SRS reference, deliverable, dependencies, happy/negative case and invariants. Record missing functionality and bugs before editing.
5. Implement the smallest idiomatic change that satisfies the step on both backend implementations and the shared UI when applicable. Keep SQL Server and numeric BIGINT IDs; preserve state transitions, Unicode, decimals and API parity.
6. Audit for duplicated/dead code, missing validation, authorization bypass, CSRF, unsafe file handling, idempotency, transaction/stock/ledger errors, migration drift, incorrect monetary rounding and regression risks. Fix defects before moving on.
7. Run applicable `.NET build/test`, Django checks/tests, migrations in safe test environment, React build/tests and cross-backend/API/MSSQL/E2E checks. If a runtime is unavailable, label validation unverified and do not mark the step complete when that test is required.
8. Re-read the changed code and diffs. Record failing/passing commands, acceptance evidence and exact changed paths in the tracker. Never report a test as passed without executing it.
9. Commit source + tests + tracker/doc updates to `development` with a professional descriptive message; reread remote HEAD. Never commit `.env`, passwords, DB dumps, generated binaries or tokens.
10. Mark a step complete only when every applicable acceptance criterion and required checks pass. For blocked steps, preserve its ID, code/commit/evidence and blocker; do not advance. Start the next step only in a later iteration after the preceding gate passes.
11. Report short status: step ID, verified existing code, changes, bug fixes, tests actually run, commit SHA, next step or exact blocker.

## Acceptance and stop conditions

- Existing functionality may satisfy a task, but it still requires concrete code evidence, applicable tests and a tracker update.
- Reject false green results, fabricated commits, guessed repository paths, skipped permission checks or bypassed tests.
- Respect production safety: no destructive DB operation, restore, deployment, payment processing, branch merge or external integration without necessary authorization and safe environment.
- Prefer narrow tested commits; keep ASP.NET and Django behavior and shared React request/response contracts aligned.
- When blocked by missing access, secrets, business policy, environment or failing tests, keep the same step open and report exact remedial action. No work on later steps until resolved.
- This file defines **what to do when the hourly task runs**. The scheduler and GitHub permissions determine whether unattended execution can act; verify actual completed commits in the repository.
