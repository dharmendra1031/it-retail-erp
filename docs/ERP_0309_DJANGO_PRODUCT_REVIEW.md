# ERP-0309 — Django Product model, serializer and search parity

**Reviewed source:** `django/apps/catalog/models.py`, `api.py`, `migrations/0002_product.py`, `tests.py`, `django/config/api_urls.py`, and ASP.NET `ProductsApiController.List` at base commit `5549c127a3b39ec56514682f92e570acafe1dc45`.

The Django `Product` model and serializer already provide a numeric `BigAutoField` ID, required unique normalized SKU, optional unique barcode, English/Arabic names and descriptions, active Category/Unit and optional Brand relationships, stock/nonstock/digital type, exact decimal price/reorder fields and active status. `0002_product.py` represents those fields and PROTECT FKs. The `products` router exposes list/detail/create/update/delete. No new schema field, index or serializer contract is justified by search parity; migration action is N/A for ERP-0309.

## Search repair and red-green evidence

`ProductViewSet.get_queryset` previously filtered only `sku__icontains`. ASP.NET ERP-0308 added SKU, barcode, English name and Arabic name matching. The Django predicate now combines the same four fields with `Q(...__icontains=search)` after trimming the term; ordering and response fields remain unchanged.

Added `ProductApiTests.test_product_search_finds_english_arabic_name_and_barcode`. It creates a Product through the real API with an English name that does **not** occur in its SKU, then GETs the list by an English-name fragment, the Arabic name and the barcode. Before the fix, all three subtests returned an empty list instead of the created numeric ID. After the fix, the full Django test command below passed **85 tests, 7 skipped, 0 failures**. The skipped tests require SQL Server and were not claimed as passes.

```powershell
$env:SECRET_KEY='local-test-only-key'
.\.venv\Scripts\python.exe manage.py test apps.core apps.accounts apps.companies apps.partners apps.catalog --settings=config.settings_test --verbosity 1
.\.venv\Scripts\python.exe manage.py check --settings=config.settings_test
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run --settings=config.settings_test
```

`manage.py check` reported no issues; `makemigrations --check --dry-run` reported no changes. Tests used the isolated in-memory SQLite database from `settings_test.py`; no production SQL Server or data was accessed. This proves Django API search behavior under the test backend, while physical SQL Server index/Unicode behavior and cross-backend API parity remain ERP-0310/0319 gates.

Remaining WP16 work: shared Product error/status contract and race handling (ERP-0311–0313), Product permission/CSRF negatives (ERP-0314/0317–0319), React Product UI and selectors (ERP-0315–0316), and two-backend SQL/E2E acceptance. Separate Item Code/Model/price/tax policy decisions from ERP-0306 are still unresolved. No stock or financial behavior changed.
