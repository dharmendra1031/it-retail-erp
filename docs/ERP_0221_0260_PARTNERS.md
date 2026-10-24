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
