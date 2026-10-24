# WP11 — English/Arabic and RTL foundation

**Scope:** Language toggle, stable translation keys, React RTL, bilingual Unicode storage and a bilingual Company identity print preview. Full quotation/invoice/report rendering is owned by WP27/WP30/WP44.

- `frontend/src/i18n.tsx` uses complete typed EN/AR dictionaries, persists selected language per browser and assigns `lang` and `dir` to document element.
- Permission grants remain *language-independent action codes*. `frontend/src/locale.ts` translates catalog module/action captions for Arabic without changing security policy keys.
- Date/currency formatting accepts the locale explicitly and uses built-in `Intl`; monetary arithmetic belongs to WP18, not JS floats. No hardcoded tax rate.
- Company identity preview includes RTL Arabic fields and locale date; is **not** a purchase/quotation invoice printer.
- Keyboard forms preserve Enter-to-next-field except textarea where Enter inserts newline; Tab/Shift-Tab, checkbox Space and native select arrows remain operational.
- Backend Company Unicode save/search is SQL Server-tested; Arabic document transactions depend on future business modules.

**Negative scope:** Missing arbitrary translated texts cannot be silently added at runtime because the complete `Record<keyof English,string>` checks build-time keys; unknown backend validation text still requires translation mapping. Quotation RTL output is deferred until quotation module exists. Physical printing and currency-format audits are future owner WP44.

## ERP-0201 — SRS acceptance extraction (2026-10-23)

Source: original SRS v1.0, sections §§3, 4, 40, 41, 62 and 65 (linked by `ERP_PROGRESS.json`).

| SRS section | Verifiable requirement in this work package | Owner/dependency boundary |
| --- | --- | --- |
| §3 Language | EN/AR application toggle, complete bilingual interface, Unicode persistence for Arabic | React language context and bilingual model fields; financial documents require their actual document modules |
| §4 Master data | English and Arabic names/description stored separately on Company, Customer, Supplier, Product, Category and Brand as applicable | Each master is implemented/verified by its own owner WP10–WP16; no placeholder translations of business data |
| §40 Printing | Quotation, invoice, receipts and other financial documents should offer EN/AR/bilingual output | WP27 quotation, WP30 invoice, WP44 document printing; **not** implemented or certified by this requirement-extraction step |
| §41 Paper sizes | A4, A5, thermal; configurable layout | WP44 and physical printer acceptance; no layout engine fabricated in WP11 |
| §62 Responsive | Desktop/laptop/tablet responsiveness; mobile an optional future capability | Current React layout/RTL direction and navigation tested only for available screens |
| §65 Test 10 | Create and print the same business document in EN and AR | Deferred E2E until WP27/WP30/WP44 document model, tax and printing workflows exist |

**Current owned acceptance:** language change updates `lang`/`dir` and translated labels, existing Company/partner/catalog fields round-trip Arabic Unicode without replacement, localized date/currency display uses `Intl`, and existing Company identity preview is printable as a preview only. No tax/invoice arithmetic is performed in localized JavaScript.

**Negative gates:** unexpected missing translation keys fail typed dictionary builds; keyboard focus and RTL controls must not be displaced; app must not confuse Arabic interface with translated database values; Unicode encoding must remain unchanged across SQL Server APIs. Later document printing must test both scripts, mixed direction, page sizes and physical output.

**Assumptions / exclusions:** keep action/permission codes language-neutral, money storage uses decimal database types, numeric BIGINT PKs unchanged. The SRS's document printing and whole-system test cases are explicit downstream-owner acceptance, not a reason to claim an unbuilt quotation is functional. This is step ERP-0201 requirement extraction; ERP-0202 code inspection remains open.

## ERP-0202 — source inspection & observed behavior (2026-10-24)

**Code inspected at:** `b8d966147840c4e4a92ea3f5ec3b9f88dcc71b51`. **Evidence run:** [CI 40002127807](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40002127807), all 5 jobs successful. This is the *source-inspection task*, not verification of the entire localization package.

