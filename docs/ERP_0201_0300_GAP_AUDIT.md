# ERP-0201 to ERP-0300 — Source/SRS gap audit

Reviewed against the project SRS ("Computer Hardware, Software & IT Retail Management System", version 1.0), sections 3, 8, 10 and 14. As of commit `ffeb6181b53abe42a15ce68e43a84f0903b195b1`, the official `ERP_PROGRESS.json` remains at **200/1000**. This audit does **not** complete any tracker steps.

| Package | Existing code evidence | Open acceptance work |
| --- | --- | --- |
| WP11, 0201–0220: EN/AR and RTL | `frontend/src/i18n.tsx`, `frontend/src/locale.ts`, `frontend/src/components/Companies.tsx` | Check every error path, React screen, RTL keyboard focus and print layout; report/transaction layouts are owned later |
| WP12, 0221–0240: Customer Master | `django/apps/partners/models.py`, `aspnet-core/src/ITRetailERP.Web/Models/Customer.cs`, `frontend/src/components/Partners.tsx` | SRS §8 has Company Name, Contact Person, Telephone, Email, VAT/Tax Number, Opening Balance, Remarks and Customer Type values Cash/Credit/Individual/Company/Corporate/Government/Other. Current models do not cover all of these. Add fields and validate full cross-backend round-trip, branch authorization, numeric precision and document access |
| WP13, 0241–0260: Supplier Master | `django/apps/partners/models.py`, `aspnet-core/src/ITRetailERP.Web/Models/Supplier.cs`, `frontend/src/components/Partners.tsx` | SRS §10 requires Contact Person, Telephone, Credit Limit and Remarks, which are absent. Supplier browser save test fails against ASP.NET on CI 39989947895; locate true cause before marking complete. Ledger is a downstream owner |
| WP14, 0261–0280: Category and hierarchy | `django/apps/catalog/models.py`, `aspnet-core/src/ITRetailERP.Web/Models/Category.cs`, `frontend/src/components/Catalog.tsx` | Re-run SQL Server hierarchical insert, same-parent uniqueness, cycle rejection, FK/delete protection, English/Arabic and browser parity |
| WP15, 0281–0300: Brand and Unit | `django/apps/catalog/models.py`, `aspnet-core/src/ITRetailERP.Web/Models/Brand.cs`, `aspnet-core/src/ITRetailERP.Web/Models/Unit.cs`, `frontend/src/components/Catalog.tsx` | Verify unicode, duplicate code rejection, unit precision bounds, delete when referenced by products, keyboard-only create/edit and both backend browser suites |

## Verification and governance

- CI 39989947895: Django tests, Django Playwright, React build, ASP.NET build **PASS**; ASP.NET-backed Playwright Supplier flow **FAIL**.
- The earlier ASP.NET SQL smoke tests contain a working direct Supplier POST, but do not prove the shared React flow passes.
- All IDs are expected to remain numeric BIGINT identity/BigAutoField, and financial amounts must retain decimal(18,3) precision, never JavaScript floats for posting calculations.
- Add missing fields with forward-only additive migrations (and SQL Server upgrade/rollback tests) on both backends; keep React English/Arabic labels and keyboard-first forms aligned. No changes to existing production data are authorized by this audit.
- Keep 0201 as the next tracker step until the applicable SRS/CI acceptance gate is satisfied. Do not mark 300/1000 from file presence alone.
