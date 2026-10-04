# ERP 1000-step dependency and sequencing audit

**Reviewed branch:** `development` @ `8e79e082ec9245ae63d30e8091b66b1435202945`

ERP-0014 exposed a repeated-template sequencing defect: early packages could demand cross-cutting runtime capabilities intentionally owned later. The features were present in the 1000-step scope; the order semantics were wrong.

## Authoritative cross-cutting ownership

| Capability | Owner |
|---|---|
| API parity | WP02 |
| Dev/test environment | WP03 |
| SQL/migration conventions | WP04 |
| Authentication/CSRF | WP05 |
| Permission catalog/action policies | WP06 |
| Role Master/permission assignment | WP07 |
| User Master/role membership | WP08 |
| Branch/warehouse access | WP09 |
| Localization/RTL | WP11 |
| Bilingual/A4/A5/thermal printing | WP44 |
| Security/audit hardening + protected files | WP46 |
| Full 13-case E2E acceptance | WP49 |
| Release/deployment | WP50 |

## Corrected rule

A package implements capabilities it owns and capabilities delivered by already-completed dependencies. If a checklist item references a later-owned capability, the current package records the required contract, acceptance evidence and downstream owner and defers runtime implementation. It does not build a duplicate temporary system and does not block solely on the future dependency.

A real blocker still applies when the missing behavior belongs to the current package or an already-due dependency, or when current-package environment/business/test requirements cannot be satisfied.

## Additional dependency defect found

WP23 Warranty explicitly depended on WP30 Sales, a later package. WP23 now owns warranty policy/date/status/serial-ready foundations. Sold-customer/source-invoice linkage is integrated by WP30 and finally proven by WP49. This removes the forward dependency without weakening the SRS warranty requirement.

## Verification

01. PASS — 50 packages retained
02. PASS — 1000 steps retained
03. PASS — unique IDs
04. PASS — ERP-0001..ERP-1000 order retained
05. PASS — 20 steps per package
06. PASS — no forward/cyclic explicit dependency
07. PASS — WP23 forward dependency removed
08. PASS — all 50 step-14 gates ownership-aware
09. PASS — global semantics present
10. PASS — protocol dependency gate present
11. PASS — completed ERP-0001..0013 preserved
12. PASS — ERP-0014 complete
13. PASS — ERP-0015 still pending
14. PASS — WP06 permissions preserved
15. PASS — WP07 roles preserved
16. PASS — WP08 users preserved
17. PASS — WP09 branch scope preserved
18. PASS — WP46 audit hardening preserved
19. PASS — WP49 E2E retained
20. PASS — no future capability falsely marked runtime-pass

**Result: 20/20 dependency-plan checks passed.**

No application code, SQL schema, production data, authorization behavior or audit persistence was changed by this sequencing correction.
