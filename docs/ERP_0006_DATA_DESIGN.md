# ERP-0006 — requirement traceability data and configuration design

**Reviewed development HEAD:** `d795659f69e2c04fb2cc49bc6868837704426ed0`

## Decision

The Package 01 requirement-to-implementation map, scope decisions and 13 acceptance cases are **engineering traceability metadata**, not runtime ERP business data. They remain version-controlled under `docs/`; ERP-0006 therefore requires **no SQL Server table, EF entity, Django model, API endpoint or React persistence feature**.

Adding a Requirement/Acceptance database table now would duplicate Git history, create two sources of truth and introduce schema/API parity work with no SRS runtime requirement.

## Canonical configuration

| Concern | Canonical source |
|---|---|
| SRS baseline and scope decisions | `docs/SRS_BASELINE.md` |
| Requirement ownership/gaps/evidence | `docs/ERP_REQUIREMENTS_GAP_MATRIX.md` |
| 1000 ordered implementation gates | `docs/ERP_PLAN_1000_STEPS.md` |
| Machine-readable execution position/history | `docs/ERP_PROGRESS.json` |
| Per-run database findings | `docs/ERP_DATABASE_REVIEW.md` |
| Happy/negative acceptance specifications | `docs/ERP_0004_ACCEPTANCE.md`, `docs/ERP_0005_NEGATIVE_ACCEPTANCE.md` |

Requirement keys use stable plan IDs such as `ERP-0006`; acceptance keys use `AT-01` through `AT-13`. These are versioned document identifiers, **not database primary keys**.

## Numeric ID rule

All persisted ERP application entities continue to use numeric auto-increment IDs. Existing evidence:
- ASP.NET Company/User/Role application keys use `long` / SQL Server `BIGINT IDENTITY`.
- Django business models inherit Django's configured/default auto field and current migrations use `BigAutoField`.
- No UUID/GUID/public-ID field is introduced by this step.

If traceability ever becomes runtime data by an approved requirement, its new entity primary keys must be numeric BIGINT auto-increment in both backends; human requirement codes remain separate unique business keys.

## Schema impact

**N/A — schema unchanged.** No migration is appropriate for ERP-0006. This is intentional, not missing implementation. Existing DB-001 through DB-006 remain open and must be fixed only at their owning safe implementation gates.

No money, stock or financial transaction is introduced. DECIMAL precision, posting atomicity, stock/ledger reconciliation and immutable transactional audit therefore cannot be signed off by this step.

## Verification gate

ERP-0006 is complete when this design is committed, the database review records the N/A decision, the plan/tracker advance together, and remote `development` is read back. Runtime builds, SQL migration execution and E2E are not required for a documentation-only no-schema design decision and must not be reported as passed.
