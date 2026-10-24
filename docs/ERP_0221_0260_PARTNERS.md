# ERP-0221–0260 — Customer and Supplier work packages

Reviewed against SRS baseline and actual current code. Specification steps are not proof of deferred transaction modules.

## ERP-0221 — Customer SRS acceptance and owner mapping

SRS §§4,8,9,51,52,57 require Customer code, English/Arabic names/address, mobile, civil ID access controls, type, payment terms, opening balance, credit limit, searchable master and confidential attachments. Actual ledger/receivables belong WP32–WP33/WP43; posted invoice rules not owned by WP12. Current SRS baseline AT-02 spans quotation/print owners and cannot pass in WP12.

**Source evidence:** `docs/SRS_BASELINE.md`, `docs/ERP_REQUIREMENTS_GAP_MATRIX.md`, `django/apps/partners/models.py`, `frontend/src/components/Partners.tsx`. **Verification:** SRS/source mapping only; CI baseline 40056434243. No new runtime acceptance claimed.

## ERP-0222 — Customer source/backend/frontend inventory

ASP.NET Customer long PK, normalized ASCII code, nullable optional email, BIGINT FK-protected binary documents, server-side civilId omission for non-admin; Django CustomerSerializer mirrors bilingual fields, validates mandatory Arabic name/mobile, protects files; React Partners form handles bilingual CRUD/search, optional email, 3-place decimal strings, admin document upload/download. Existing full CI 40056434243 PASSED 5/5; file presence alone does not pass AT-02.

**Source evidence:** `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CustomersApiController.cs`, `django/apps/partners/api.py`, `frontend/src/components/Partners.tsx`, `aspnet-core/tests/smoke_sqlserver.py`, `django/apps/partners/tests.py`. **Verification:** SRS/source mapping only; CI baseline 40056434243. No new runtime acceptance claimed.

## ERP-0223 — Customer SRS/code discrepancy review

Source shows bilingual Customer API and form, normalized unique code, required Arabic name/mobile, CivilId read omission for nonadmins, documents admin-only and download protection. Remaining scope: full customer statement/receivable posting is WP32–WP33/WP43, quotation and printable output WP28/WP44; no API for these should be invented now. Current customer browsing is in-memory filtering, pagination owner WP48, full file threat scanning is downstream security WP46.

**Source:** SRS §§4,8,9,51,52,57; existing Customer DTO/DRF serializer, React Partner form and SQL/browser tests. Specification only: downstream financial statements/printing not claimed.

## ERP-0224 — Customer positive acceptance specification

Create authenticated admin Customer with code C-RTL-001, NameEn Retail, NameAr متجر الكويت, Arabic address, mobile, CreditLimit 2500.750, OpeningBalance 15.250, paymentTermsDays 30, type credit. Expect 201 numeric BIGINT ID, case-normalized code, exact Unicode and decimal string round-trip in GET/list/edit and shared React. New source must not alter monetary figures on UI locale switch. Ledger/quotation cannot be certified before business owners.

**Source:** SRS §§4,8,9,51,52,57; existing Customer DTO/DRF serializer, React Partner form and SQL/browser tests. Specification only: downstream financial statements/printing not claimed.

## ERP-0225 — Customer negative and authorization acceptance

Reject duplicate case-insensitive code and simultaneous duplicates with HTTP 400; reject blank Arabic name/mobile, invalid credit/decimal/email without saved mutation; deny employee CivilId details, admin-only file upload/list/download and cross-owner document access; reject MIME/extension mismatch; existing protected documents block delete with 409 and private downloads return no-store/nosniff. File scanning and attachment retention policy are WP46.

