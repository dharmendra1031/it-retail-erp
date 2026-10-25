# WP15 — Brand and Unit Master acceptance (ERP-0281–0300)

**SRS:** §§4, 12, 14, 63. **Implementation:** `1d611a93ecc838bc87ddf8cdde646195c278005a`. **Status:** Verified — CI [40170805039](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40170805039) 5/5 PASS on implementation commit `e8cb36b5`.

## Acceptance and code ownership

| Steps | Evidence / decision |
| --- | --- |
| 0281–0283 | Reviewed SRS, `Brand`/`Unit` models, ASP.NET controllers, DRF viewsets, React Catalog form, EF/Django migrations and Product FK. Scope: global bilingual Brand and Unit masters; product pricing and inventory are future-owned. |
| 0284–0285 | Positive: create English/Arabic Brand and Unit, retrieve and update, reference both through Product API. Negative: normalized duplicate code, invalid precision, unauthorized operation, and referenced delete. |
| 0286–0287 | Numeric BIGINT identity/BigAutoField IDs; normalized uppercase code; NVARCHAR Unicode names; unique code indexes; Unit decimal places 0–6 with database check constraint; Product.BrandId optional and Product.UnitId required, both protected on delete. |
| 0288–0289 | `BrandsApiController`, `UnitsApiController`, `CatalogRequests.cs`, `django/apps/catalog/api.py` provide equivalent CRUD and new `?search=` across code, English and Arabic names. |
| 0290 | Existing `20261023130000_CatalogMasters.cs`, `20261025040000_UnitPrecisionCheck.cs`, `catalog/0001_initial.py` and `catalog/0003_unit_precision_check.py` own schema. No new migration needed. Verify migrations and SQL rollback in CI. |
| 0291–0293 | Both APIs: `GET /api/brands`, `GET /api/brands?search=...`, `GET /api/brands/{id}`, `POST /api/brands`, `PUT /api/brands/{id}`, `DELETE /api/brands/{id}`; same for `/api/units`. JSON: `code`, `nameEn`, `nameAr`, `isActive`, and Unit `decimalPlaces`. Return 200/201/204, invalid/duplicate 400, unauthenticated 401, forbidden 403, not found 404, referenced 409. SQL unique and FK constraint errors handled after concurrent writes. |
| 0294 | Global catalog permissions: `brands.view/add/edit/delete`, `units.view/add/edit/delete` enforced by both backends; CSRF enforced for .NET writes. Brand/Unit are not branch-specific. Persistent audit log is WP46. |
| 0295–0296 | `frontend/src/components/Catalog.tsx` supports keyboard Enter navigation, EN/AR labels, RTL inputs, bilingual list display, edit/delete, decimalPlaces range and status. React search is client-side, server search is available. Product selectors are owned by WP16 and not claimed. |
| 0297–0298 | ASP.NET `CatalogValidationTests.cs` checks code and precision; Django `catalog/tests.py` checks bilingual search, normalized duplicate, product FK, 0–6 precision and permissions. |
| 0299 | Disposable SQL Server `smoke_sqlserver.py` checks API create/update/search, database precision CHECK, Product FK and negative cases; Playwright shared React browser runs against both backends and checks Arabic list labels and keyboard flow. |
| 0300 | Reviewed duplication, security, Unicode, SQL constraints, keyboard and deferred owners. CI 40170805039 passed all five jobs. |

## Explicit downstream dependencies

Product creation form and Brand/Unit selectors belong to **WP16 (ERP-0301–0320)**. Current Product API already references Brand/Unit through numeric IDs and is used in SQL/Django integration tests. Stock quantity, purchasing, sales, invoice printing and branch inventory are future work; no false acceptance claims. Multi-user audit history is WP46, pagination/performance hardening WP48, printing WP44.

**No production SQL Server was accessed.** All schema upgrade/rollback and SQL smoke tests run against disposable CI SQL Server.

## Verification gate

CI for implementation `e8cb36b5`: https://github.com/dharmendra1031/it-retail-erp/actions/runs/40170805039 — Django, ASP.NET, React, browser and SQL Server all **SUCCESS**. No production database accessed. Product form remains WP16.
