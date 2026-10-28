# ERP-0319–0340: Product concurrency and digital licenses

## Requirements, scope and acceptance

The SRS product sections require stock, non-stock service and digital types, optional digital license key/number and activation/expiry dates. Product Master owns type selection and license provisioning. Stock movement and quantity accounting are owned by WP21/WP25; sale of a non-stock service belongs to sales posting WP30. Those future flows must reject non-stock stock movements and must not alter quantity for a service sale. This package does not claim either runtime outcome yet.

Existing `Product` models and Product APIs already offered `stock`, `nonstock`, `digital` and blocked serial/reorder settings for the latter two. Before this batch, no persisted license lifecycle, secret protection, duplicate active key guard, permission-controlled reveal, or UI existed. The Product conflict tests lacked simultaneous SQL Server writer coverage.

The current acceptance path is: create an active digital Product, provision a license with a key or number and optional dates, list it without plaintext, reveal only with the separate permission, and revoke it. Reject a duplicate active key, invalid date order, non-digital Product, type change away from digital while licenses exist, and non-stock/digital serial or reorder settings. Revocation makes a key reusable; it does not delete the historical row. Stock ledger/sale effects remain the named downstream acceptance cases above.

## Data and security design

`ProductLicense` uses a numeric BIGINT identity, restrictive Product FK, Unicode `license_number` (100), optional AES-GCM encrypted key and HMAC-SHA256 fingerprint, optional date-only activation/expiry, active state and UTC timestamps. `PRODUCT_LICENSE_SECRET` is a deployment-supplied 32-byte base64 secret; both backends use the same fingerprint normalization. The filtered unique index on active non-null fingerprints enforces the duplicate rule under concurrent writes. CHECK constraints enforce digital type stock settings on Product and activation/expiry order and key-or-number presence on License. Names and license numbers are Unicode; money and stock DECIMAL precision in Product is unchanged. Neither response nor log should contain a plaintext key except the permission-gated reveal response, which sends `Cache-Control: no-store`. Key rotation needs a planned data migration because existing encrypted keys and fingerprints depend on this secret.

EF migrations `20261028150000_ProductTypeStockSettings` and `20261028160000_ProductLicenses` and Django migrations `0004_product_type_stock_settings` and `0005_product_license` add the corresponding constraints, table and index. Reversing either license migration drops license data, so rollback on a populated production database requires a separately approved data preservation plan. The test database upgrade succeeded. No production database was accessed.

## API contract

Both backends serve `GET /api/product-licenses?productId={positive BIGINT}`, `POST /api/product-licenses`, `GET /api/product-licenses/{id}`, `GET /api/product-licenses/{id}/reveal`, and `DELETE /api/product-licenses/{id}`. POST accepts `productId`, optional `licenseKey` (max 512), `licenseNumber` (max 100), and nullable ISO `activationDate`/`expiryDate`. At least a key or number is required. Standard responses contain numeric `id`, `productId`, `licenseNumber`, `hasKey`, dates, and `isActive`; only reveal returns `licenseKey`. Create returns 201, successful revoke returns 200 and is idempotent, missing ID returns 404, malformed input returns 400 `{ "detail": "Invalid request." }`, and active duplicate key returns 400 `{ "detail": "Active license key already exists." }`. Authentication, action permissions and CSRF apply; reveal requires `product-licenses.reveal`, while list/detail, create and revoke require their own `view`, `add`, `revoke` grants. The global Product Master has no branch FK; branch-specific stock and transaction scope belongs to later packages. License audit events belong to WP46; current rows preserve timestamps and revocation state.

## Verification and limits

- Release ASP.NET build: 0 warnings/errors; full local SQL Server suite: 22/22 passed. The Product tests include physical duplicate-index collisions and concurrent writer behavior.
- Django system check and migration drift check passed. Full SQLite suite: 97 tests, eight SQL-specific skips. Full local SQL Server suite: 97/97 passed, including license validation and Product concurrent duplicate handling.
- EF database update and pending-model check passed on disposable `ITRetailERP_Erp0320_Test`. Django SQL Server tests created and discarded their test database.
- React production build passed. Playwright against local Django on a disposable SQLite database: bilingual Product create, masked digital license lifecycle and Arabic RTL Product Master, 3/3 passed.
- ASP.NET HTTP smoke, physical schema checks and both backend SQL Server browser E2E require the pushed CI run. A local browser pass on SQLite does not establish SQL Server browser parity.

The Product search fixture and document series tests were made independent of persisted/concurrent test data after full-suite failures. No stock quantity or sale posting was implemented or reported as tested here.
