# ERP-0304 — stock Product happy-path acceptance specification

**Trace:** SRS §§4, 12–14, 42–43; `SRS_BASELINE.md` AT-01 Product creation portion; WP16 ERP-0301–0320. This document defines an executable acceptance case. It does not claim that the case has passed. The original linked SRS could not be fetched in this environment; `ERP_0301_PRODUCT_SCOPE.md` and `ERP_0303_PRODUCT_GAP_MATRIX.md` provide the repository requirement trace.

## HP-Product-01: create and retrieve a bilingual stock item with barcode

### Preconditions

1. Use separate disposable SQL Server test databases for ASP.NET Core and Django. Apply each backend's current migrations. Never use a production or shared developer database for this acceptance case.
2. Create an authenticated administrator or a user granted `products.add` and `products.view`; obtain the backend's session/CSRF token through the normal login flow. Point the same React frontend at each backend in separate runs.
3. Create active Category and Unit masters, plus an active Brand. Record their positive numeric IDs. Use a fresh SKU and barcode per isolated test run; do not rely on hard-coded IDs or an empty database.
4. Run Product API tests directly and, once the Product screen exists (ERP-0315), run the same case through React. Retain request/response and SQL readback evidence for both backends.

### Input fixture

Submit `POST /api/products` with JSON shaped as follows, substituting the three master IDs and a run-unique SKU/barcode suffix. Money and quantity values are decimal **strings** in the API fixture.

```json
{
  "sku": "laptop-accept-01",
  "barcode": "123456789012",
  "nameEn": "Laptop",
  "nameAr": "حاسوب محمول",
  "descriptionEn": "Portable computer",
  "descriptionAr": "حاسوب محمول للاختبار",
  "categoryId": 1,
  "brandId": 2,
  "unitId": 3,
  "productType": "stock",
  "serialTracked": true,
  "costPrice": "250.000",
  "basePrice": "320.500",
  "minPrice": "300.000",
  "reorderLevel": "5.000000",
  "isActive": true
}
```

The numbers `1`, `2` and `3` illustrate the payload shape only. Actual IDs come from the created master records. The chosen SKU is deliberately lowercase to verify uppercase normalization. The Arabic text must be compared as Unicode characters, not transliterated or visually approximated.

### Actions and exact assertions

1. Create the Product with a valid CSRF token. Assert **201 Created**, a positive numeric `id`, `sku` normalized to `LAPTOP-ACCEPT-01` (or the run-specific uppercase value), and barcode preserved. Assert no UUID or string ID is substituted.
2. Assert the response contains the exact English and Arabic names and descriptions, the three selected master IDs, `productType: "stock"`, `serialTracked: true`, `isActive: true`, and fixed-point strings `costPrice: "250.000"`, `basePrice: "320.500"`, `minPrice: "300.000"`, `reorderLevel: "5.000000"`. Compare the field names, types and values across backends.
3. Fetch `GET /api/products/{id}` as an authorized reader. Assert **200 OK** and the same values after a new request. Fetch `GET /api/products?search=<SKU>` and assert exactly one matching Product in this isolated fixture. Name and barcode search are separately due in WP16; this step does not claim that they currently work.
4. Query the corresponding SQL Server test database after the API request. Assert exactly one Product row for the normalized SKU, an auto-generated `BIGINT` ID, exact NVARCHAR Arabic fields, exact decimal(18,3) prices and decimal(18,6) reorder value, and FKs pointing to the created masters. Check the unique SKU/barcode indexes and restrictive FKs against the migrated schema.
5. After ERP-0315 delivers the shared Product UI, repeat creation with keyboard-only navigation in English and Arabic/RTL. Assert the correct API request, visible success state and persisted row after reload on both backend targets. Capture browser results separately from direct API results.

### Completion evidence and boundaries

Record backend target, migration command/result, test database identifier, API/SQL assertion output, Product test file paths and React Playwright trace/results. ERP-0317–0319 own executable ASP.NET, Django, SQL Server and browser proof; ERP-0320 closes WP16 only after applicable positive and negative gates pass. The existing Django Product test and ASP.NET SQL smoke cover parts of this path but do not cover all response fields, SQL readback and React Product creation on both backends.

This case creates a **master record only**. It must not invent or assert opening/current stock, a purchase posting, warranty assignment or tax calculation. SRS AT-01 stock increase remains pending WP21/WP25, and tax, serial/warranty and selling lifecycle belong to their named packages. Item Code versus SKU, separate purchase/cost price and required leaf-category policy remain open decisions from ERP-0301/0306; the fixture uses the existing API fields without deciding those policies.
