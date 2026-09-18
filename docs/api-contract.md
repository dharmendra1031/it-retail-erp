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

All entity IDs are numeric auto-increment values.