**Checked source:** `django/apps/partners/tests.py`, `aspnet-core/tests/smoke_sqlserver.py`, `django/apps/partners/api.py`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CustomersApiController.cs`. **Evidence:** existing SQL/browser CI 40060339256, no new feature claimed from documentation alone.

## ERP-0226 — Customer BIGINT and decimal schema design

Customer/PartnerDocument already use BIGINT IDENTITY/BigAutoField, unique normalized ASCII code, separately stored EN/AR Unicode name/address, positive decimal(18,3) credit and opening balance. PartnerDocument is binary + MIME + 200-char name with exclusive owner CHECK and restrictive FKs. Existing EF Partners/PartnerDetails and Django partners 0001/0002 migration cover all WP12 owned fields; do not add redundant columns or UUIDs. No live data migration warranted at this design step.

**Checked source:** `django/apps/partners/models.py`, `django/apps/partners/migrations/0001_initial.py`, `django/apps/partners/migrations/0002_partner_details.py`, `aspnet-core/src/ITRetailERP.Web/Data/ApplicationDbContext.cs`, `aspnet-core/src/ITRetailERP.Web/Migrations/20261023120000_Partners.cs`. **Evidence:** existing SQL/browser CI 40060339256, no new feature claimed from documentation alone.

## ERP-0227 Customer invariant review

Customer code must normalize to ASCII uppercase, use a DB unique index plus clean 400 on duplicate/concurrent writes; names and Arabic address must preserve Unicode; mandatory NameEn/NameAr/Mobile, 0–365 payment term days, nonnegative DECIMAL(18,3) amounts, no HTML/locale parsing of money. Customer inactive state must remain explicit; no silent deletion if PartnerDocument rows exist. FK PROTECT + check constraint prevent cross-owner or orphan attachment. Downgrade PartnerDetails migration is potentially destructive on existing data, so do not run on production; on disposable SQL CI test migrations and rollback rehearsal, with pre-upgrade backup required for real deployment. No new DDL for step.

## ERP-0228 — ASP.NET customer model/contract/API acceptance

Existing Customer long ID, bounded EN/AR strings, mandatory NameAr/Mobile server validation, ASCII uppercase code, decimal(18,3), optional email. CustomersApiController policy-gated CRUD catches concurrent unique errors and restricts CivilId/documents to admins; file checks and private no-store/nosniff downloads in place. No extra model or API is necessary.

Source: `aspnet-core/src/ITRetailERP.Web/Models/Customer.cs`, `aspnet-core/src/ITRetailERP.Web/Contracts/PartnerRequests.cs`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CustomersApiController.cs`. Existing security fix CI 40060339256 PASS; added non-admin smoke pending and is not yet a success claim.

## ERP-0229 — Django customer serializer and protected-file acceptance

CustomerSerializer mandates Arabic name/mobile and normalized unique code, preserves three-decimal money and suppresses CivilId for non-admin. PartnerViewSet handles database unique failures inside transaction.atomic, enforces admin-only documents and validates extension/MIME/signature. Download response has no-store/nosniff. No WP12 Django schema additions needed.

Source: `django/apps/partners/models.py`, `django/apps/partners/api.py`, `django/apps/partners/tests.py`, `django/config/exceptions.py`. Existing security fix CI 40060339256 PASS; added non-admin smoke pending and is not yet a success claim.

## ERP-0230 — Customer existing SQL schema/migration acceptance

Reviewed existing EF Partners (Customer, PartnerDocument) and PartnerDetails migrations against Django partners 0001/0002 and current models. Both map numeric BIGINT identity, unique code, Unicode fields, decimal(18,3), PartnerDocument owner-check and restrictive FKs. No current WP12 schema delta; creating a dummy migration would be wrong. Existing CI 40056434243 tested disposable SQL migrations; down/up safety for previous migrations was verified in earlier baseline WP03. No destructive production rollback. Post-migration non-null fields are additive with defaults.

Evidence: `django/apps/partners/migrations/0001_initial.py`, `django/apps/partners/migrations/0002_partner_details.py`, `aspnet-core/src/ITRetailERP.Web/Migrations/20261023120000_Partners.cs`, `aspnet-core/src/ITRetailERP.Web/Migrations/20261023150000_PartnerDetails.cs`. Existing 5/5 CI 40056434243; no new runtime code needed for this review.

## ERP-0231 — Customer cross-backend route and JSON contract

