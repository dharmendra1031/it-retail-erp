# ERP-0316 — Product Master bilingual RTL, keyboard and decimal verification

**Reviewed source commit:** `e7c8247d37efd2656c1da990b2c423ab0a8f5105` on `development`.  
**Verified CI:** [40660802519](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40660802519) — five jobs SUCCESS (frontend, ASP.NET, Django, browser and disposable SQL Server).

## Tested improvements

- `frontend/e2e/erp.spec.ts` now has an Arabic Product flow: creates bilingual Category/Unit, changes to Arabic, confirms document `dir=rtl`, LTR SKU, RTL Arabic Product input, Enter focus advancement, Arabic master selectors, decimal price/reorder inputs, Product save/list readback and a narrow 390px viewport.
- `django/apps/catalog/tests.py` has a Product API round-trip case with Arabic diacritics in name and description, edit/readback, three-place exact money strings and six-place reorder string.
- `aspnet-core/tests/smoke_sqlserver.py` now asserts Product create/readback retains Arabic name, cost/base/min prices and the six-place reorder level without binary floating point conversion.
- Shared existing `frontend/src/forms/keyboard.ts` used, with native Tab and arrow controls unaffected; no extra CSS or localization library introduced.

## Scope / test boundaries

Current Product form is an admin entry screen; English and Arabic labels are provided by the existing i18n dictionary with document `lang/dir`. HTML input patterns enforce up to 3/6 decimal places before API validation. Future currency formatting for sales/receipts and Arabic print output belongs WP44; no tax/price list or stock transaction posting here.

CI 40660802519 passed across both React browser configurations and SQL Server; production DB not accessed. No migration/index or model changes. Final permission-audit/branch-scope behavior stays with current and future security packages, and granular nonadmin Product UI navigation is not implemented yet. Next ERP-0317 Product positive ASP.NET validations.
