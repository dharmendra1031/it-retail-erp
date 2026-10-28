# ERP-0311 — Product Master API contract and parity review

**Source revision:** `674bc93cc054e7c7bd046a2434743e76e5546abb`, `development`. Source: original SRS §§4,12–14/42–43 as mapped in `ERP_0301_PRODUCT_SCOPE.md`; API code reviewed directly in ASP.NET `ProductsApiController.cs`, `ProductRequest.cs`, Django `catalog/api.py`, `config/api_urls.py` and `config/exceptions.py`. This document distinguishes **implemented** behavior from **target** behavior; a documented contract is not a passed runtime test.

## Routes and response status

| Method/path | Implemented in both | Response |
|---|---|---|
| GET `/api/products?search=term` | Yes; term matches SKU, Barcode, `NameEn` or `NameAr` | 200 JSON array sorted by SKU; no pagination yet |
| GET `/api/products/{id}` | Yes | 200 Product object; 404 when missing |
| POST `/api/products` | Yes | 201 Product object; 400 validation/duplicate |
| PUT `/api/products/{id}` | Yes | 200 Product object; 400 invalid/duplicate; 404 missing |
| DELETE `/api/products/{id}` | Yes | 204; 404 missing; referenced-record conflict handling needs lifecycle acceptance |

All routes omit trailing slash. An unauthenticated operation must return 401, insufficient permission 403, invalid anti-CSRF mutation 403. Permission policies are `products.view/add/edit/delete` in both APIs; no frontend-only permission bypass is acceptable.

## JSON contract (camelCase)

```json
{
  "sku": "LAPTOP-01",
  "barcode": "123456789012",
  "nameEn": "Laptop",
  "nameAr": "حاسوب محمول",
  "descriptionEn": "Portable laptop",
  "descriptionAr": "حاسوب محمول",
  "categoryId": 1,
  "brandId": null,
  "unitId": 1,
  "productType": "stock",
  "serialTracked": false,
  "costPrice": "250.000",
  "basePrice": "320.500",
  "minPrice": "300.000",
  "reorderLevel": "5.000000",
  "isActive": true
}
```

For reads, `id` is the additional positive, server-generated BIGINT identity field. The UI must reject unsafe JavaScript numbers. SKU and optional barcode are trimmed and uppercased; SKU permits `[A-Z0-9_-]{1,40}`, nonblank barcode permits `[A-Z0-9_-]{3,64}`. Blank barcode canonicalizes to null. Category and Unit are required active BIGINT references; Brand is an optional active reference. `productType` is one of `stock`, `nonstock` or `digital`; nonstock/digital must not have serial tracking or nonzero reorder level. Prices are nonnegative three-decimal fixed-point strings in responses; reorder level has six decimals; `minPrice <= basePrice`. Arabic fields are Unicode and optional under current API policy.

## Error contract and **observed parity gaps**

**Target:** `{ "detail": "Invalid request." }` for invalid input; `{ "detail": "SKU or barcode already exists." }` for duplicate identifier; no stack traces or SQL constraint details. A 400/403 must never mutate existing Product data. Backend error response shapes must remain usable by `frontend/src/api/client.ts`.

- ASP.NET currently catches duplicate SKU/barcode through preflight `AnyAsync` but **not** late `DbUpdateException` from concurrent writes. Its `Valid` returns generic 400; auth/CSRF through ASP.NET policies/antiforgery.
- Django `ProductSerializer.validate_sku/barcode` uses field validation but `config.exceptions.api_exception_handler` collapses field errors to `{detail:"Invalid request."}`. `CatalogViewSet.create/update` catches `IntegrityError` inside `transaction.atomic` and returns 400 `Invalid request.` on a database collision. Both need consistent duplicate conflict detail and physical SQL Server race tests in ERP-0312–0313/0319.
- ASP.NET and Django do not currently support separate Item Code, Model, wholesale and purchase price, tax category/percent, warranty period or opening/current stock as Product JSON fields. Those **must not** be silently added with fabricated mappings; see decisions/ownership in `ERP_0306_PRODUCT_DATA_DESIGN.md`. Tax belongs WP18, stock ledger WP21/25, warranty WP23, multiple prices WP20.
- Product pagination and its response shape require a synchronized contract before UI (ERP-0315), with broad performance coverage in WP48. Do not change all other Catalog endpoints accidentally.

## Acceptance checks before WP16 signoff

Test successful bilingual Product create/read/update, duplicate SKU/barcode, nonexistent/inactive Category/Brand/Unit, invalid money/quantity and type, unauthorized/CSRF reads and writes, concurrent inserts, Unicode/precision readback, and identical frontend-visible errors against ASP.NET/Django with disposable SQL Server. Existing CI 40649719993 passed before this documentation-only step. No runtime contract changes, migration or production SQL access in ERP-0311.
