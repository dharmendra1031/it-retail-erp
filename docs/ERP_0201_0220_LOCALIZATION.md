# WP11 — English/Arabic and RTL foundation

**Scope:** Language toggle, stable translation keys, React RTL, bilingual Unicode storage and a bilingual Company identity print preview. Full quotation/invoice/report rendering is owned by WP27/WP30/WP44.

- `frontend/src/i18n.tsx` uses complete typed EN/AR dictionaries, persists selected language per browser and assigns `lang` and `dir` to document element.
- Permission grants remain *language-independent action codes*. `frontend/src/locale.ts` translates catalog module/action captions for Arabic without changing security policy keys.
- Date/currency formatting accepts the locale explicitly and uses built-in `Intl`; monetary arithmetic belongs to WP18, not JS floats. No hardcoded tax rate.
- Company identity preview includes RTL Arabic fields and locale date; is **not** a purchase/quotation invoice printer.
- Keyboard forms preserve Enter-to-next-field except textarea where Enter inserts newline; Tab/Shift-Tab, checkbox Space and native select arrows remain operational.
- Backend Company Unicode save/search is SQL Server-tested; Arabic document transactions depend on future business modules.

**Negative scope:** Missing arbitrary translated texts cannot be silently added at runtime because the complete `Record<keyof English,string>` checks build-time keys; unknown backend validation text still requires translation mapping. Quotation RTL output is deferred until quotation module exists. Physical printing and currency-format audits are future owner WP44.
