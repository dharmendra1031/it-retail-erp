# ERP-0007 — traceability constraints, statuses and rollback rules

**Reviewed development HEAD:** `fd6565471ec6a40ff0e2b18d6f04d8ccf056f8a6`

Package 01 traceability is version-controlled engineering metadata. ERP-0007 therefore defines integrity rules for the documents/tracker and records runtime database concerns without inventing a traceability table.

## Traceability constraints

1. Every plan requirement has one stable `ERP-NNNN` ID and an owning work package.
2. Every SRS gap row must carry concrete source evidence and a plan owner; absence is recorded as `ABSENT`, not guessed.
3. Every acceptance case keeps a stable `AT-01`–`AT-13` key and may be marked passed only with actual required runtime evidence.
4. `ERP_PROGRESS.json.nextStepId` is the first incomplete/unblocked plan step. A blocked step remains current.
5. A completed step must have evidence paths and verification notes; unexecuted tests are recorded as `not run`, never inferred from source existence.
6. Scope decisions use explicit decision IDs and owner/gate. Unknown business policy is not replaced with a developer default.
7. Runtime business entity IDs remain numeric BIGINT auto-increment/BigAutoField; traceability codes are document keys, not DB primary keys.

## Status vocabulary

Requirement implementation status: `ABSENT`, `PARTIAL`, `IMPLEMENTED_UNVERIFIED`, `VERIFIED`, `FUTURE_DECISION`, `OUT_OF_SCOPE`.

Execution step status: `pending`, `blocked`, `complete`. `complete` means the step's applicable gate is satisfied; it does not imply dependent SRS acceptance cases pass.

Acceptance status: `pending`, `blocked`, `passed`. Only executed evidence can move an acceptance case to `passed`.

## Unicode

Traceability files are UTF-8 and may contain English/Arabic evidence. Runtime bilingual ERP text must remain Unicode end-to-end. Current Company evidence is compatible: ASP.NET migration uses SQL Server `nvarchar` and React Arabic inputs use RTL direction; Django strings are Unicode. This source inspection is not a live database round-trip test.

## Decimal handling

Package 01 introduces no money fields, so decimal schema is **N/A** here. Future money/rate/quantity models must use explicit fixed precision consistently in SQL Server, EF and Django; binary floating-point is not acceptable for posted money. Exact precision/rounding is owned by the relevant financial/tax package and must be parity-tested before posting. DB-003 remains open.

## Rollback and correction

- Documentation correction: commit a forward correction preserving Git history; do not rewrite published development history merely to hide a bad status.
- Incorrectly completed step: revert its plan checkbox/tracker status in a corrective commit, restore it as `nextStepId`, record why, and do not work later steps until resolved.
- Requirement/SRS change: record the changed baseline and affected owners/acceptance cases before implementation.
- Runtime schema/data rollback: not applicable to ERP-0007 because no migration is introduced. Future migrations require additive/data-preserving upgrade and tested rollback/forward-fix strategy before production.
- Never use destructive production rollback to satisfy documentation traceability.

## Current database constraints observed

Existing Company uses numeric `long/BIGINT IDENTITY` in ASP.NET and Django business models use BigAutoField policy. ASP.NET Company bilingual columns are `nvarchar`; TaxNumber/CommercialRegistrationNumber are indexed but not unique. Business uniqueness is intentionally not invented here. Existing DB-001–DB-006 remain unresolved at their owning gates.

## Exit evidence

This document plus the database-review entry is the ERP-0007 deliverable. No application code, schema or migration change is required. Runtime build, SQL migration and E2E are not applicable to this documentation-only constraint definition and are not reported as passed.
