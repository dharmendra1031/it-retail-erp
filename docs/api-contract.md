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
