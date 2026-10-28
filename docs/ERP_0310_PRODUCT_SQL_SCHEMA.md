# ERP-0310 — Product Master SQL Server schema and migration verification

**Reviewed revision:** `7dfb38980df11c3763cf8a9bcafd62cde7597541` on `development`.  
**Verified CI:** [40649242422](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40649242422): **5/5 SUCCESS** (ASP.NET, Django, React, browser and disposable SQL Server).  
**Scope:** Product fields, unique indexes, protected foreign keys, database parity and existing migration rollback/reapply; not new business features.

## Existing migrations inspected

- **ASP.NET Core:** `aspnet-core/src/ITRetailERP.Web/Migrations/20261023140000_Products.cs`, `Data/ApplicationDbContext.cs`. The Product primary key is `BIGINT IDENTITY`, with NVARCHAR EN/AR names/descriptions, a unique SKU index, a filtered unique non-null barcode index, restrictive Category/Brand/Unit foreign keys, price `decimal(18,3)` and reorder `decimal(18,6)`.
- **Django:** `django/apps/catalog/migrations/0002_product.py`, `apps/catalog/models.py`. The Product model uses `BigAutoField`, Unicode `CharField`, unique SKU, optional unique barcode, PROTECT FKs, three-place price and six-place reorder decimals. SQL Server actually materializes Django decimal fields as `numeric`, an exact synonym for SQL Server `decimal`.
- Original Product schema/indexes support the **approved core fields** and both four-field search predicates from ERP-0308/0309. There is no approved Product schema change requiring a new EF or Django migration in ERP-0310. Business decisions on separate Item Code, Model, price lists, tax and warranty remain explicitly deferred.

## New executable verification

Added `aspnet-core/tests/product_schema_sqlserver.py` to the SQL Server CI job in `.github/workflows/erp-verification.yml`. It requires `GITHUB_ACTIONS=true`, the exact CI Django DB name `erp_integration`, and connects only to the local disposable SQL instance. For **both** `erp_integration.catalog_product` and `erp_net_ci.Products`, it checks:

1. Numeric Product `BIGINT IDENTITY` key.
2. Column presence/nullability and `NVARCHAR` lengths for SKU, optional barcode and bilingual names/descriptions.
3. Exact `NUMERIC/DECIMAL(18,3)` price and `(18,6)` reorder metadata without falsely distinguishing SQL Server's equivalent type aliases.
4. Unique single-column SKU and **filtered unique non-null barcode** indexes (multiple absent barcodes remain possible).
5. Database foreign keys to Category, Brand and Unit with `NO_ACTION` delete behavior (protect referenced masters).

### Test outcome and correction

First test CI [40648922891](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40648922891) failed on a **test assumption**: Django SQL Server described cost price as `numeric` rather than `decimal`. This was not evidence of different stored precision or a schema defect. Commit `7dfb3898` adjusted the test to accept both exact equivalents while retaining strict digit/scale checks.

The corrected commit's CI [40649242422](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40649242422) passed the new physical Product schema check for **both databases** and all five overall jobs. SQL Server tests also executed the existing Django `catalog` migration reversal to `0001` and reapplication, and EF reversal to `20260918070000_InitialCreate` and reapplication **in disposable CI databases only**.

## Safety / residual work

No new migration, application schema, production SQL data or deployed database was modified. Existing initial `Down` migrations can drop data and are **not** an authorized production rollback. Product API validation rules (negative prices, `min <= base`, product type rules and inactive references) are not physical Product SQL CHECK constraints; do not describe them as database guarantees. ERP-0311–0313 own uniform API error handling/parity; ERP-0317–0319 own further end-to-end Product validation, concurrent writes and Unicode round-trips, and ERP-0315 owns Product UI. Physical schema parity and existing upgrade/reapply are verified here, but Product Module as a whole is not yet acceptance-complete.

**Next:** ERP-0311, document the identical Product API contract and error/status handling between backends.
