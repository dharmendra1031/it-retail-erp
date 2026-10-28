# ERP-0314 — Product Master authorization, CSRF and scope contract

**Reviewed source:** `development` at `f24b00b5138370038fab07fd6c5bba49a4c95dc1`. **Verified CI:** [40658905027](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40658905027) — 5/5 jobs SUCCESS, including both Django and ASP.NET Product authorization/CSRF regressions.

## Current server-side Product authorization

- ASP.NET `ProductsApiController` enforces `[Authorize]` plus action policies `products.view/add/edit/delete`. `PermissionHandler` checks current DB role membership and `erp.permission` role claims. Admin role can perform all actions.
- Django `ProductViewSet` inherits `CatalogPermission` + `IsAuthenticated` and resolves `products.*` against saved role grants. Users with a single `products.view` grant can GET Product list/detail but cannot POST/PUT/DELETE. Mutations are not authorized solely by hiding UI controls.
- **CSRF regression fixed:** ASP.NET Product POST was actually permitted without a CSRF header when using bare `[ValidateAntiForgeryToken]`; CI [40658496827](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40658496827) proved that by unexpectedly inserting a Product. In commit `f24b00b5`, Product Create/Update/Delete now apply the existing service-registered `ApiCsrfFilter` (working in Role/Company APIs). Subsequent real HTTP smoke rejects a Product create missing CSRF with 403 and confirms that no record was saved. Django's authenticated cookie session uses `ApiSessionAuthentication` and Django CSRF, tested with `APIClient(enforce_csrf_checks=True)`.

## New tests and evidence

- `django/apps/catalog/tests.py`: admin creates Product, non-admin without grant gets 403 on list/detail, assigning `products.view` enables read-only list/detail, then POST/PUT/DELETE all return 403 and original Product row remains unchanged. A separate CSRF-enforced cookie-session test rejects Product creation without token.
- `aspnet-core/tests/smoke_sqlserver.py`: with disposable SQL Server and real HTTP authentication, admin POST without CSRF returns 403/no Product, employee without Product grant gets 403, then assigned `products.view` can GET list/detail but cannot mutate. Admin GET confirms unauthorized edit did not change the row.
- The initial red SQL Server job caught the CSRF vulnerability, and the corrected run 40658905027 passed all five jobs. Existing Product physical schema, Django/EF migrations, financial/role regressions and React browser tests remained green.

## Scope and audit owner boundaries

`Product` currently has **no CompanyId, BranchId or warehouse stock balance**. It is a global Product Master; **there is no branch-scoped Product filter to claim**. Branch/warehouse stock availability and movement scope belong WP21/WP25, and generalized product audit history (actor, before/after, timestamp) belongs WP46. This package keeps server-side Product CRUD permissions and protects invalid/unapproved mutations, but does not fabricate a branch-ID column or new audit subsystem. The React shell currently hides master navigation from non-admin users, even where they have `products.view`; role-aware React product navigation is an identified UI/access gap for ERP-0315/integration, not a backend bypass.

No schema migration, stock postings or production database change. Next: ERP-0315 Product React form/list/selectors and pagination.
