# IT Retail ERP — SRS baseline and delivery boundaries

**Baseline ID:** SRS-v1.0 / ERP-0001
**Source document:** [Computer Hardware & IT Retail Management System SRS](https://docs.google.com/document/d/1Gb_pMJAN14UY0scLJjGBGiuRZdlXOWJARB1aLkzIobc/edit?usp=sharing)
**Source last modified:** 2026-09-09T13:09:35.807Z
**Repository HEAD inspected before this step:** `42127710bb9b3ebff2f46304959a318a065b87a0` (`development`).
**Scope of this step:** extract and trace source intent, workflows, mandatory acceptance and open decisions. Runtime implementation inventory, code-gap comparison and actual test execution belong to ERP-0002 onward.

## 1. Business objective and supported product types (SRS §§1–2)

The system serves a Kuwait computer/IT retail and trading business. It covers hardware, software/digital licenses and paid IT services, from supplier procurement through inventory and sale/service to customer payments and reports.

**Required high-level capabilities from §1 (22):** Computer Hardware Sales; Software Sales; Quotations; Sales Invoices; Credit Sales; Cash Sales; Purchase Management; Inventory / Stock Management; Serial Number Management; Warranty Management; Customer Management; Supplier Management; Customer Receivables; Supplier Payables; Payments & Receipts; Tax/VAT Configuration; Product Profitability; Repair & Service Management; Job Cards; Reports; English & Arabic bilingual operation; User permissions.

**Business classifications from §2:**
- Stocked hardware: desktops, laptops, monitors, processors, RAM, storage, printers, networking equipment, peripherals and accessories.
- Software/digital goods: operating systems, office applications, antivirus, software licenses and other digital products.
- Services: installation, formatting, upgrades, virus removal, repair, data recovery, networking and IT support.
- Stock, non-stock and digital items are separate transaction behaviors; detailed field/type acceptance is owned by WP16–WP17.

## 2. Seven mandatory business workflows (SRS §55)

- **WF-01 — Purchase:** Supplier → Purchase Order → Goods Receipt / Purchase Invoice → Stock Increase → Supplier Payable → Supplier Payment.
- **WF-02 — Quotation:** Customer → Quotation → Customer Approval → Convert to Sales Invoice → Payment / Credit → Stock Decrease.
- **WF-03 — Direct Sales:** Customer → Sales Invoice → Payment → Stock Decrease.
- **WF-04 — Credit Sale:** Customer → Credit Sales Invoice → Customer Outstanding → Payment Receipt → Outstanding Balance Update.
- **WF-05 — Sales Return:** Original Sales Invoice → Sales Return / Credit Note → Stock Increase → Customer Balance Adjustment.
- **WF-06 — Purchase Return:** Purchase Invoice → Purchase Return → Stock Decrease → Supplier Balance Adjustment.
- **WF-07 — Repair:** Customer → Job Card → Diagnosis → Repair → Service Charges → Ready → Delivery.

Each workflow must preserve transaction status, document references, posting idempotency, stock and ledger effects. These are acceptance targets, not claims that the features already run.

## 3. Thirteen required SRS acceptance tests (SRS §65 — Minimum Acceptance Criteria)

Every case is **pending** until the identical business outcome passes with the React frontend and both ASP.NET/Django APIs against safe SQL Server test databases. Permissions/stock/financial cases require negative tests too.

| SRS test | Expected observable result | Owning plan packages | Initial status |
|---|---|---|---|
| AT-01 | Create Product → Purchase Product → Stock Increases. | WP16, WP21, WP25 | Pending — no verified E2E evidence |
| AT-02 | Create Customer → Create Quotation → Print Quotation. | WP12, WP28, WP44 | Pending — no verified E2E evidence |
| AT-03 | Convert Quotation → Sales Invoice. | WP28–WP30 | Pending — no verified E2E evidence |
| AT-04 | Create Direct Sales Invoice → Stock Decreases. | WP21, WP30 | Pending — no verified E2E evidence |
| AT-05 | Create Credit Invoice → Customer Outstanding Increases. | WP30–WP33 | Pending — no verified E2E evidence |
| AT-06 | Receive Customer Payment → Outstanding Decreases. | WP32–WP33 | Pending — no verified E2E evidence |
| AT-07 | Create Sales Return → Stock Increases. | WP21, WP34 | Pending — no verified E2E evidence |
| AT-08 | Create Purchase Return → Stock Decreases. | WP21, WP26 | Pending — no verified E2E evidence |
| AT-09 | Purchase Serial Number → Sell Serial Number → Warranty linked to Customer. | WP22–WP23, WP25, WP30 | Pending — no verified E2E evidence |
| AT-10 | Create the same documents in English and Arabic → Print correctly. | WP11, WP44 | Pending — no verified E2E evidence |
| AT-11 | Create low stock condition → Dashboard displays Low Stock. | WP21, WP40 | Pending — no verified E2E evidence |
| AT-12 | Unauthorized user attempts restricted action → System blocks action. | WP06–WP08, WP46 | Pending — no verified E2E evidence |
| AT-13 | Cancelled financial transaction → Audit trail remains available. | WP26, WP34, WP46 | Pending — no verified E2E evidence |

## 4. Developer invariants (SRS §65 — Important Developer Notes)

- 1. Arabic and English must be treated as first-class languages throughout the system.
- 2. Product descriptions must be stored separately in English and Arabic.
- 3. Tax rates must be configurable and must not be hard-coded.
- 4. Serial-number tracking must be available for selected products.
- 5. Warranty must be linked with serial number and sales invoice.
- 6. Quotation must be convertible into Sales Invoice.
- 7. Direct Sales Invoice must also be possible.
- 8. Cash and Credit Sales must both be supported.
- 9. Customer outstanding must update automatically.
- 10. Purchase and Sales must automatically update stock.
- 11. Returns must automatically reverse the relevant stock/balance impact.
- 12. Posted financial transactions should not be permanently deleted.
- 13. Audit trail is mandatory.
- 14. The system should be designed for future multi-branch and multi-warehouse support.
- 15. Database design should support future accounting integration.
- 16. The system should be API-ready.
- 17. All reports should support filtering by date, customer, supplier, product, category, brand, salesperson and branch/warehouse where applicable.
- 18. The interface should be simple enough for counter sales users while providing advanced controls for management.

These constraints are mandatory across both backends and the frontend. In particular, posted financial records must retain audit history rather than be hard-deleted.

## 5. Source development phases (SRS §66)

### Source phase 1: Core System
**Source features:** Company Master; User & Roles; Customer; Supplier; Product; Category; Brand; Tax; Purchase; Sales; Quotation; Quotation → Invoice; Cash/Credit Sales; Customer Payment; Basic Inventory; Basic Reports; English/Arabic.

### Source phase 2: Advanced Inventory
**Source features:** Serial Number; Warranty; Multiple Warehouses; Stock Transfer; Physical Stock; Stock Adjustment; Barcode; Stock Valuation; Advanced Profit Reports.

### Source phase 3: Service
**Source features:** Job Card; Repair Management; Technician; Service Charges; Warranty Repair; Service Reports.

### Source phase 4: Advanced Business
**Source features:** Accounting; Expenses; Employee Commission; Multiple Branches; Advanced Dashboard; API Integration; Online Store; Mobile Application; Payment Integration.

**Plan interpretation:** the 1000-step plan implements the defined core retail, advanced inventory, service, reports, security, recovery and platform foundations. Source Phase 4 contains a mixture of concrete applications and future integrations. The precise accounting, expenses, commission, online-store, mobile and gateway deliverables need business approval before being represented as completed. Multi-branch/warehouse readiness and dashboard/report foundations are included; a full additional accounting/e-commerce/mobile application is not silently implied by API readiness.

## 6. End-to-end concept and traceability (SRS §67)

- **Retail cycle:** Supplier → Purchase → Inventory → Sales / Service → Customer → Payment → Profit / Reports.
- **Quotation cycle:** Customer → Quotation → Approval → Sales Invoice → Payment → Stock Update → Customer Ledger.
- **Traceability invariant:** for applicable items, the system must trace purchase to stock to the sold serial to customer to invoice/payment to warranty.

## 7. Management questions that reports must answer (SRS §68)

- MQ-01: How much did we sell today?
- MQ-02: How much did we purchase today?
- MQ-03: What is our current stock?
- MQ-04: What is the value of our stock?
- MQ-05: Which products are low in stock?
- MQ-06: Which products are selling most?
- MQ-07: Which customers owe us money?
- MQ-08: How much does each customer owe?
- MQ-09: Which suppliers do we owe?
- MQ-10: Which quotations are pending?
- MQ-11: Which quotations were converted into invoices?
- MQ-12: What is the profit on each sale?
- MQ-13: Which serial number was sold to which customer?
- MQ-14: Is the product still under warranty?
- MQ-15: Which repair jobs are pending?
- MQ-16: How much tax was charged?
- MQ-17: Which user created or modified a transaction?
- MQ-18: What is the total sales/purchase/profit for a selected period?

Reports/dashboard data must reconcile with posted source transactions; users should not need to manually total source documents to answer these questions.

## 8. Requirement-to-deliverable ownership

| SRS capability | Plan owner | Future completion evidence |
|---|---|---|
| Hardware sales | WP16–WP23, WP25, WP30–WP31 | Purchase → stock → invoice, serial and warranty where configured |
| Software and digital products | WP16–WP17, WP30–WP31 | License key and expiry where applicable; correct non-stock behavior |
| Quotations and approvals | WP28–WP29, WP44 | Draft → approval → one-time conversion; printable documents |
| Cash and credit sales | WP19–WP20, WP30–WP33 | Payment method, partial payment, credit limit and ledger consistency |
| Purchase, receipts and returns | WP24–WP27 | Stock and supplier payable posting/reversal |
| Inventory and stock counts | WP21–WP22, WP35–WP37, WP42 | Movement history, variance approval and valuation |
| Warranty and serialized tracking | WP22–WP23, WP42 | End-to-end supplier → customer serial provenance |
| Customer and supplier management | WP12–WP13, WP27, WP32–WP33, WP43 | Bilingual masters, statements, payables and receivables |
| Tax, price, discount and profitability | WP18–WP20, WP37, WP41 | Configurable tax, decimal math and role-based discounts |
| Repair and service/job cards | WP38–WP39 | Device intake → repair → delivery, parts and charges |
| Reporting and bilingual printing | WP11, WP40–WP44 | Management questions and English/Arabic/bilingual output |
| User permissions and audit | WP05–WP09, WP46 | Server-side role/action/branch denial; immutable financial trace |
| Backup and future integrations | WP47–WP50 | Recovery drills, scale and approved external integration boundaries |

Detailed section-by-section file ownership and actual coverage gaps will be built in ERP-0002/ERP-0003. This baseline records planned ownership, not an assertion that listed features exist.

## 9. Architecture and explicit delivery decisions

- **Confirmed project decision:** one React/TypeScript/Vite frontend against interchangeable ASP.NET Core .NET 10 and Django REST backends; identical `/api` semantics; Microsoft SQL Server; numeric auto-increment application primary keys (`BIGINT IDENTITY` / `BigAutoField`). The SRS technology recommendation describes an ASP.NET API approach; the two-backend parity requirement is a confirmed project-specific extension.
- **Language/currency:** English and Arabic are first-class, SQL text must preserve Unicode, and money uses decimal data types with explicitly tested rounding and KWD presentation.
- **Security/operation:** enforce permissions server-side, protect confidential files and secrets, audit financial status changes, verify backup/restore and keep production mutations behind explicit authorization.
- **Release rule:** all relevant source acceptance cases, backend/API parity and deployment/recovery checks must pass before calling a scoped release complete.

### Assumptions to validate rather than silently invent

| Decision ID | Working assumption / unresolved business question | Owner / decision gate |
|---|---|---|
| DEC-01 | The initial deployment is a single shop, while schema, permission filtering and references remain branch/warehouse-ready. Confirm launch branch/warehouse count. | Business owner; before branch/warehouse design (WP09, WP36). |
| DEC-02 | Tax rates/categories are configuration, not hard-coded. Confirm actual Kuwait tax treatment with an accountant/tax adviser before tax release. | Business accountant; WP18. |
| DEC-03 | Stock costing method (e.g. weighted average) is not fixed by SRS. Confirm one approach and return/landed-cost policy. | Business accountant; WP37. |
| DEC-04 | Negative stock is blocked by default unless an approved configuration and privilege explicitly allow it. | Business owner; WP21. |
| DEC-05 | Product/document numbering, period resets and branch-aware prefix rules require approval; numeric DB IDs remain separate from human document numbers. | Business owner; WP02 and WP24–WP34. |
| DEC-06 | Exact document engine, bilingual print templates, layout approval and thermal/A4/A5 test devices require business validation. | Operations owner; WP44. |
| DEC-07 | Phase-4 accounting, expenses, commission, e-commerce, dedicated mobile application and payment gateway go-live remain scope decisions, not presumptively delivered by this 1000-step plan. | Project owner; WP50 release gate / approved scope extension. |
| DEC-08 | Final hosting, off-site backup target, retention, access model, integration credentials and restore approval are environment-specific. | Operations/security owner; WP47–WP50. |

### Exclusions and constraints at this baseline

- No live payment-gateway connection, third-party API credentials, external mobile app or standalone general-ledger application is claimed to be implemented.
- No claim that the current repo passes the 13 acceptance cases or that a previous build output validates the current HEAD.
- No destructive SQL migration, production deployment, restore, third-party account action or `main` merge is authorized by this planning step.
- Open decisions above must be resolved before their dependent implementation or release gate; they do not justify fake defaults or skipping steps.

## 10. Verified repository starting evidence and remaining reviews

At reviewed HEAD, `README.md` describes the React + dual-backend SQL Server architecture; `docs/api-contract.md` lists authentication and Company Master routes; `aspnet-core/src/ITRetailERP.Web/Program.cs` configures Identity, environment loading and controllers; `django/config/api_urls.py` exposes authentication and Company API routes; `frontend/src/App.tsx` renders login and Company Master.

These are source-level observations only. They are **not** full API or runtime test evidence. ERP-0002 will inventory every relevant file, ERP-0003 will compare all requirements against actual implementations, and later gated steps will perform builds, migrations, unit/integration/E2E tests and bug repair.

**ERP-0001 completion evidence:** source SRS sections 1, 2, 55, both 65 headings, 66, 67 and 68 extracted; 7 workflows, 13 acceptance cases, 18 developer notes, 4 SRS phases and 18 management questions mapped; open scope assumptions/exclusions documented. Documentation structure audited separately; application tests not applicable to extraction-only work.
