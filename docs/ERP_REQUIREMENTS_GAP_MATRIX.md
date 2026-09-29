# ERP-0003 — SRS-to-code gap matrix

**SRS:** [Computer Hardware & IT Retail Management System SRS](https://docs.google.com/document/d/1Gb_pMJAN14UY0scLJjGBGiuRZdlXOWJARB1aLkzIobc/edit?usp=sharing), last modified 2026-09-09T13:09:35.807Z.
**Code snapshot:** `development` HEAD `e2755b3f2c9316e10ddf8b150c67c75ff8c66124`, complete non-truncated Git tree (78 tracked files).
**Assessment:** source-level only; no build, SQL migration, browser, or API runtime tests executed in this step.

## Status definitions

- `PARTIAL`: some source code exists, but the complete SRS behavior is not implemented or its test evidence is missing.
- `ABSENT`: no implementation was found in the complete reviewed repository tree; this does not claim the feature cannot exist outside this branch.
- `FUTURE-DECISION`: SRS marks a future integration and a business approval is needed before claiming delivery.
- A code file or migration existing is **not** a passing functional test.

## Evidence keys (actual paths checked against the reviewed tree)

- **[A]** `aspnet-core/src/ITRetailERP.Web/Controllers/Api/AuthController.cs`; `django/apps/accounts/api.py`; `frontend/src/components/Login.tsx`.
- **[C]** `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CompaniesApiController.cs`; `django/apps/companies/api.py`; `django/apps/companies/serializers.py`; `frontend/src/components/Companies.tsx`.
- **[P]** `django/apps/accounts/models.py` (Role, AccessPermission, User foundations); `aspnet-core/src/ITRetailERP.Web/Data/ApplicationDbContext.cs` (Identity<long>).
- **[U]** `frontend/src/App.tsx`; `frontend/src/components/AppShell.tsx` (only Login and Company screen/navigation).
- **[R]** `django/config/api_urls.py` and `aspnet-core/src/ITRetailERP.Web/Controllers/Api/` (only auth/companies routes/controllers).
- **[D]** `aspnet-core/src/ITRetailERP.Web/Migrations/20260918070000_InitialCreate.cs`; `django/apps/accounts/migrations/0001_initial.py`; `django/apps/companies/migrations/0001_initial.py` (only auth and Company business schema).
- **[L]** `aspnet-core/src/ITRetailERP.Web/Models/Company.cs`; `django/apps/companies/models.py`; `frontend/src/components/CompanyForm.tsx` (Company English/Arabic fields, not global translation).
- **[E]** `aspnet-core/src/ITRetailERP.Web/Program.cs`; `django/config/settings.py`; `frontend/vite.config.ts` (env and shared `/api` proxy).
- **[T]** Complete, non-truncated `development` Git tree and its only controllers/routes/apps/screens: `[R]`, `[U]`, `[D]`; no other ERP module found.
- **[B]** `docs/SRS_BASELINE.md` and `docs/ERP_PLAN_1000_STEPS.md` (documented intent only; not executed functionality).
- **[Q]** `aspnet-core/src/ITRetailERP.Web/Controllers/Api/CompaniesApiController.cs` (`ToListAsync` without pagination); `django/apps/companies/api.py` (unpaginated queryset).
- **[G]** `aspnet-core/src/ITRetailERP.Web/Services/CompanyLogoStorage.cs`; `django/apps/companies/serializers.py` (file deletion/overwrite before DB update).
- **[M]** `aspnet-core/src/ITRetailERP.Web/Migrations/20260918070000_InitialCreate.cs` (`EmailIndex` nonunique, Company `nvarchar` and `bigint`); `django/apps/accounts/migrations/0001_initial.py` (unique email and BigAutoField).

## Full source-section coverage

| SRS section | Title | Status | Code evidence | Concrete missing/verification gap | Plan owner |
|---|---|---|---|---|---|
| 1 | PROJECT OBJECTIVE | PARTIAL | [A] [C] [T] | Hardware/software/service ERP and full transaction chain absent | WP01, WP16–WP50 |
| 2 | BUSINESS TYPE | ABSENT | [T] | Hardware, software-license and service-specific item/catalog workflows absent | WP16–WP17, WP30, WP38 |
| 3 | LANGUAGE REQUIREMENT | PARTIAL | [L] [U] | No global EN/AR language switch, full RTL UI or bilingual documents | WP11, WP44 |
| 4 | BILINGUAL MASTER DATA | PARTIAL | [L] [T] | Only Company bilingual fields; Product/Customer/Supplier/Category bilingual masters missing | WP11–WP16 |
| 5 | COMPANY MASTER | PARTIAL | [C] [G] | Company CRUD and logo code present; logo consistency, validation and document identity require tests/fixes | WP10, WP44 |
| 6 | USER MANAGEMENT | PARTIAL | [A] [P] [U] | Login exists; employee details, user management, branch, status and role assignment screens/APIs absent | WP05, WP07–WP09 |
| 7 | USER PERMISSIONS | PARTIAL | [P] [R] | Django models exist; permission catalog APIs, role/user grants and server-side per-action checks absent | WP06–WP09, WP46 |
| 8 | CUSTOMER MASTER | ABSENT | [T] | Customer model, bilingual CRUD, code, terms, credit, attachments absent | WP12 |
| 9 | CUSTOMER LEDGER | ABSENT | [T] | Customer debit/credit ledger, statement and balances absent | WP32–WP33, WP43 |
| 10 | SUPPLIER MASTER | ABSENT | [T] | Supplier model and bilingual CRUD, payment terms and opening balance absent | WP13 |
| 11 | SUPPLIER LEDGER | ABSENT | [T] | Supplier payable ledger, statement, allocation and outstanding absent | WP27, WP43 |
| 12 | PRODUCT / ITEM MASTER | ABSENT | [T] [D] | Product/SKU/barcode, prices, descriptions, tax, reorder and product schema absent | WP16, WP18–WP20 |
| 13 | PRODUCT TYPES | ABSENT | [T] | Stock/non-stock/digital item behavior and license lifecycle absent | WP17 |
| 14 | CATEGORY & BRAND | ABSENT | [T] | Category, subcategory, brand and bilingual master APIs/UI absent | WP14–WP15 |
| 15 | SERIAL NUMBER MANAGEMENT | ABSENT | [T] [D] | Serial uniqueness, intake, sale selection and provenance absent | WP22, WP42 |
| 16 | WARRANTY MANAGEMENT | ABSENT | [T] | Warranty linked to invoice/customer/serial and status check absent | WP23 |
| 17 | PURCHASE MANAGEMENT | ABSENT | [T] | PO, goods receipt, approval and supplier procurement absent | WP24 |
| 18 | PURCHASE INVOICE | ABSENT | [T] [D] | Purchase invoice/posting and stock increase absent | WP25 |
| 19 | PURCHASE RETURN | ABSENT | [T] | Purchase return and stock/payable reversal absent | WP26 |
| 20 | QUOTATION MANAGEMENT | ABSENT | [T] | Quotation create, approval and lifecycle statuses absent | WP28 |
| 21 | QUOTATION PRINTING | ABSENT | [T] | English/Arabic/bilingual quotation printing absent | WP28, WP44 |
| 22 | QUOTATION TO SALES INVOICE | ABSENT | [T] | One-time quotation-to-sales conversion and reference preservation absent | WP29 |
| 23 | SALES INVOICE | ABSENT | [T] | Direct/converted sales invoice models, API and print absent | WP29–WP30 |
| 24 | CASH SALES | ABSENT | [T] | Cash-sale checkout and paid-in-full allocation absent | WP30–WP31 |
| 25 | CREDIT SALES | ABSENT | [T] | Credit sale, outstanding and limit enforcement absent | WP30–WP33 |
| 26 | CUSTOMER PAYMENT / RECEIPT | ABSENT | [T] | Customer receipt, partial allocation, KNET/card/transfer handling absent | WP19, WP32 |
| 27 | SALES RETURN / CREDIT NOTE | ABSENT | [T] | Sales return, credit note, stock-in/refund and audit absent | WP34 |
| 28 | TAX / VAT MANAGEMENT | ABSENT | [T] [D] | No configurable tax category/rates or decimal invoice calculator | WP18, WP41 |
| 29 | INVENTORY MANAGEMENT | ABSENT | [T] [D] | No stock movement ledger or transactional purchase/sale/return posting | WP21, WP25–WP26, WP30, WP34 |
| 30 | STOCK ADJUSTMENT | ABSENT | [T] | Adjustment reasons, approval and audit absent | WP35 |
| 31 | STOCK TRANSFER | ABSENT | [T] | Warehouse transfer, status and balanced stock movements absent | WP36 |
| 32 | PHYSICAL STOCK COUNT | ABSENT | [T] | Physical count, variance review and adjustment approval absent | WP35 |
| 33 | LOW STOCK ALERT | ABSENT | [T] | Reorder thresholds and low-stock dashboard alert absent | WP16, WP40 |
| 34 | STOCK VALUATION | ABSENT | [T] | Costing-method decision, valuation and stock-value report absent | WP37, WP42 |
| 35 | PROFIT MANAGEMENT | ABSENT | [T] | Profit calculations including discounts/returns/costs absent | WP37, WP41 |
| 36 | SERVICE / REPAIR MODULE | ABSENT | [T] | Service and repair lifecycle absent | WP38–WP39 |
| 37 | JOB CARD | ABSENT | [T] | Job card, technician, status transitions and device intake absent | WP38 |
| 38 | DASHBOARD | ABSENT | [U] [T] | Dashboard shell and KPI aggregates for sales, purchases, dues, stock, quotation/service absent | WP40 |
| 39 | REPORTS | ABSENT | [T] | Sales/purchase/stock/customer/supplier/quotation reports and filters absent | WP41–WP43 |
| 40 | DOCUMENT PRINTING | ABSENT | [T] [C] | Company invoice fields exist but no quotation/invoice/receipt/job-card print engine | WP10, WP44 |
| 41 | PAPER SIZES | ABSENT | [T] | A4/A5/thermal printable and configurable layout support absent | WP44 |
| 42 | BARCODE SUPPORT | ABSENT | [T] | Scan-to-cart, barcode lookup and label generation absent | WP31, WP45 |
| 43 | SEARCH | PARTIAL | [C] [Q] [T] | Company local-search only; global indexed product/serial/customer/document search absent | WP16, WP42, WP45 |
| 44 | DATA EXPORT | ABSENT | [T] | Excel/PDF/CSV exports and per-role export checks absent | WP41–WP44 |
| 45 | BACKUP & RESTORE | ABSENT | [T] | Backup scheduler/history, manual backup and tested restore absent | WP47 |
| 46 | MULTI-BRANCH READY ARCHITECTURE | PARTIAL | [E] [D] | Dual backend foundation exists; explicit branch-scoped users/data/models not present | WP09, WP36, WP48–WP50 |
| 47 | MULTI-WAREHOUSE | ABSENT | [T] | Warehouse entities and per-warehouse balances absent | WP09, WP36 |
| 48 | PRICE MANAGEMENT | ABSENT | [T] | Retail/wholesale/corporate price lists and selection absent | WP20 |
| 49 | DISCOUNT MANAGEMENT | ABSENT | [T] | Item/invoice discount types, caps and permission policy absent | WP20 |
| 50 | PAYMENT TERMS | ABSENT | [T] | Customer/supplier payment terms and due-date rules absent | WP19 |
| 51 | CREDIT LIMIT | ABSENT | [T] | Credit limit, outstanding and available-credit validation absent | WP12, WP31–WP33 |
| 52 | CUSTOMER DOCUMENT ATTACHMENTS | ABSENT | [T] | Optional protected customer/supplier attachments absent; confirm access/retention scope | WP12–WP13, WP46 |
| 53 | NOTIFICATIONS / ALERTS | ABSENT | [T] | Low-stock, overdue, warranty, quotation and repair alerts absent | WP40 |
| 54 | NUMBERING SYSTEM | ABSENT | [T] | Configurable year/branch-aware document numbers and uniqueness absent | WP02, WP24–WP34 |
| 55 | IMPORTANT BUSINESS WORKFLOWS | ABSENT | [T] [B] | Seven business workflows are documented but none implemented end-to-end | WP24–WP39, WP49 |
| 56 | DATABASE DESIGN REQUIREMENT | PARTIAL | [D] [M] | Identity/Company migration exists; full normalized transaction schema/FKs/indexes absent | WP04, WP21, WP24–WP37 |
| 57 | DATA INTEGRITY | PARTIAL | [M] [D] [T] | Existing identity FKs; financial/serial/document/stock atomicity rules absent | WP04, WP18, WP21–WP37, WP46 |
| 58 | TRANSACTION STATUS | ABSENT | [T] | Draft/post/approve/reverse financial state machines and authorization absent | WP24–WP39, WP46 |
| 59 | SECURITY REQUIREMENTS | PARTIAL | [A] [P] [M] | Authentication and CSRF exist; granular authorization, audit, tested recovery absent | WP05–WP09, WP46–WP47 |
| 60 | FUTURE ACCOUNTING INTEGRATION | FUTURE-DECISION | [B] [T] | Accounting integration model/events and scope approval pending; no live GL claimed | WP01, WP48, WP50 |
| 61 | FUTURE API INTEGRATION | PARTIAL | [E] [B] | REST architecture exists; external service adapters/credentials not implemented or approved | WP02, WP48, WP50 |
| 62 | MOBILE / WEB RESPONSIVENESS | PARTIAL | [U] [E] | Basic responsive CSS present; tablet flows and full mobile navigation untested | WP11, WP48 |
| 63 | RECOMMENDED MAIN MENU | PARTIAL | [U] [R] | Only Company Master in sidebar; SRS business menu and permission-gated routes absent | WP07–WP09, WP12–WP45 |
| 65 (acceptance) | MINIMUM ACCEPTANCE CRITERIA | ABSENT | [T] [B] | All 13 mandatory acceptance cases remain unverified on both backends and React | WP49 |
| 65 (developer notes) | IMPORTANT DEVELOPER NOTES | PARTIAL | [B] [M] [T] | Architecture and bilingual Company fields present; most 18 developer invariants unimplemented | WP01–WP50 |
| 66 | PHASE-WISE DEVELOPMENT RECOMMENDATION | PARTIAL | [B] [C] [T] | Plan maps four source phases; implementation remains limited to auth/Company foundation | WP01–WP50 |
| 67 | FINAL SYSTEM CONCEPT | ABSENT | [T] [B] | Supplier→purchase→stock→sale/service→payment and quotation chain absent | WP24–WP39, WP49 |
| 68 | SUCCESS CRITERIA | ABSENT | [T] | No production KPI/report endpoints answering 18 management questions | WP40–WP43, WP49 |

## SRS acceptance test trace (none passed at this code snapshot)

| AT | Acceptance | Implementation dependency | Result at review |
|---|---|---|---|
| AT-01 | Product→purchase→stock increases | WP16, WP21, WP25 | Pending; no passing E2E evidence |
| AT-02 | Customer→quotation→print | WP12, WP28, WP44 | Pending; no passing E2E evidence |
| AT-03 | Approved quotation→sales invoice | WP28–WP30 | Pending; no passing E2E evidence |
| AT-04 | Direct sales→stock decreases | WP21, WP30 | Pending; no passing E2E evidence |
| AT-05 | Credit invoice→customer outstanding increases | WP30–WP33 | Pending; no passing E2E evidence |
| AT-06 | Receipt→customer outstanding decreases | WP32–WP33 | Pending; no passing E2E evidence |
| AT-07 | Sales return→stock increases | WP21, WP34 | Pending; no passing E2E evidence |
| AT-08 | Purchase return→stock decreases | WP21, WP26 | Pending; no passing E2E evidence |
| AT-09 | Purchased serial→sale→customer warranty | WP22–WP23, WP25, WP30 | Pending; no passing E2E evidence |
| AT-10 | English/Arabic documents print correctly | WP11, WP44 | Pending; no passing E2E evidence |
| AT-11 | Low-stock condition→dashboard alert | WP21, WP40 | Pending; no passing E2E evidence |
| AT-12 | Unauthorized restricted action denied | WP06–WP08, WP46 | Pending; no passing E2E evidence |
| AT-13 | Cancelled transaction retains audit trail | WP26, WP34, WP46 | Pending; no passing E2E evidence |

## Confirmed code gaps / defect register

| ID | Source-level evidence | Work and safe exit gate |
|---|---|---|
| GAP-001 | `[P]`, `[R]`, `[U]`: framework roles/Django permission models exist; no ERP Role/User/Permission management route, UI or action policy. | WP06–WP09: parity contract, secure CRUD, server-side positive/negative tests. |
| GAP-002 | `[G]`, `[C]`: .NET logo save uses `FileMode.Create` for `company-{id}{ext}` before DB commit; Django `_save_logo` deletes existing path before `company.save`. A failed write can destroy/replace the prior logo; create spans DB and filesystem without cleanup. | WP10: write new unique temp object, validate content, commit DB reference, cleanup old file after success; test DB-save/file failures before rollout. |
| GAP-003 | `[Q]`: .NET Company GET materializes all rows via `ToListAsync`; Django `ModelViewSet` has no explicit paging configuration. | WP10/WP48: contract-preserving paged endpoint, indexed ordering and React page handling; verify with large data. |
| GAP-004 | `[L]`, `[U]`: only Company fields have explicit Arabic data; no global RTL/language switch or bilingual document templates. | WP11/WP44: cross-backend Unicode, RTL/UI and printable English/Arabic test. |
| GAP-005 | `[D]`, `[R]`, `[T]`: only Identity and Company schema/routes exist; no purchase/sale/inventory/serial/ledger/return or document-number entities. | WP16–WP39: normalized decimal/Unicode model design, transactional posting and required acceptance tests. |
| GAP-006 | `[M]`: .NET ASP.NET Identity `EmailIndex` on NormalizedEmail is non-unique while Django email is unique; app-side RequireUniqueEmail does not replace concurrent DB enforcement. | WP04/WP08: inspect existing email duplicates/collation; add safe filtered unique index and concurrency tests. |
| GAP-007 | `[C]`, `[R]`: Company endpoints require authentication but not granular View/Add/Edit/Delete permissions; no audit trail for deletes. | WP06–WP10/WP46: enforce action policies; decide delete/archive policy and audit; test unauthorized action. |
| GAP-008 | `[T]`: no tracked app test projects/suites or migration/React E2E regression matrix found. | WP03/WP49: restore tests, CI and both-backend SQL Server parity verification. |

## Scoping and database decisions

- IDs remain numeric auto-increment; SQL Server 2019, .NET 10, Django and React parity are project constraints.
- Financial amounts require decimal precision and chosen KWD rounding; no transaction schema exists yet, so do not claim a precision fix was applied.
- Bilingual master fields must be Unicode and invoice/quotation print must support English, Arabic and bilingual output.
- Do not assume a current Kuwait VAT rate or commit live payment gateway settings; tax policy and future Phase-4 integrations require business approval.
- Existing auth/Company schemas of the two backends need contract parity, not identical framework-owned tables.
- Source SRS has no section 64 and uses section 65 twice; both 65 requirements are separately tracked above.

**Coverage:** 68 source headings mapped; PARTIAL=16, ABSENT=51, FUTURE-DECISION=1. No full business module is marked complete by this matrix.
