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
