# WP09 — Branch and Warehouse foundation

Schema:
- Company -> Branch (BIGINT FK, restrict delete); unique branch code per Company
- Branch -> Warehouse (BIGINT FK, restrict delete); unique warehouse code per Branch
- User -> optional Branch (BIGINT FK, restrict delete); default null for bootstrap/migration compatibility.
- Unique numeric auto-increment IDs on both backends and Unicode English/Arabic names.

Contracts: `GET/POST /api/branches`, `GET/PUT/DELETE /api/branches/{id}`, analogous `/api/warehouses`. Authenticated users can see only their assigned branch and its warehouses; administrators can see all and manage. Missing/cross-branch reads return 404. Unauthorized writes return 403, missing/invalid foreign keys 400, in-use branch delete 409.

No automatic cross-branch transfer or stock posting endpoint is invented here. The transaction owners WP24–37 must use this branch/warehouse relationship when introduced. Single shop can set up one branch and one warehouse explicitly; no silent new Company auto-creation. Future department-level scoping and immutable changes audit belong to WP46.
