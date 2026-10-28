# ERP-0313 — Django Product duplicate error parity and transaction safety

**Source commit:** `b6e818c786f194377d590de5e0084f90fe1c7b3e` on `development`. **CI:** [40657866476](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40657866476) — 5/5 jobs SUCCESS, including Django unit tests in SQLite and disposable SQL Server and existing Product schema tests.

## Changes

- `django/apps/catalog/api.py`: ProductSerializer now applies one explicit SKU/barcode uniqueness message (`SKU or barcode already exists.`) for both fields. The DRF auto-generated Barcode `UniqueValidator` was disabled for Product only, so the product's existing custom `validate_barcode` owns the field error and matches ASP.NET. SKU is also validated through its own custom validator.
- `django/config/exceptions.py`: allows that precise Product duplicate detail through the existing consistent `{detail:...}` API error formatter. Other field-validation failures remain a generic safe `Invalid request.`.
- `CatalogViewSet` already runs create/update within `transaction.atomic` and catches `IntegrityError`. For Product only, it now maps a demonstrable SQL Server 2601/2627 or SQLite UNIQUE collision to the same 400 duplicate detail; unrelated database integrity errors retain generic 400 instead of being mislabelled as duplicate. Non-Product catalog APIs keep their previous messages.
- `django/apps/catalog/tests.py`: Product API test asserts the exact 400 response for duplicate SKU and duplicate Barcode; also verifies two distinct SKUs with empty barcode both create and return `null`. Real SQL Server unique nullable Barcode index and FK metadata were previously validated in ERP-0310.

## Red/green evidence

First CI [40657648527](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40657648527) failed in both Django SQLite and SQL Server tests: duplicate Barcode went through DRF's implicit UniqueValidator and returned `Invalid request.`. This demonstrated a true API parity bug. Revision `b6e818c7` disabled the redundant automatic field validator and retained explicit duplicate checking. CI [40657866476](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40657866476) passed all five jobs, including Django in both DB environments. Existing SQL Server migrate/reapply and ASP.NET integration tests also passed.

## Boundaries

No Product migration or physical schema change; no stock, pricing, tax or license lifecycle operation. Product Master does not post financial documents, so generic request-id/idempotency tokens are outside WP16; duplicate natural SKU/Barcode prevent repeated Product creation, while PUT targets one numeric Product ID. Cross-process concurrent HTTP create/update still needs explicit stress tests in ERP-0319. Unauthorized/CSRF Product-specific proofs are ERP-0314. Product UI and accessibility are ERP-0315/0316. Production SQL Server not touched.

**Next:** ERP-0314 authorization/scope/audit ownership and security acceptance.
