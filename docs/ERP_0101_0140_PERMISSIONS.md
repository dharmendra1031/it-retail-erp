# WP06 and WP07 — Permission catalog and Role Master assignments

Current code owns permission catalog and assignment, using Django `AccessPermission` and `Role.permissions`, and ASP.NET Core Identity `AspNetRoleClaims`. No additional ASP.NET permission table or numeric IDs are needed; framework role claims keep their standard ID and application Role IDs are BIGINT.

## Contract
- `GET /api/permissions` (Admin): array of `{code,name}`, e.g. `sales.post`, `sales.reverse`, `companies.add`.
- `GET /api/roles/{id}/permissions` (Admin): `{permissions:["companies.add"]}`.
- `PUT /api/roles/{id}/permissions` (Admin, CSRF): `{permissions:string[]}`; full replacement, distinct sorted, unknown codes 400, protected Admin role 400, non-Admin 403, missing role 404.
- No privilege self-service, no implicit Admin grant, no auto-assignment. Role permission changes remain Admin-only. ASP uses a transaction and Django uses `atomic`.
- Existing Company reads remain authenticated; Company creates, edits and deletes are checked server-side using their distinct action grants or Admin membership. Defer branch scope and audit to WP09/WP46.
- The catalogue covers currently relevant master actions plus future lifecycle verbs View/Add/Edit/Delete/Print/Export/Approve/Cancel/Post/Reverse; it **does not** imply corresponding business APIs exist.
- Frontend must not assume hiding a button is authorization. The server rejects missing permission.

## Acceptance
Django: permission catalog + role grant replacement (including invalid/cross-user denial), delegated Company create without delete. ASP: catalog and full grant replacement validated in SQL Server CI smoke. Both login, CSRF and existing Company tests retained. Later full Sales role/invoice posting semantics belong to Purchase/Sales owners.
