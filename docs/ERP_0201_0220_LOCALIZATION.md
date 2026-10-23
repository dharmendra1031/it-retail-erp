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
