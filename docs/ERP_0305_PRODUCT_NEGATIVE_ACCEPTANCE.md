# ERP-0305 — Product negative and authorization acceptance specification

**Trace:** WP16 negative proof in `ERP_PLAN_1000_STEPS.md`; SRS Product/Item Master and permissions baseline in `SRS_BASELINE.md`; `ERP_0301_PRODUCT_SCOPE.md`; positive fixture in `ERP_0304_PRODUCT_HAPPY_PATH.md`. This is an executable test design, not a runtime pass. The linked original SRS was unavailable during this review; repository requirement extraction is the source used here.

## Shared setup and invariant

Run every case against separate disposable, migrated SQL Server databases for ASP.NET Core and Django. Create active Category, Unit and optional Brand records, plus one valid Product using the ERP-0304 fixture. Use distinct candidate SKUs/barcodes for independent cases. Authenticate through each backend's session flow and include valid CSRF state except where a case intentionally omits it. Capture the baseline Product row and total count before each request. A rejected create must leave the total count and all existing rows unchanged; a rejected update must preserve every previously saved field. Verify through a fresh API GET and SQL readback, not only a 4xx response. Never point tests at production.

| Case | Request variation from the valid stock Product | Expected result and persisted-state assertion |
| --- | --- | --- |
| NEG-P01 normalized duplicate SKU | POST with SKU differing only in case/outer whitespace from the seeded Product; use a new barcode | 400; no second Product; seeded row unchanged. Both APIs must enforce uppercase normalization and the SQL unique index must protect a race. |
| NEG-P02 duplicate barcode | POST with new SKU but barcode differing only in case/outer whitespace from the seeded Product | 400; no second Product; seeded barcode unchanged. Test non-numeric legal barcode characters as well as the numeric fixture so case normalization is meaningful. |
| NEG-P03 negative price | POST with `costPrice: "-0.001"` and new identifiers | 400; no Product row. Repeat for negative base/min price as separate parameterized cases. |
| NEG-P04 bad precision or ordering | POST with `basePrice: "320.5001"`; then `minPrice: "321.000"` while base remains `"320.500"` | 400 for each; no new row; no silent rounding or clamping. |
| NEG-P05 missing or invalid category | POST without `categoryId`, then with zero, nonexistent ID and inactive Category ID | 400 for each; no Product row or FK side effect. Required active Unit and invalid optional Brand are analogous relationship cases. |
| NEG-P06 unsupported type settings | POST `productType: "nonstock"` with `serialTracked: true`, or `productType: "digital"` with nonzero `reorderLevel` | 400; no Product row. This checks current WP16 master validation, not later type-specific stock/license behavior. |
| NEG-P07 malformed identifiers | POST SKU outside `[A-Z0-9_-]{1,40}` or nonblank barcode outside `[A-Z0-9_-]{3,64}` | 400; no Product row. |
| NEG-P08 rejected update | PUT an existing Product with duplicate normalized SKU/barcode or invalid price/category | 400; original Product's SKU, barcode, bilingual text, prices, FKs and update timestamp remain unchanged. |

For each 400, compare the two backends' documented error contract. Current source already differs: ASP.NET `ProductsApiController` returns `{ "detail": "SKU or barcode already exists." }` or `{ "detail": "Invalid request." }`, while Django `ProductSerializer` may return field-specific errors and `CatalogViewSet` maps late `IntegrityError` to a generic detail. ERP-0311–0313 must settle and implement the shared response contract before claiming parity. Do not treat any 400 alone as full acceptance.

## Authorization and CSRF cases

1. **Unauthenticated create:** POST a valid Product with no session. Expect **401** under the shared API contract and no new row.
2. **Authenticated but denied create:** Create a non-admin user whose role grants `products.view` but lacks `products.add`. With valid CSRF state, POST a valid Product. Expect **403**, no row. Verify the same user can read the seeded Product to distinguish permission denial from login failure.
3. **Denied edit and delete:** For a user lacking `products.edit`/`products.delete`, PUT and DELETE the seeded Product with valid CSRF state. Expect **403** and an identical saved row. A user with only `products.add` must not gain edit/delete implicitly.
4. **CSRF denial:** As an otherwise authorized user, submit POST/PUT/DELETE without the required CSRF token. Assert a 4xx denial and unchanged SQL state. Record exact backend statuses and align the common contract in ERP-0311; do not assume the two frameworks currently emit the same CSRF code.
5. **Read denial:** An authenticated user without `products.view` must receive **403** on list/detail. A 401 for an unauthenticated reader remains a separate check.

ASP.NET source uses `products.*` policies on each action and antiforgery on writes; Django `CatalogPermission` resolves `products.view/add/edit/delete` through role permissions and session CSRF. Source presence is not a runtime authorization proof. Product-specific restricted-role, CSRF and no-mutation checks belong to ERP-0314/0317–0319. Persistent denied-action audit evidence belongs WP46 and is not claimed here.

## Concurrent uniqueness and database proof

Send two simultaneous authenticated POSTs with the same normalized SKU but different barcodes, then repeat with different SKUs and the same normalized barcode. Exactly one request may create a row. The other must produce the agreed controlled 400 response, never an unhandled 500; SQL must contain exactly one matching identifier and no partial row. Repeat a conflicting PUT against an already saved Product and assert its old values survive. EF Product writes currently lack late `DbUpdateException` translation, while Django catches `IntegrityError`; ERP-0312–0313 own the fix, and ERP-0319 owns disposable SQL concurrency proof.

EF `ApplicationDbContext.cs`/`20261023140000_Products.cs` declare unique SKU and filtered non-null barcode indexes and restrictive Category/Brand/Unit FKs. Django `catalog.Product`/`0002_product.py` declare unique SKU/barcode and PROTECT FKs. Verify physical migrated SQL Server constraints, numeric BIGINT IDs, NVARCHAR preservation and exact decimal(18,3)/decimal(18,6) values during ERP-0310/0319. No stock or ledger mutation is part of these master-data denials; those later transactional effects remain owned by WP21/WP25.

**ERP-0305 completion criterion:** this specification is recorded with source evidence and owners. The negative cases themselves remain **unverified** until both APIs, disposable SQL Server and the shared React UI (where applicable) execute them and report exact results. Existing Django Product tests and ASP.NET SQL smoke cover a subset, not this complete matrix.
