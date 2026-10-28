# ERP-0308 — ASP.NET Product entity, contract and search repair

**Reviewed source:** `Models/Product.cs`, `Contracts/ProductRequest.cs`, `Data/ApplicationDbContext.cs`, `Migrations/20261023140000_Products.cs`, `Controllers/Api/ProductsApiController.cs`, and `tests/ITRetailERP.Tests/ProductSearchTests.cs`. Base commit `1f0aa9f82fb6485ef39e351daa56ae8ed5990ffe` on `development`.

## Entity, contract and database review

Existing Product uses a `long`/SQL `BIGINT IDENTITY` primary key; required unique normalized SKU; optional unique barcode; separate English/Arabic name and description fields; required Category/Unit and optional Brand FKs; stock/nonstock/digital type; three-decimal cost/base/min prices, six-decimal reorder, active status and UTC timestamps. `ProductRequest` and `ProductResponse` expose numeric IDs and exact decimal string responses. EF `ApplicationDbContext` and Product migration already declare the relevant unique indexes, precision and restrictive FKs. No approved new Product field or index exists from ERP-0306, so an entity/contract/schema change or empty migration is N/A here.

`ProductsApiController` already supports list/detail/create/update/delete, permission policies and antiforgery on writes. Source audit found list `?search=` matched only SKU. ERP-0301/0303 require Product name and barcode search for this package. The list predicate now matches SKU, non-null barcode, English name or Arabic name after trimming the query term. It keeps existing ordering and response shape. Separate Item Code remains an unresolved D1 policy; no alias or new column was invented.

## Red-green evidence

Added `ProductSearchTests.ListFindsProductByEnglishNameArabicNameAndBarcode` against a disposable LocalDB SQL Server database (`ITRetailERP_ProductSearchTest`). The test opens a transaction, inserts active Category/Unit and a Product with English/Arabic names and alphanumeric barcode, then invokes the real `ProductsApiController.List` with each search term. It rolls the fixture back. Before the code change, the test failed with `Assert.Contains() Failure: Filter not matched in collection; Collection: []` at `ProductSearchTests.cs:51`. The cause was the SKU-only predicate in `ProductsApiController.List`.

After the predicate change, `dotnet test tests/ITRetailERP.Tests/ITRetailERP.Tests.csproj -c Release --logger 'console;verbosity=minimal'` passed **12/12** against the dedicated test database. `dotnet build src/ITRetailERP.Web/ITRetailERP.Web.csproj -c Release --no-restore` succeeded with **0 warnings, 0 errors**. EF migrations were applied to this local test database before the red run. No production database was accessed. The new test proves SQL query translation and returned Product rows, not HTTP authorization/CSRF or Django parity.

## Remaining WP16 gates

Django `ProductViewSet.get_queryset` still filters SKU only; ERP-0309 owns matching search and its test. Both backends still need the shared Product error contract, late unique-constraint handling, broader Product validation, permissions, React Product UI and two-backend SQL/E2E proof under ERP-0311–0320. Search remains unpaginated; Product UI pagination belongs ERP-0315 and broad pagination policy WP48. The unresolved Item Code/Model/price/tax decisions in ERP-0306 remain open before claiming full SRS Product Master delivery. No stock or financial transaction behavior changed.