ASP.NET/Django both expose GET/POST /api/customers, GET/PUT/DELETE /api/customers/{numeric id}, GET/POST /api/customers/{id}/documents, GET /api/customers/{id}/documents/{documentId}. JSON properties camelCase nameEn/nameAr/addressEn/addressAr/civilId/customerType/paymentTermsDays/creditLimit/openingBalance. Money is invariant 3-place string and numeric id safe JSON integer. 201 create, 200 read/update, 204 delete, 400 invalid/duplicate, 403 denied, 404 wrong owner, 409 linked files. Django exception handler normalizes validation to detail Invalid request; CivilId must be omitted for non-admin. Actual protected documents are binary responses, not JSON. No future ledger endpoints claimed.

Evidence: `django/apps/partners/api.py`, `django/config/exceptions.py`, `aspnet-core/src/ITRetailERP.Web/Contracts/PartnerRequests.cs`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CustomersApiController.cs`, `frontend/src/api/partners.ts`. Existing 5/5 CI 40056434243; no new runtime code needed for this review.

## ERP-0232 — Customer ASP.NET CRUD and duplicate-post correctness

CustomersApiController POST/PUT applies normalized uppercase code once, checks collisions before insert and catches SQL unique-index race as HTTP 400. Validation precedes writes. DB assigns BIGINT Id; detail/create responses use exact decimal strings. DELETE refuses records with protected attachments (409). Each request is a single ORM save, no stock/ledger posting. Customer financial posting and approval idempotency are future WP30–33.

**Source:** `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CustomersApiController.cs`, `aspnet-core/src/ITRetailERP.Web/Services/SqlConstraintErrors.cs`, `aspnet-core/tests/smoke_sqlserver.py`. Baseline SQL/browser CI 40060339256 PASS; future receivable posting not claimed.

## ERP-0233 — Customer Django transaction and response parity

PartnerViewSet uses transaction.atomic for create/update and catches integrity races with standardized safe 400; CustomerSerializer validates normalized code, mandatory Arabic name/mobile, decimal values and optional email. Detailed/list representation masks CivilId unless admin; independent document CRUD uses protected FK. There is no WP12 financial posting/retry workflow; account receivables belong WP32/33. Django and ASP.NET create/update are semantically equivalent for the current master.

**Source:** `django/apps/partners/api.py`, `django/apps/partners/tests.py`, `django/config/exceptions.py`. Baseline SQL/browser CI 40060339256 PASS; future receivable posting not claimed.

## ERP-0234 — Customer server-side permission and confidential-field acceptance

ASP.NET policies gate customer read/add/edit/delete; only role Admin can list/upload/download secured attachments; non-admin customers.view can read customer rows but CivilId is omitted from both list/detail. Verified as SQL+API negative checks at CI 40060771866, including read-only inability to POST customer or get private file. Django has corresponding role-based read CivilId suppression and admin-only binary endpoints. Whole-system financial transaction branch scope/audit is owned by WP46/financial owners, not duplicated.

**Evidence:** `aspnet-core/tests/smoke_sqlserver.py`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CustomersApiController.cs`, `django/apps/partners/tests.py`, `django/apps/partners/api.py`; 5/5 CI 40060771866 PASS. This does not certify ledger or audit events in later financial modules.

## ERP-0235 — Customer React form, list, validation and private documents

Shared Partners.tsx renders Customer create/update/delete, EN/AR names/address, required Arabic name/mobile, type list, tax ID, civil ID, terms, 3-decimal opening balance and credit; search by code/name; keyboard Enter behavior; editing loads secured file list and allows admin to upload PDF/JPEG/PNG. The sidebar permits only admin to open Customer Master, but backend remains authority. API code uses decimal strings, not JS floats. Current customer/supplier Playwright and SQL smoke verified in CI 40060771866. Pagination/huge catalog performance remains WP48.

**Evidence:** `frontend/src/components/Partners.tsx`, `frontend/src/api/partners.ts`, `frontend/e2e/erp.spec.ts`, `frontend/src/components/AppShell.tsx`; 5/5 CI 40060771866 PASS. This does not certify ledger or audit events in later financial modules.

## ERP-0236 — Customer Arabic RTL/mobile and keyboard acceptance

