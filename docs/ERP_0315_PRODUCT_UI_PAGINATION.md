# ERP-0315 — Product Master React UI and optional server pagination

**Reviewed source commit:** `c74ac6339d74d1f3ef62a65d86e184c39bfd1fc6` on `development`. **Verified CI:** [40660099435](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40660099435) — **5/5 PASS** (ASP.NET, Django, React build, Playwright browser and SQL Server integration including React against ASP.NET).

## Product UI delivered

- `frontend/src/api/products.ts`: typed `ProductValues`/Product API client; uses the existing credential/CSRF request helper. Validates nested Product numeric IDs are safe integers.
- `frontend/src/components/Products.tsx`: Product Create/Edit/Delete, English/Arabic names/descriptions, SKU/Barcode, active Category/Brand/Unit selectors, stock/nonstock/digital dropdown, serial flag, three-decimal prices, six-decimal reorder level and Active status. Product type switch automatically clears incompatible inventory fields. Reuses existing CSS classes and `advanceOnEnter` keyboard handler; no new framework or additional CSS.
- `frontend/src/App.tsx` and `components/AppShell.tsx`: Admin Product Master route/navigation. `frontend/src/i18n.tsx` adds matching English and Arabic labels/error translations, including duplicate SKU/Barcode.
- Product list has server-backed SKU/Barcode/EN/AR-name search, total count, current page and Previous/Next controls; page size is 25.

## Backend pagination — new optional contract

Both ASP.NET `ProductsApiController.List` and Django `ProductViewSet.list` accept optional `page` and `pageSize` query parameters (default `page=1`, `pageSize=25`, range 1–100). **When paging is supplied**, GET `/api/products?page=1&pageSize=25&search=...` returns:

```json
{"items":[],"total":0,"page":1,"pageSize":25}
```

Both apply the four-field search before counting and only fetch the current page. Invalid page/size yields HTTP 400 `{detail:"Invalid request."}`. Existing unpaged GET `/api/products` continues returning a JSON **array** to preserve earlier API callers/tests; broad pagination migration belongs WP48. No SQL schema migration was needed; the unique SKU index supports stable ordering.

## Test evidence

- `django/apps/catalog/tests.py`: Product API paging, total, ordering across pages and invalid bounds.
- `aspnet-core/tests/ITRetailERP.Tests/ProductSearchTests.cs`: Product list paging JSON, numeric identity and invalid page.
- `frontend/e2e/erp.spec.ts`: actual React browser creates Category and Unit, opens Product Master, selects required masters, enters bilingual SKU/Barcode/price values, creates Product then searches it.
- Initial browser run [40659759197](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40659759197) exposed a dropdown accessible-name mismatch (`getByLabel("Category", exact:true)` timed out). Product dropdowns now have explicit accessible labels; final run **40660099435** passed all five jobs. Also verifies shared React against real ASP.NET with disposable SQL Server.

## Limitations and ownership

Current Product screen navigation is Admin-only because `CurrentUser` exposes `isAdmin`, not granular Product grants. Non-admin with `products.view` **can use the authorized backend** (proved ERP-0314), but lacks permission-aware UI navigation/read-only form; do not claim it is implemented. This UI authorization parity needs a subsequent integration/role-navigation repair. Product transactions, license provisioning, stock ledger, tax, multi-price, warranty and audit are not in WP16 UI and remain their later work packages. The current screen is one Product Master entry form, not a stock/sales screen. Financial audit and stock branch isolation are not yet built.

No production DB accessed; schema unmodified. Next ERP-0316: bidi/RTL, decimal display, focus and responsive accessibility verification.
