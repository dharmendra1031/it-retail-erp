# WP08 — User Master / role membership

Two backend implementations expose `GET/POST /api/users`, `GET/PUT /api/users/{id}`, and `PUT /api/users/{id}/password`, Admin only with CSRF on writes.

All exposed IDs are numeric `BIGINT` user IDs. Request fields are `username, fullName, email, mobile, isActive, roleIds`; create additionally requires `password`. Responses never expose passwords/hashes. Role IDs must exist or the request fails before persistence. Duplicate email/usernames get 400; invalid input 400, unauthorized caller 403, missing user 404. Existing user is updated/disabled, never hard-deleted.

Django extends existing custom User with a mobile column, uses Django password hashing and `validate_password`; .NET extends Identity user with `IsActive` and reuses PhoneNumber, security stamp, password reset token and scoped transaction. Disabled accounts are denied at login and cookie validation. Default privileged bootstrap and existing login screens remain.

Full employee master, branch-level assignment and audit logs are future WP09/WP46 scope. New User Master UI is keyboard-first and English/Arabic localized as required by project rules.