| Surface | Exact current code | Inspected behavior and boundary |
| --- | --- | --- |
| React EN/AR switch | `frontend/src/i18n.tsx`, `frontend/src/components/AppShell.tsx`, `frontend/src/main.tsx` | Selected language is saved in localStorage; `documentElement.lang` and `dir` become `en/ltr` or `ar/rtl`. English object + Arabic `Record<keyof typeof english,string>` checks all declared translation keys at TS build time. Language UI uses an accessible select. No translation API or database translation table needed for this package. |
| React UI & RTL | `frontend/src/components/{Login,Companies,Roles,Users,Organization,Partners,Catalog}.tsx`, `frontend/src/styles.css`, `frontend/src/forms/keyboard.ts` | Labels and edit actions call typed `t(...)`; Arabic names/addresses use `dir="rtl"`; CSS has `[dir="rtl"]` table/sidebar alignment and a 900px single-column breakpoint. Keyboard behavior skips textarea Enter, keeps form navigation; Playwright covers narrow 375px viewport, role/Company form focus and Arabic navigation. |
| Validation/localized errors | `frontend/src/i18n.tsx` `languageError`, `frontend/src/api/client.ts`, `django/apps/companies/serializers.py`, `django/apps/partners/api.py`, `django/apps/catalog/api.py`, `aspnet-core/src/ITRetailERP.Web/Contracts/{PartnerRequests,CompanyRequest,CatalogRequests}.cs` | ASP.NET returns language-neutral English/generic `detail` or model-validation failures. Django DRF serializers return field-specific error dictionaries. The frontend translates only mapped known detail strings; unknown server messages may appear untranslated and DRF field errors currently fall back to generic client feedback. Validation translation parity is NOT certified; next gap-comparison step owns the findings. |
| Unicode and database IDs | `django/apps/{companies,partners,catalog}/models.py`, `aspnet-core/src/ITRetailERP.Web/Models/{Company,Customer,Supplier,Category,Brand,Product}.cs`, migrations and EF snapshot | Separate English and Arabic strings; SQL Server nvarchar and BIGINT identity; monetary and amount data stored as decimal, never translated. Company and partner Arabic save/reload exists in both integration suites. No localization table/migration required for existing bilingual fields. |
| API and permissions | `django/apps/companies/api.py`, `django/apps/partners/api.py`, `aspnet-core/src/ITRetailERP.Web/Controllers/Api/{CompaniesApiController,CustomersApiController,SuppliersApiController}.cs`, `frontend/src/locale.ts` | Business APIs persist EN/AR values; permission action codes remain invariant while React translates display captions. There is no locale parameter changing authorization or storage schema. |
| Current print preview | `frontend/src/components/Companies.tsx`, `frontend/src/styles.css` `@media print`, `frontend/src/locale.ts` | Company identity preview renders English/Arabic names and addresses, localized `printedOn` date, print-only isolation; is not a quotation, invoice, receipt, PDF or physical printer test. |
| CI observed | `.github/workflows/erp-verification.yml`, `frontend/e2e/erp.spec.ts` | 40002127807: Django SQL Server 72/72; .NET xUnit 4/4, migrations and API smoke; Django Playwright 16/16; ASP Playwright 14/14; builds passed. Neither A4/A5/thermal print tests nor a fully translated financial-document test is included. |

**Inspection findings for ERP-0203:** (1) duplicated RTL/sidebar alignment CSS selectors, so review for non-functional cleanup; (2) error translation is finite-string mapping rather than complete parity with DRF field-level failures, and unknown backend errors can remain in English; (3) mobile navigation is responsive but no full accessibility/mixed-script audit has yet been evidenced; (4) `formatMoney` formats a JS `number` for *display* only, not exact financial posting calculations; (5) quotation/invoice/physical print output is rightly deferred to WP27/WP30/WP44. Record and prioritize these against SRS acceptance before any WP11 claim.

No database schema or source runtime modification was required to *inspect* these files. Security restrictions and numeric identity policy remain unchanged.
