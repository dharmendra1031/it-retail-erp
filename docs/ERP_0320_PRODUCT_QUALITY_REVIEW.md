# ERP-0320 — Product Master quality and closeout review

**Review base:** `d73e2503319345597be4daa79ed4ab4d8a4522e9`, `development`. **Package:** WP16, ERP-0301–ERP-0320. **Original scope:** Product SKU/barcode, bilingual names/descriptions, category/brand/unit, stock/nonstock/digital type, cost/base/min price, reorder, status, secure CRUD/search, browser Product Master. The later-created ProductLicense work belongs WP17.

## Source and evidence inspected

- ASP.NET: `Models/Product.cs`, `Contracts/ProductRequest.cs`, `Controllers/Api/ProductsApiController.cs`, `Data/ApplicationDbContext.cs`, migrations `20261023140000_Products` and `20261028150000_ProductTypeStockSettings`; SQL integration tests `ProductCreationTests.cs`, `ProductSearchTests.cs`, `smoke_sqlserver.py`, `product_schema_sqlserver.py`.
- Django: `apps/catalog/models.py`, `api.py`, migrations `0002_product`/`0004_product_type_stock_settings`, Product API and SQL-concurrency tests in `apps/catalog/tests.py`.
- Shared React: `src/components/Products.tsx`, `src/api/products.ts`, `src/App.tsx`, `src/components/AppShell.tsx`, `src/i18n.tsx`, `e2e/erp.spec.ts`.
- Existing `docs/api-contract.md` contained an outdated claim that Product pagination did not exist in the earlier ERP-0311 section, contradicted by later ERP-0315 and current source. This commit corrects the contract, preserves the legacy unpaged response and documents the already-built ProductLicense API separately from WP16 completion.

## Quality review and findings

| Check | Code evidence | Result / owner |
| --- | --- | --- |
| Developer-style maintainability | One focused Product controller/API serializer and React Product component using existing Catalog API/keyboard helpers; no extra service layers | Existing code reused; no refactor needed solely to reduce line counts |
| Data and concurrency | EF/Django unique SKU and filtered nullable-barcode constraints; SQL Server duplicate-write guards with normal 400 responses; type CHECK and protected FKs | Verified by prior SQL Server test evidence, ERP-0319; no duplicate schema/migration |
| Security | `products.view/add/edit/delete` enforced server-side, antiforgery on writes; no secrets in Product response. Digital-license reveal is separate permission-gated endpoint | Backend controls present; license threat model and audit still WP17/WP46 |
| Scale | Both backends support `?page=&pageSize=&search=` and bounded page size (1–100), with legacy unpaged array retained | Product UI uses pages of 25; future broad listing/large-table performance WP48 |
| Localization | EN/AR Unicode, LTR identifier inputs, RTL name fields; product keyboard/RTL Playwright flows | Earlier WP16 CI acceptance captured; print/report localization belongs WP44 |
| Permission-aware React navigation | `App.tsx` forces non-admin users to Companies; `AppShell.tsx` hides Product and other masters behind `user.isAdmin` | Known usability/role-grant gap: delegated non-admin Product users cannot open Product UI even with backend `products.view`. Requires a shared client capability contract and permission-aware navigation; not a server-side security bypass. Track as follow-up for permission UI integration; do not weaken backend policies by blindly showing management buttons. |
| ProductLicense form keyboard handling | `ProductLicenses.tsx` does not use shared `advanceOnEnter` on its nested form | WP17 UI/keyboard acceptance: add helper and Playwright coverage without altering completed WP16 Product form |
| Product list backward compatibility | Unpaged list remains potentially unbounded; paged mode enforced by React | Maintain legacy clients until a coordinated paging-only version; general performance work WP48 |
| Secret/configuration | Key encryption uses deployment `PRODUCT_LICENSE_SECRET`, checked when crypto operations run | WP17 operations/deployment docs must require persistent secret; rotation needs data migration |
| Documentation | ERP-0311 paragraph contradicted ERP-0315 and live source | Fixed here. Digital-license route/security overview added; pending WP17 acceptance distinguished from already committed code |

## Verification and limits

Baseline `development` CI [40685879289](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40685879289) passed all five jobs (ASP.NET, Django, React, browser and SQL Server) for `21b46ee1`. ERP-0319's documentation-only commit `d73e2503` triggered CI [40997526436](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40997526436); record its actual final result when available, never presume pass. For ERP-0320 no application source, schema, test or deployment modifications were made; documentation correction plus code review require no new runtime test by themselves, while GitHub Actions provides a regression gate after commit.

**WP16 closeout:** Product Master functionality implemented/tested for approved scope. Open business-policy choices such as separate Item Code, Model, Purchase/Wholesale prices and Tax mapping were not guessed; retain their explicit owner/decision contracts from `ERP_0306_PRODUCT_DATA_DESIGN.md`. No stock ledger, sale posting, invoice, tax posting or production migration is claimed. Future WP17, WP18, WP20, WP21/25, WP44/46/48 and final integration own those parts.

**Next:** ERP-0321, extract stock/non-stock/digital license behavior acceptance from SRS, verify existing early implementation against the contract rather than rewriting it.