Existing Playwright verifies AR root lang/dir, Arabic Customer input dir=rtl and LTR code/email/credit, 375px navigation and 768/1024px tablet browser layout. Credit Customer keyboard-first flow creates and reloads bilingual values. Original language picker changes only UI labels; SQL decimal strings unchanged. Generic test suite does not certify real assistive screen-reader usage or financial document printing; those are WP49/WP44. Current SQL/browser CI 40060771866 green.

Evidence: `frontend/e2e/erp.spec.ts`, `frontend/src/components/Partners.tsx`, `frontend/src/i18n.tsx`, `frontend/src/locale.ts`. 5/5 CI 40060771866 successful; deferred financial and accessibility cases are not reported passed.

## ERP-0237 — Customer ASP.NET validation and credit Customer runtime tests

`LocalizationContractTests` checks EN/AR DTO length and invariant money, and `aspnet-core/tests/smoke_sqlserver.py` exercises real SQL Server credit customer POST/PUT/GET, mandatory Arabic/mobile, duplicate code race, 3-decimal amounts, invalid email/credit and protected customer documents. The latest 5/5 workflow 40060771866 ran .NET unit tests and API+browser SQL smoke. Full customer ledger posting/quotation conversion tests are future WP28/30/32.

Evidence: `aspnet-core/tests/ITRetailERP.Tests/LocalizationContractTests.cs`, `aspnet-core/tests/smoke_sqlserver.py`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CustomersApiController.cs`. 5/5 CI 40060771866 successful; deferred financial and accessibility cases are not reported passed.

## ERP-0238 — Customer Django negative/error and protected-file regression acceptance

Django PartnerApiTests covers Customer Arabic/mobile required, duplicate normalized code (and Unicode identifier rejection), invalid email/negative 3-decimal credit, rejected update leaves previous details unchanged, CivilId admin-only, restricted documents, bad MIME/extension signatures and delete conflict. Django and SQL Server jobs passed CI 40060771866. Test database disposable; no real customer data changed.

**Source:** `django/apps/partners/tests.py`, `django/apps/partners/api.py`, `django/config/exceptions.py`. Successful workflow 40060771866. Deferred financial and printing acceptance remain explicitly open.

## ERP-0239 — Customer SQL, concurrency and shared React E2E acceptance

CI 40060771866 completed five jobs successfully: Django, ASP.NET, frontend, SQL Server integration and browser. ASP smoke checks DB BIGINT, Customer create/update/get Unicode/credit, 2 concurrent duplicate writes [201,400], forbidden private document retrieval, Customer protected-delete conflict, no-store and no-sniff. Shared React Playwright checks valid credit customer submit and Supplier after it. Cross-backend financial ledger/printed quotation not yet built and cannot be certified.

**Source:** `aspnet-core/tests/smoke_sqlserver.py`, `frontend/e2e/erp.spec.ts`, `.github/workflows/erp-verification.yml`, `django/apps/partners/tests.py`. Successful workflow 40060771866. Deferred financial and printing acceptance remain explicitly open.

## ERP-0240 — Customer acceptance closeout

Reviewed shared PartnerViewSet and React Partners module for unnecessary parallel code, ASP.NET PartnerValidation reuse, CSRF, duplicate unique index race, customer CivilId masking, Admin-only documents and security headers. Security fix commit 1773c7f prevents caching confidential customer/supplier downloads, and focused ASP.NET SQL smoke e0b0cd1 proves read-only employee cannot access CivilId/file or post. 5/5 successful CI run 40060771866 proves current customer acceptance. No schema/migration/regression remains blocking WP12. Still open by ownership: AR quotation/report physical printing WP28/WP44; customer ledger, payment/allocation and branch financial posting WP30/WP32/33; larger pagination WP48; advanced security audit/retention WP46. Do not claim these delivered.

**Evidence:** CI [40060771866](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40060771866) passed Django, ASP.NET, React, browser and SQL Server jobs on test environments. WP12 signoff applies only to existing customer master CRUD, permissions, validation and secured documents, not later invoices/payments/printing.

## ERP-0241 — Supplier Master requirements and downstream ledger ownership

SRS §§4,10,11,50,52,57: normalized Supplier code, bilingual EN/AR company names/address, contact person, telephone/mobile/email/tax number, 0–365 payment terms, three-decimal opening balance and credit limit, active state, protected attachment access and searchable CRUD. Supplier ledger, balance allocation, first purchase and payables belong WP24–WP27/WP43; no fake purchase link or stock/ledger posting in WP13.

Evidence: `docs/SRS_BASELINE.md`, `docs/ERP_REQUIREMENTS_GAP_MATRIX.md`, `django/apps/partners/models.py`, `frontend/src/components/Partners.tsx`. SRS acceptance specification/source, not verification of supplier ledger, purchase or financial print.

## ERP-0242 — Supplier ASP.NET/Django/React source inspection

SupplierRequest/Supplier long entity and SuppliesApiController present GET/POST/PUT/DELETE with bounded validation, unique code and amount/email checks. Django SupplierSerializer/PartnerViewSet and PartnerDocument APIs match; React Partners handles Supplier bilingual fields, saved decimals and admin file picker. ASP/Django files use numeric BIGINT IDs and contract-consistent supplier routes. Baseline CI 40060771866 passed SQL + frontend and browser, but not an actual purchase/ledger acceptance.

Evidence: `aspnet-core/src/ITRetailERP.Web/Models/Supplier.cs`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/SuppliersApiController.cs`, `django/apps/partners/api.py`, `django/apps/partners/models.py`, `frontend/src/components/Partners.tsx`. SRS acceptance specification/source, not verification of supplier ledger, purchase or financial print.

