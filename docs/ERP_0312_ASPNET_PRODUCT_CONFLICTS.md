# ERP-0312 — ASP.NET Product mutation safety and duplicate-race handling

**Implemented revision:** `2497bb6ff95c808601e4d0b2462195c1e57234db` on `development`. **CI:** [40656984940](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40656984940) — 5/5 jobs successful, including disposable SQL Server Product conflict tests.

## Runtime fix

Updated `aspnet-core/src/ITRetailERP.Web/Controllers/Api/ProductsApiController.cs` to translate late SQL Server constraint exceptions **only** when the driver reports a known error number:

- SQL Server **2601/2627** (unique index/constraint collisions during Product create or update): HTTP 400 `{ "detail": "SKU or barcode already exists." }`. Existing early SKU/Barcode preflight remains, but database uniqueness protects a race after preflight.
- SQL Server **547** (FK/check constraint collision during create/update): HTTP 400 `{ "detail": "Invalid request." }`; during delete: HTTP 409 `{ "detail": "Record is in use." }`.
- Any other `DbUpdateException` is not caught and will still fail loudly for triage. The code does not suppress unexpected SQL failures or introduce unnecessary service/transaction layers.

## Regression proof

Added `aspnet-core/tests/ITRetailERP.Tests/ProductConflictTests.cs`. Two direct-controller integration cases use the SQL Server database configured by `ConnectionStrings__DefaultConnection` and an explicit rolled-back transaction. A pending duplicate Product is invisible to the API preflight query, causing the **physical unique SKU or barcode index** to reject a second insert during `SaveChangesAsync`. Both attempts must produce a clean 400 with exact duplicate error detail and leave no Product rows written. No production database is used.

**Verified:** CI 40656984940: ASP.NET build, Django suite, React production build, browser suite and SQL Server job PASS. SQL Server job also passes Django/EF migration replay, dual Product physical schema inspection and .NET tests. This is a strong controlled late-conflict regression but does not simulate two independent HTTP sessions racing; real concurrent HTTP acceptance remains ERP-0319.

## Idempotency and ownership

Product Master create uses a unique natural SKU (plus unique optional Barcode); a repeated create with the same identifier returns 400 rather than double-inserting, while PUT remains a full replacement of the same numeric ID. Product Master does not allocate document numbers or post inventory/accounting state. Financial transaction idempotency is owned by later sales/purchase/inventory packages; do not add a generic idempotency framework here.

No change to EF/Django migrations, Product pricing, authorization policies, stock state or frontend UI. The Product interface/API remains behind existing permissions and CSRF. Next: ERP-0313 Django parity, transaction safety and error contract.
