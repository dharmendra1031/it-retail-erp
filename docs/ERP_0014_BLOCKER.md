# ERP-0014 — authorization/audit blocker

**Reviewed development HEAD:** `7f7def45a2dc22a5585c63286bf129d57b262554`

ERP-0014 requires server-side role/branch/action permission enforcement, audit events and proof that a restricted action is denied.

## Current evidence

- ASP.NET Company controller has controller-level `[Authorize]` only; no ERP action policy for View/Add/Edit/Delete and no branch scope enforcement/audit event.
- Django CompanyViewSet uses `IsAuthenticated` only; Role/AccessPermission models exist but are not consumed by this endpoint.
- Package-01 traceability itself is Git metadata and has no runtime endpoint on which a meaningful ERP permission can be enforced.
- ERP-0005 already specifies the concrete negative acceptance: an authenticated user without `Company.Delete` must receive 403 and the Company row must remain unchanged.

## Blocker

A passing ERP-0014 proof requires the shared authorization foundation and audit persistence owned by later User/Role/Permission/Audit work packages. Implementing an isolated Package-01-only permission system would duplicate future architecture and violate scope sequencing.

**Status: BLOCKED.** Do not mark complete and do not advance to ERP-0015. Unblock when shared permission codes, user/role assignment, branch scope and immutable audit design exist in both backends; then enforce Company.Delete server-side and execute the 403/no-mutation/audit parity test.