## ERP-0243 — Supplier SRS/code discrepancy and acceptance ownership

Current Supplier CRUD covers code, bilingual names, contact details, paymentTermsDays, openingBalance and creditLimit; file list/upload/download are Admin-only. SRS §11 supplier statement/payables and first Purchase linkage cannot yet be executed—WP24/25/27/43 own them. Current no-store/nosniff protections are fixed; absent bulk pagination belongs WP48 and deep audit/retention WP46. No independent supplier-specific database migration is required.

Source `docs/SRS_BASELINE.md`, `django/apps/partners/api.py`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/SuppliersApiController.cs`, `frontend/src/components/Partners.tsx`, `aspnet-core/tests/smoke_sqlserver.py`. Current Supplier Master proof separate from later purchase/ledger posting.

## ERP-0244 — Supplier create/read/update and first-purchase acceptance contract

Admin creates S-AR-001 with Arabic name المورد الرئيسي, English name Main Supplier, contact person, tax number, terms 14, openingBalance 135.500, creditLimit 800.500. Both ASP.NET/Django respond 201 with numeric BIGINT Id and exact decimals, list/detail round-trip and edit preserve Arabic. Shared React can save via keyboard and reload. Later link the same SupplierId to the first purchase order/invoice through WP24/25 and verify payable entry WP27; this downstream case is a test contract, not a claimed implementation.

Source `docs/SRS_BASELINE.md`, `django/apps/partners/api.py`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/SuppliersApiController.cs`, `frontend/src/components/Partners.tsx`, `aspnet-core/tests/smoke_sqlserver.py`. Current Supplier Master proof separate from later purchase/ledger posting.

## ERP-0245 — Supplier duplicate-code, decimal and private-document negative acceptance

Customer/Supplier code policy is ASCII letters/digits/hyphen/underscore and normalizes upper-case in both backends; duplicate Supplier create/update and concurrent duplicate must return 400 without partial save. Reject negative or overprecision openingBalance/creditLimit and invalid optional email. Only Admin may list, upload or download Supplier files; readers with suppliers.view get 403. Reject MIME-signature/extension mismatch and >5 MB; content-disposition safe filename, nosniff and no-store. Wrong owner document id gets 404; linked files block Supplier delete with 409. No first-purchase posting claimed.

Checked files: `django/apps/partners/tests.py`, `aspnet-core/tests/smoke_sqlserver.py`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/SuppliersApiController.cs`, `django/apps/partners/api.py`. Future purchase/ledger owner acceptance explicitly deferred.
