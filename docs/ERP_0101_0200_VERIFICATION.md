# ERP-0101–ERP-0200 — Security and organization foundation verification

**Date:** 2026-10-23  
**Branch:** `development`  
**Verified source:** `710f0f05a8fedc080a58c6149c961d56a7f6d4dd`  
**Passing [GitHub Actions run 39979943571](https://github.com/dharmendra1031/it-retail-erp/actions/runs/39979943571):** 5/5 jobs PASS, tested on disposable CI databases only.

## What is actually implemented and exercised

| Step range | Current package deliverable | Code/acceptance result |
|---|---|---|
| 0101–0120 | 73 module/action permission keys; role-policy enforcement for Company CRUD | Catalog and protected role grants. Server denies forbidden Company actions |
| 0121–0140 | Role Master, permission replacement matrix | Admin-only role/permission management, protected Admin role, invalid code rejection, keyboard-accessible English/Arabic permission matrix |
| 0141–0160 | User Master and membership | Admin-only creation, update, password hashing/reset, activate/deactivate, assignment to existing roles; disabled logins blocked |
| 0161–0180 | Branch/Warehouse foundation | BIGINT Company→Branch→Warehouse foreign keys, user→branch assignment, uniqueness, cross-branch read denied, in-use delete prevented |
| 0181–0200 | Company identity/logo lifecycle | Bilingual Company CRUD; max-2MB MIME/signature upload checks and Django deep Pillow verification; logo replacement cleanup; print identity preview and Arabic controls |

## CI evidence

- **Django:** 60/60 SQL Server 2022 tests PASS; on isolated SQLite 53 PASS + 7 SQL-only SKIP.
- **ASP.NET Core:** 4/4 SQL-backed xUnit tests, EF migration drift/rollback, REST API/CSRF and business master smoke PASS.
- **Playwright:** 13/13 Django browser tests and 11/11 ASP.NET browser tests PASS.
- **React:** TypeScript/production build PASS; EN/AR switching, LTR/RTL, Enter navigation and master forms exercised.
- **Production database and IIS:** not accessed, not signed off.

## 100-step acceptance evidence

Every step is marked complete **only for its package-owned review, implementation, or current available integration scope**. These 100 tasks are not 100 independent business modules. Later-package controls are tracked below and must be tested again when the real transaction features exist.

| Step | Evidence gate | Source paths |
|---|---|---|
| ERP-0101 | Mapped exact SRS package scope and future-owner exclusions | docs/ERP_0101_0140_PERMISSIONS.md, docs/SRS_BASELINE.md |
| ERP-0102 | Inspected currently checked-in Django/ASP.NET/React code | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Security/PermissionRequirement.cs, django/apps/accounts/permissions.py |
| ERP-0103 | Compared implemented surfaces with documented business acceptance and gaps | docs/ERP_0101_0140_PERMISSIONS.md, docs/ERP_REQUIREMENTS_GAP_MATRIX.md |
| ERP-0104 | Verified current package happy path using API/UI smoke | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/PermissionsApiController.cs, django/apps/accounts/permissions_api.py |
| ERP-0105 | Verified current package authorization/validation negative path | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/tests/smoke_sqlserver.py, django/apps/companies/tests.py |
| ERP-0106 | Reviewed existing BIGINT/Unicode/FK schema and transactional invariants | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/migrations/0004_permission_catalog.py |
| ERP-0107 | Documented input constraints and rollback/ownership boundaries | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/permissions.py |
| ERP-0108 | Implemented or reviewed ASP.NET Core package-owned code | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Security/PermissionRequirement.cs |
| ERP-0109 | Implemented or reviewed Django package-owned code | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/permissions.py |
| ERP-0110 | Verified real package migration/schema and documented non-owned migration cases | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/migrations/0004_permission_catalog.py, .github/workflows/erp-verification.yml |
| ERP-0111 | Documented shared request/response/error shapes | docs/ERP_0101_0140_PERMISSIONS.md, docs/api-contract.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/PermissionsApiController.cs |
| ERP-0112 | Verified ASP.NET package operations and current server-side enforcement | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Security/PermissionRequirement.cs |
| ERP-0113 | Verified Django package operations and transaction scope | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/permissions.py |
| ERP-0114 | Checked implemented authorization, with future-only branch/audit controls deferred | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Security/PermissionRequirement.cs, django/apps/accounts/permissions.py |
| ERP-0115 | Verified shared React screen, API integration and user feedback | docs/ERP_0101_0140_PERMISSIONS.md, frontend/src/components/Roles.tsx |
| ERP-0116 | Verified currently implemented English/Arabic labels, RTL layout and keyboard behavior | docs/ERP_0101_0140_PERMISSIONS.md, frontend/src/i18n.tsx, frontend/e2e/erp.spec.ts |
| ERP-0117 | Ran available ASP.NET build/API/integration checks for package functionality | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/tests/smoke_sqlserver.py |
| ERP-0118 | Ran Django unit/SQL integration/negative tests for package functionality | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/tests.py, django/apps/companies/tests.py |
| ERP-0119 | Ran disposable SQL Server plus browser smoke (and defined future-module exclusions) | docs/ERP_0101_0140_PERMISSIONS.md, .github/workflows/erp-verification.yml, frontend/e2e/erp.spec.ts |
| ERP-0120 | Reviewed current changes, regression evidence, security/performance boundaries and CI | docs/ERP_0101_0140_PERMISSIONS.md, docs/ERP_DATABASE_REVIEW.md, docs/api-contract.md |
| ERP-0121 | Mapped exact SRS package scope and future-owner exclusions | docs/ERP_0101_0140_PERMISSIONS.md, docs/SRS_BASELINE.md |
| ERP-0122 | Inspected currently checked-in Django/ASP.NET/React code | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/RolesApiController.cs, django/apps/accounts/roles_api.py |
| ERP-0123 | Compared implemented surfaces with documented business acceptance and gaps | docs/ERP_0101_0140_PERMISSIONS.md, docs/ERP_REQUIREMENTS_GAP_MATRIX.md |
| ERP-0124 | Verified current package happy path using API/UI smoke | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Contracts/RoleRequest.cs, django/apps/accounts/serializers.py |
| ERP-0125 | Verified current package authorization/validation negative path | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/tests/smoke_sqlserver.py, django/apps/companies/tests.py |
| ERP-0126 | Reviewed existing BIGINT/Unicode/FK schema and transactional invariants | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/models.py |
| ERP-0127 | Documented input constraints and rollback/ownership boundaries | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/roles_api.py |
| ERP-0128 | Implemented or reviewed ASP.NET Core package-owned code | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/RolesApiController.cs |
| ERP-0129 | Implemented or reviewed Django package-owned code | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/roles_api.py |
| ERP-0130 | Verified real package migration/schema and documented non-owned migration cases | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/models.py, .github/workflows/erp-verification.yml |
| ERP-0131 | Documented shared request/response/error shapes | docs/ERP_0101_0140_PERMISSIONS.md, docs/api-contract.md, aspnet-core/src/ITRetailERP.Web/Contracts/RoleRequest.cs |
| ERP-0132 | Verified ASP.NET package operations and current server-side enforcement | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/RolesApiController.cs |
| ERP-0133 | Verified Django package operations and transaction scope | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/roles_api.py |
| ERP-0134 | Checked implemented authorization, with future-only branch/audit controls deferred | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/RolesApiController.cs, django/apps/accounts/roles_api.py |
| ERP-0135 | Verified shared React screen, API integration and user feedback | docs/ERP_0101_0140_PERMISSIONS.md, frontend/src/components/Roles.tsx |
| ERP-0136 | Verified currently implemented English/Arabic labels, RTL layout and keyboard behavior | docs/ERP_0101_0140_PERMISSIONS.md, frontend/src/i18n.tsx, frontend/e2e/erp.spec.ts |
| ERP-0137 | Ran available ASP.NET build/API/integration checks for package functionality | docs/ERP_0101_0140_PERMISSIONS.md, aspnet-core/tests/smoke_sqlserver.py |
| ERP-0138 | Ran Django unit/SQL integration/negative tests for package functionality | docs/ERP_0101_0140_PERMISSIONS.md, django/apps/accounts/tests.py, django/apps/companies/tests.py |
| ERP-0139 | Ran disposable SQL Server plus browser smoke (and defined future-module exclusions) | docs/ERP_0101_0140_PERMISSIONS.md, .github/workflows/erp-verification.yml, frontend/e2e/erp.spec.ts |
| ERP-0140 | Reviewed current changes, regression evidence, security/performance boundaries and CI | docs/ERP_0101_0140_PERMISSIONS.md, docs/ERP_DATABASE_REVIEW.md, docs/api-contract.md |
| ERP-0141 | Mapped exact SRS package scope and future-owner exclusions | docs/ERP_0141_0160_USER_MASTER.md, docs/SRS_BASELINE.md |
| ERP-0142 | Inspected currently checked-in Django/ASP.NET/React code | docs/ERP_0141_0160_USER_MASTER.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/UsersApiController.cs, django/apps/accounts/users_api.py |
| ERP-0143 | Compared implemented surfaces with documented business acceptance and gaps | docs/ERP_0141_0160_USER_MASTER.md, docs/ERP_REQUIREMENTS_GAP_MATRIX.md |
| ERP-0144 | Verified current package happy path using API/UI smoke | docs/ERP_0141_0160_USER_MASTER.md, aspnet-core/src/ITRetailERP.Web/Contracts/UserRequest.cs, django/apps/accounts/models.py |
| ERP-0145 | Verified current package authorization/validation negative path | docs/ERP_0141_0160_USER_MASTER.md, aspnet-core/tests/smoke_sqlserver.py, django/apps/companies/tests.py |
| ERP-0146 | Reviewed existing BIGINT/Unicode/FK schema and transactional invariants | docs/ERP_0141_0160_USER_MASTER.md, aspnet-core/src/ITRetailERP.Web/Migrations/20261023100000_UserIsActive.cs |
| ERP-0147 | Documented input constraints and rollback/ownership boundaries | docs/ERP_0141_0160_USER_MASTER.md, django/apps/accounts/users_api.py |
| ERP-0148 | Implemented or reviewed ASP.NET Core package-owned code | docs/ERP_0141_0160_USER_MASTER.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/UsersApiController.cs |
| ERP-0149 | Implemented or reviewed Django package-owned code | docs/ERP_0141_0160_USER_MASTER.md, django/apps/accounts/users_api.py |
| ERP-0150 | Verified real package migration/schema and documented non-owned migration cases | docs/ERP_0141_0160_USER_MASTER.md, aspnet-core/src/ITRetailERP.Web/Migrations/20261023100000_UserIsActive.cs, .github/workflows/erp-verification.yml |
| ERP-0151 | Documented shared request/response/error shapes | docs/ERP_0141_0160_USER_MASTER.md, docs/api-contract.md, aspnet-core/src/ITRetailERP.Web/Contracts/UserRequest.cs |
| ERP-0152 | Verified ASP.NET package operations and current server-side enforcement | docs/ERP_0141_0160_USER_MASTER.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/UsersApiController.cs |
| ERP-0153 | Verified Django package operations and transaction scope | docs/ERP_0141_0160_USER_MASTER.md, django/apps/accounts/users_api.py |
| ERP-0154 | Checked implemented authorization, with future-only branch/audit controls deferred | docs/ERP_0141_0160_USER_MASTER.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/UsersApiController.cs, django/apps/accounts/users_api.py |
| ERP-0155 | Verified shared React screen, API integration and user feedback | docs/ERP_0141_0160_USER_MASTER.md, frontend/src/components/Users.tsx |
| ERP-0156 | Verified currently implemented English/Arabic labels, RTL layout and keyboard behavior | docs/ERP_0141_0160_USER_MASTER.md, frontend/src/i18n.tsx, frontend/e2e/erp.spec.ts |
| ERP-0157 | Ran available ASP.NET build/API/integration checks for package functionality | docs/ERP_0141_0160_USER_MASTER.md, aspnet-core/tests/smoke_sqlserver.py |
| ERP-0158 | Ran Django unit/SQL integration/negative tests for package functionality | docs/ERP_0141_0160_USER_MASTER.md, django/apps/accounts/tests.py, django/apps/companies/tests.py |
| ERP-0159 | Ran disposable SQL Server plus browser smoke (and defined future-module exclusions) | docs/ERP_0141_0160_USER_MASTER.md, .github/workflows/erp-verification.yml, frontend/e2e/erp.spec.ts |
| ERP-0160 | Reviewed current changes, regression evidence, security/performance boundaries and CI | docs/ERP_0141_0160_USER_MASTER.md, docs/ERP_DATABASE_REVIEW.md, docs/api-contract.md |
| ERP-0161 | Mapped exact SRS package scope and future-owner exclusions | docs/ERP_0161_0180_BRANCHES.md, docs/SRS_BASELINE.md |
| ERP-0162 | Inspected currently checked-in Django/ASP.NET/React code | docs/ERP_0161_0180_BRANCHES.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/BranchesApiController.cs, django/apps/companies/organization_api.py |
| ERP-0163 | Compared implemented surfaces with documented business acceptance and gaps | docs/ERP_0161_0180_BRANCHES.md, docs/ERP_REQUIREMENTS_GAP_MATRIX.md |
| ERP-0164 | Verified current package happy path using API/UI smoke | docs/ERP_0161_0180_BRANCHES.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/WarehousesApiController.cs, django/apps/companies/models.py |
| ERP-0165 | Verified current package authorization/validation negative path | docs/ERP_0161_0180_BRANCHES.md, aspnet-core/tests/smoke_sqlserver.py, django/apps/companies/tests.py |
| ERP-0166 | Reviewed existing BIGINT/Unicode/FK schema and transactional invariants | docs/ERP_0161_0180_BRANCHES.md, aspnet-core/src/ITRetailERP.Web/Migrations/20261023110000_BranchesWarehouses.cs |
| ERP-0167 | Documented input constraints and rollback/ownership boundaries | docs/ERP_0161_0180_BRANCHES.md, django/apps/companies/organization_api.py |
| ERP-0168 | Implemented or reviewed ASP.NET Core package-owned code | docs/ERP_0161_0180_BRANCHES.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/BranchesApiController.cs |
| ERP-0169 | Implemented or reviewed Django package-owned code | docs/ERP_0161_0180_BRANCHES.md, django/apps/companies/organization_api.py |
| ERP-0170 | Verified real package migration/schema and documented non-owned migration cases | docs/ERP_0161_0180_BRANCHES.md, aspnet-core/src/ITRetailERP.Web/Migrations/20261023110000_BranchesWarehouses.cs, .github/workflows/erp-verification.yml |
| ERP-0171 | Documented shared request/response/error shapes | docs/ERP_0161_0180_BRANCHES.md, docs/api-contract.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/WarehousesApiController.cs |
| ERP-0172 | Verified ASP.NET package operations and current server-side enforcement | docs/ERP_0161_0180_BRANCHES.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/BranchesApiController.cs |
| ERP-0173 | Verified Django package operations and transaction scope | docs/ERP_0161_0180_BRANCHES.md, django/apps/companies/organization_api.py |
| ERP-0174 | Checked implemented authorization, with future-only branch/audit controls deferred | docs/ERP_0161_0180_BRANCHES.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/BranchesApiController.cs, django/apps/companies/organization_api.py |
| ERP-0175 | Verified shared React screen, API integration and user feedback | docs/ERP_0161_0180_BRANCHES.md, frontend/src/components/Organization.tsx |
| ERP-0176 | Verified currently implemented English/Arabic labels, RTL layout and keyboard behavior | docs/ERP_0161_0180_BRANCHES.md, frontend/src/i18n.tsx, frontend/e2e/erp.spec.ts |
| ERP-0177 | Ran available ASP.NET build/API/integration checks for package functionality | docs/ERP_0161_0180_BRANCHES.md, aspnet-core/tests/smoke_sqlserver.py |
| ERP-0178 | Ran Django unit/SQL integration/negative tests for package functionality | docs/ERP_0161_0180_BRANCHES.md, django/apps/accounts/tests.py, django/apps/companies/tests.py |
| ERP-0179 | Ran disposable SQL Server plus browser smoke (and defined future-module exclusions) | docs/ERP_0161_0180_BRANCHES.md, .github/workflows/erp-verification.yml, frontend/e2e/erp.spec.ts |
| ERP-0180 | Reviewed current changes, regression evidence, security/performance boundaries and CI | docs/ERP_0161_0180_BRANCHES.md, docs/ERP_DATABASE_REVIEW.md, docs/api-contract.md |
| ERP-0181 | Mapped exact SRS package scope and future-owner exclusions | docs/ERP_0181_0200_COMPANY.md, docs/SRS_BASELINE.md |
| ERP-0182 | Inspected currently checked-in Django/ASP.NET/React code | docs/ERP_0181_0200_COMPANY.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/CompaniesApiController.cs, django/apps/companies/serializers.py |
| ERP-0183 | Compared implemented surfaces with documented business acceptance and gaps | docs/ERP_0181_0200_COMPANY.md, docs/ERP_REQUIREMENTS_GAP_MATRIX.md |
| ERP-0184 | Verified current package happy path using API/UI smoke | docs/ERP_0181_0200_COMPANY.md, aspnet-core/src/ITRetailERP.Web/Services/CompanyLogoStorage.cs, django/apps/companies/api.py |
| ERP-0185 | Verified current package authorization/validation negative path | docs/ERP_0181_0200_COMPANY.md, aspnet-core/tests/smoke_sqlserver.py, django/apps/companies/tests.py |
| ERP-0186 | Reviewed existing BIGINT/Unicode/FK schema and transactional invariants | docs/ERP_0181_0200_COMPANY.md, django/apps/companies/migrations/0001_initial.py |
| ERP-0187 | Documented input constraints and rollback/ownership boundaries | docs/ERP_0181_0200_COMPANY.md, django/apps/companies/serializers.py |
| ERP-0188 | Implemented or reviewed ASP.NET Core package-owned code | docs/ERP_0181_0200_COMPANY.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/CompaniesApiController.cs |
| ERP-0189 | Implemented or reviewed Django package-owned code | docs/ERP_0181_0200_COMPANY.md, django/apps/companies/serializers.py |
| ERP-0190 | Verified real package migration/schema and documented non-owned migration cases | docs/ERP_0181_0200_COMPANY.md, django/apps/companies/migrations/0001_initial.py, .github/workflows/erp-verification.yml |
| ERP-0191 | Documented shared request/response/error shapes | docs/ERP_0181_0200_COMPANY.md, docs/api-contract.md, aspnet-core/src/ITRetailERP.Web/Services/CompanyLogoStorage.cs |
| ERP-0192 | Verified ASP.NET package operations and current server-side enforcement | docs/ERP_0181_0200_COMPANY.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/CompaniesApiController.cs |
| ERP-0193 | Verified Django package operations and transaction scope | docs/ERP_0181_0200_COMPANY.md, django/apps/companies/serializers.py |
| ERP-0194 | Checked implemented authorization, with future-only branch/audit controls deferred | docs/ERP_0181_0200_COMPANY.md, aspnet-core/src/ITRetailERP.Web/Controllers/Api/CompaniesApiController.cs, django/apps/companies/serializers.py |
| ERP-0195 | Verified shared React screen, API integration and user feedback | docs/ERP_0181_0200_COMPANY.md, frontend/src/components/Companies.tsx |
| ERP-0196 | Verified currently implemented English/Arabic labels, RTL layout and keyboard behavior | docs/ERP_0181_0200_COMPANY.md, frontend/src/i18n.tsx, frontend/e2e/erp.spec.ts |
| ERP-0197 | Ran available ASP.NET build/API/integration checks for package functionality | docs/ERP_0181_0200_COMPANY.md, aspnet-core/tests/smoke_sqlserver.py |
| ERP-0198 | Ran Django unit/SQL integration/negative tests for package functionality | docs/ERP_0181_0200_COMPANY.md, django/apps/accounts/tests.py, django/apps/companies/tests.py |
| ERP-0199 | Ran disposable SQL Server plus browser smoke (and defined future-module exclusions) | docs/ERP_0181_0200_COMPANY.md, .github/workflows/erp-verification.yml, frontend/e2e/erp.spec.ts |
| ERP-0200 | Reviewed current changes, regression evidence, security/performance boundaries and CI | docs/ERP_0181_0200_COMPANY.md, docs/ERP_DATABASE_REVIEW.md, docs/api-contract.md |

## Safety and deferred work

- `sales.post`, `sales.reverse`, stock transfer and related codes exist in the **catalog**, not as working Sales/Inventory endpoints; actual posting permissions, financial idempotency, decimals and stock ledgers are future WP24–37.
- Company/branch references and branch/warehouse master read-scope are implemented; **all future transactions** must independently enforce branch scope. No proof of cross-branch stock transfer denial exists because transfer APIs do not exist.
- Printing in WP10 is Company identity via browser preview/print; invoice/report bilingual PDF and physical printing belong to WP44. No claim of real financial printing.
- .NET logo validation checks file type, extension, size and magic header, whereas Django performs Pillow image decode verification. Full payload decoding of .NET image uploads, file-scanning and failure-injection for file/database atomicity remain a production-hardening concern and require an explicit later gate.
- Existing data migrations must be tested on a staging copy before installation; CI is SQL Server 2022, not production SQL Server 2019.
- Server-side authorization remains mandatory; hiding a React button never grants permission. Advanced per-branch access policies for future transaction records and immutable audit trail remain separate package work.
