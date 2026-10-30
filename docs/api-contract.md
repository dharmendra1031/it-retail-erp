# API contract

Both backend implementations expose the same endpoints used by the React frontend.

## Authentication

- `GET /api/auth/csrf`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/logout`

State-changing requests send the CSRF token in the `X-CSRF-TOKEN` header.

## Company Master

- `GET /api/companies`
- `GET /api/companies/{id}`
- `POST /api/companies`
- `PUT /api/companies/{id}`
- `DELETE /api/companies/{id}`

Create and update requests use multipart form data so the company logo can be uploaded with the same request.

## Role Master

- `GET /api/roles` — list roles
- `GET /api/roles/{id}` — role detail
- `POST /api/roles` — create
- `PUT /api/roles/{id}` — rename
- `DELETE /api/roles/{id}` — remove if unassigned

Role JSON: `{ "id": 1, "name": "Cashier" }`. Create/update use JSON `{ "name": "Cashier" }`. Access requires Admin (Django superuser or Admin role, ASP.NET Core Identity Admin role). Admin role cannot be modified or deleted. Duplicate names return 400, assigned role deletion returns 409.

Company reads require login; create/update/delete require Admin. Authentication responses include `isAdmin` boolean. Both backends use the same CSRF header for mutations.

All entity IDs are numeric auto-increment values.


## Validation/error contract

Both APIs return `{ "detail": "Invalid request." }` for malformed or missing required fields. The duplicate-role condition returns `{ "detail": "Role name already exists." }`. Unauthorized (401), forbidden (403) and missing resources (404) use the HTTP status with an empty payload. Role delete while assigned returns 409 and an explanatory `detail`. Backend-native field-level validation text is intentionally not exposed by this minimal shared contract.

Full financial/stock transaction response schemas and human-readable document references depend on the owning business modules and decision DEC-05; they are not yet implemented.

## Document sequences (internal service)

There is no public number-reservation endpoint. Both backends implement SQL Server transaction-locked `DocumentSequences` counters scoped by `series`, `fiscalYear` and `branchId`. Numeric database keys stay auto-increment `BIGINT`. Formatting, branch prefixes and period resets remain a separate configuration/business approval, never encoded in database IDs.


## Current frontend validation feedback

The shared TypeScript client reads the `detail` field of JSON error responses. Role Master displays duplicate/assigned role errors, and Company Master displays backend validation messages. The client does not render raw HTML error responses. This is for the current foundational endpoints; stock/financial document errors belong to their future modules.


## Authentication and session lifecycle (WP05)

- `GET /api/auth/csrf` returns `{ "csrfToken": "..." }`. React refreshes the token after login (Django rotates it when signing in).
- `POST /api/auth/login` accepts `{ "email": "...", "password": "...", "rememberMe": false }`; successful response `{ "id": number, "name": string, "email": string, "isAdmin": boolean }`.
- `GET /api/auth/me` returns that user object with a valid session; `POST /api/auth/logout` returns 204. Missing/expired session gives 401.
- Invalid password returns 401; five failures lock an existing account for 15 minutes. Invalid payload returns `400 { "detail": "Invalid request." }`; CSRF failures return **403**, with no sensitive server details. Both implementations use `X-CSRF-TOKEN` for unsafe methods.
- Session lifetime 30 minutes. `rememberMe` keeps the cookie across browser restarts until expiry; without it the cookie is session-only. The React app handles 401 on protected API requests by returning to Login.


## Authentication security (WP05)

`GET /api/auth/csrf` returns `{ "csrfToken": "..." }`; `POST /api/auth/login` accepts `{ "email": "...", "password": "...", "rememberMe": false }` and returns the same current-user payload as `GET /api/auth/me`: numeric `id`, `name`, `email`, `isAdmin`. `POST /api/auth/logout` returns 204. All mutating requests require `X-CSRF-TOKEN`; invalid/missing CSRF returns 403. Bad credentials/locked account and expired sessions return 401. Five wrong passwords lock an existing account for 15 minutes. Idle session lifetime is 30 minutes; remember-me persists the cookie for that duration, without remember-me it is a browser-session cookie. React returns to Login when a previously authenticated API reports 401.

For current API JSON numeric IDs, frontend rejects values outside JavaScript's safe-integer range rather than silently rounding SQL BIGINT. Future monetary endpoints must use decimal storage and exact decimal strings/approved precision; financial and KWD calculations are **not yet part of the current master endpoints**. English/Arabic UI labels and RTL keyboard forms are included on Login, Company and Role; full translated reports remain later work.


## Permissions / Role grants (WP06–WP07)

`GET /api/permissions` lists supported action codes. `GET /api/roles/{id}/permissions` and CSRF-protected `PUT /api/roles/{id}/permissions` read/replace grants with `{permissions: string[]}`. Unknown codes yield 400, non-admin requests 403, missing roles 404. Role-grant data is persisted in Django `Role.permissions` M2M and ASP.NET `AspNetRoleClaims` using `erp.permission` claim type; no separate runtime table is required by WP07.


## Customer and Supplier Masters (WP12–WP13)

`GET/POST /api/customers`, `GET/PUT/DELETE /api/customers/{id}`; equivalent routes under `/api/suppliers`. All mutation requests use JSON plus session CSRF. Admin may manage; delegated actions require `customers.view/add/edit/delete` or `suppliers.view/add/edit/delete` policies. Create returns 201 and numeric `BIGINT` identity; update 200, delete 204, invalid/duplicate 400, unauthorized/forbidden 401/403, missing 404, protected records 409.

Both master types accept: `code, nameEn, nameAr, addressEn, addressAr, mobile, telephone, contactPerson, remarks, paymentTermsDays, isActive`. Customer adds `companyName, civilId, customerType, email, taxNumber, creditLimit, openingBalance`; Supplier adds `email, taxNumber, creditLimit, openingBalance`. Customer requires nonblank English/Arabic names and mobile per SRS §8. Supplier's Arabic name and mobile are optional. Names, addresses and remarks preserve Unicode; machine-readable codes use ASCII letters/digits/underscore/hyphen, uppercase, maximum 30 characters and are unique per master. Supported Customer types include `retail/wholesale/corporate/cash/credit/individual/company/government/other`. `paymentTermsDays` is 0–365; an approved credit-period policy is downstream.

Both backends accept monetary input as decimal JSON strings and return fixed-point `"0.000"` strings; `creditLimit` and `openingBalance` are nonnegative `DECIMAL(18,3)`. Optional email may be blank, but malformed nonblank email must return 400. ASP.NET and Django persist common English/Arabic and additional SRS fields; status/error contract uses `{ "detail": "Invalid request." }` for invalid input, with additional duplicate-code text as applicable. A granted non-admin Customer reader must **not** receive `civilId` in responses.

### Protected partner documents

`GET/POST /api/{customers|suppliers}/{id}/documents`, and `GET /api/{customers|suppliers}/{id}/documents/{documentId}` are **Admin-only**, including download. Upload is multipart field `file`, supports PDF/PNG/JPEG up to **5 MiB**, and must pass MIME, permitted filename-extension and file signature checks. Body is stored in SQL `varbinary(max)` / Django `BinaryField`; never expose file data through unauthenticated public media URLs. Admin download is `Content-Disposition: attachment` using a sanitized stored filename. Documents return `{id, fileName, contentType, size}`. Refusing to delete an owner with protected files returns HTTP 409. Future Customer Ledger, outstanding credit and Supplier Payable postings belong to their transaction packages, not these master endpoints.

## Category hierarchy, Brand and Unit (WP14–WP15)

`GET/POST /api/categories` and `GET/PUT/DELETE /api/categories/{id}`; equivalent routes for `brands` and `units`. Each supports uppercase ASCII `code`, `nameEn/nameAr`, `isActive`, numeric `id`. Category has nullable `parentId` (self-FK). Code must be unique among **siblings** (and among root categories); matching codes beneath different parents are permitted. A cycle, nonexistent parent, invalid code or duplicate sibling is HTTP 400. Categories with child categories or referenced products cannot be deleted (409).

Brand code is globally unique and product references protect deletion (409). Unit code is globally unique, with `decimalPlaces` integer 0–6 to govern future quantities; referenced units cannot be deleted (409). Both APIs use action policies `categories.*`, `brands.*`, `units.*`; mutation requires CSRF and returns 201/200/204 or 400/403/404/409 as appropriate. SQL unique indexes and restrictive product FKs enforce concurrency and referential integrity. Existing Product API references category/brand/unit by numeric IDs; full product entry/selling flow remains WP16 onward.

## Brand and Unit Master (WP15)

Both Django and ASP.NET expose `GET /api/brands?search=term` and `GET /api/units?search=term` (optional `search` matches code, English and Arabic names). Both support `GET /api/{brands|units}/{id}`, `POST /api/{brands|units}`, `PUT /api/{brands|units}/{id}` and `DELETE /api/{brands|units}/{id}`. CamelCase fields: `code`, `nameEn`, `nameAr`, `isActive`; Unit additionally `decimalPlaces` (integer 0–6). Codes normalize to uppercase ASCII A–Z, digits, underscore and hyphen; duplicates are rejected. Referenced brands/units cannot be deleted (409). Policies enforce `brands.*`/`units.*` actions; CSRF on ASP.NET writes. Brand/Unit selectors in Product form are WP16, not part of this milestone.

## Product Master API contract — ERP-0311

Both backends expose GET/POST `/api/products` and GET/PUT/DELETE `/api/products/{id}`. Current `?search=` matches SKU, Barcode, English/Arabic name. Unpaged GET retains the legacy SKU-sorted JSON array for compatibility; explicit `page` and/or `pageSize` returns the paged response documented under **Product paged list — ERP-0315** below. Product JSON fields: numeric `id` on read, `sku`, nullable `barcode`, `nameEn/nameAr`, `descriptionEn/descriptionAr`, `categoryId`, nullable `brandId`, `unitId`, `productType`, `serialTracked`, `costPrice/basePrice/minPrice` (exact three-decimal strings on read), `reorderLevel` (six-decimal string), `isActive`. Product mutation requires CSRF and correct `products.*` permission. Intended statuses: 200 GET/PUT, 201 POST, 204 DELETE, 400 invalid/duplicate, 401 unauthenticated, 403 permission/CSRF, 404 missing, 409 linked-record deletion. Current concurrency/duplicate error-detail parity is **not yet proven**; see `ERP_0311_PRODUCT_API_CONTRACT.md`. Item Code/Tax/Model/Warranty/ledger and pagination remain outside the current serialized Product payload until the relevant scoped implementation steps.

## Product paged list — ERP-0315

Optional `GET /api/products?page=1&pageSize=25&search=term` on both backends returns a JSON object `{ "items": [/* Product objects */], "total": 0, "page": 1, "pageSize": 25 }`. Defaults when paging is requested: page=1, pageSize=25; pageSize accepts 1–100, invalid values yield 400 with `detail: "Invalid request."`. Search covers SKU, Barcode and English/Arabic Product name before counting. Unpaged GET without either paging parameter retains the original Product array response for compatibility. React Product Master uses 25-record pages and the existing CSRF-secured Product CRUD paths. Verified in CI [40660099435](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40660099435). Future broad Catalog pagination/performance belongs WP48.


## Digital Product licenses — existing implementation, WP17 acceptance pending

Both backends currently expose `GET /api/product-licenses?productId={id}`, `POST /api/product-licenses`, `GET /api/product-licenses/{id}`, `GET /api/product-licenses/{id}/reveal` and `DELETE /api/product-licenses/{id}`. No trailing slash. An active **digital** Product is required to issue a new license. The POST body accepts `productId` (positive BIGINT), optional `licenseKey` and `licenseNumber`, and nullable `activationDate`/`expiryDate` as ISO dates. At least one of key/number is required. Expiry cannot precede activation. List/details/create/revoke responses expose numeric `id`, `productId`, `licenseNumber`, `hasKey`, dates and `isActive`; **never** include plaintext `licenseKey`. Only an explicit `/reveal` call with `product-licenses.reveal` permission returns it, with `Cache-Control: no-store`.

The APIs require session authentication and action grants `product-licenses.view/add/revoke/reveal`; POST and DELETE require `X-CSRF-TOKEN`. Create returns 201; revoke returns 200 and repeated revoke is idempotent; missing license 404, malformed input 400, duplicate **active** normalized key 400 `{ "detail": "Active license key already exists." }`, and missing authorization/CSRF 401/403. Key contents are AES-GCM encrypted at rest and HMAC-fingerprinted with a separately configured 32-byte base64 `PRODUCT_LICENSE_SECRET`; production setup and key rotation require controlled secret handling. A revoked key may be reissued; revoked records remain history and should not be physically deleted. **WP17 ERP-0321–0340** still owns formal full-lifecycle acceptance; WP46 owns audit history, WP21/25 own stock movement and WP30 owns non-stock sales.

