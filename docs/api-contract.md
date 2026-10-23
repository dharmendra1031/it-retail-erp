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


## Customer/Supplier Masters (WP12–WP13)

`GET/POST /api/customers`, `GET/PUT/DELETE /api/customers/{id}`; analogous `/api/suppliers`. Server-side permission policy `customers.*`/`suppliers.*`, Admin implicit grants. Numeric BIGINT IDs and unique uppercase code. Customer JSON fields `code,nameEn,nameAr,addressEn,addressAr,mobile,civilId,customerType,paymentTermsDays,creditLimit,isActive`, supplier replaces CivilID/type/credit with `email,taxNumber,openingBalance`. Decimal money values use invariant fixed-point strings with three decimals. Credit and opening balances must be non-negative.

Protected documents: `GET/POST /api/{customers|suppliers}/{id}/documents` (Admin only), and authenticated Admin-only `GET .../documents/{docId}`. Body stores in SQL Server `varbinary(max)`/`BinaryField`, not an unauthenticated static-media URL. Upload supports PDF/PNG/JPEG signatures and maximum 5 MiB. No public file identifiers/links are emitted to non-Admin users. A customer reader without Admin does not receive the CivilID field. Protected-document owner cannot be deleted (409).
