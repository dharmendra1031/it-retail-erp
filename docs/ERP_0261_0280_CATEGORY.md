# WP14 — Category/Subcategory acceptance (ERP-0261 to ERP-0280)

**SRS:** §§4, 12, 14, 43, 63. **Code commit:** `067fe884cb14daa5ffa42bfb525d26f6b007bfab`.
**CI:** [40157974570](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40157974570) — **5/5 jobs PASS** (Django, React, ASP.NET, browser, disposable SQL Server). **No production database was accessed.**

## Acceptance evidence

| Step | Verified evidence / scope |
| --- | --- |
| ERP-0261 | **Category SRS scope and downstream owners.** SRS §§4,12,14,43,63: bilingual root/child categories, status, searchable listing and product relationship. Product merchandising/pricing and invoice rendering belong WP16–WP17/WP44. |
| ERP-0262 | **ASP.NET/Django/React code inventory.** Checked Category model, parent FK, filtered unique indexes, controller, DRF serializer, category tree and React API clients against actual source. |
| ERP-0263 | **Category implementation gap resolution.** Reviewed code and closed two owned gaps: backend search across code/EN/AR and Arabic-language parent dropdown/table labels. Database relationships were already present. |
| ERP-0264 | **Category positive acceptance.** API creates a bilingual root and child using numeric parentId; child category is referenced by a product and React displays parent and hierarchy without losing Arabic. |
| ERP-0265 | **Category negative acceptance.** Reject same-parent/root normalized duplicate, missing parent, self/deep-cycle reparent and referenced child/root deletion; unauthorized staff cannot mutate/read without grants. |
| ERP-0266 | **Category SQL schema design.** Existing BIGINT identity/BigAutoField Category ID, nullable BIGINT parent FK, NVARCHAR EN/AR names, bool active and Product CategoryId FK; no UUID or new table. |
| ERP-0267 | **Category constraints and rollback.** Filtered root-code and composite parent-code unique indexes prevent sibling collisions; FK restricts product/child deletion. SQL unique/FK race errors have explicit 400/409 fallbacks. |
| ERP-0268 | **ASP.NET category model/contract/controller.** Reused existing long-ID Category/CategoryRequest and guarded CRUD, adding query search by code/English/Arabic and FK-conflict handling on concurrent delete. |
| ERP-0269 | **Django category model/serializer/view.** Kept parent PROTECT, sibling/root uniqueness and cycle traversal; added Q-filter search to CategoryViewSet; validation duplicate details align with ASP.NET. |
| ERP-0270 | **Category migration/index verification.** No new Category migration: Django catalog 0001 and EF CatalogMasters/Products migrations already provide matching keys, indexes and foreign keys; green CI applied migrations on disposable SQL Server. |
| ERP-0271 | **Category REST/API parity.** Both systems expose GET/POST /api/categories, GET/PUT/DELETE /api/categories/{long}, GET /api/categories?search=term. Request fields code/nameEn/nameAr/parentId/isActive; standard 201/200/204/400/403/404/409. |
| ERP-0272 | **ASP.NET category operations.** Server normalizes ASCII code, checks parent ancestry, duplicate siblings, policy and SQL conflicts; writes once per request. POST duplicate returns 400; protected child/product delete returns 409. |
| ERP-0273 | **Django category operations.** CatalogViewSet wraps mutations in transaction.atomic, validates parent chain and normalized code; catches unique race and PROTECT exceptions without partially persisting invalid changes. |
| ERP-0274 | **Permissions and scope.** Category CRUD endpoints enforce server-side categories.view/add/edit/delete permissions and CSRF; catalog is global master with no BranchId. Persistent audit is future WP46, not claimed here. |
| ERP-0275 | **Category React UI.** Existing keyboard-first form, edit/delete, parent select, sorted tree and client search; now parent option and table parent name use Arabic when selected language is Arabic. |
| ERP-0276 | **Bilingual category UX.** Code and English name LTR, Arabic input RTL; Arabic parent selector and child row use Arabic names. Shared browser tests check Arabic root direction and root ID targeting. |
| ERP-0277 | **ASP.NET tests.** CatalogValidationTests verify normalized category code, blank name rejection; SQL API smoke validates root, child, missing parent, Arabic search, cycle, child/product FK 409. |
| ERP-0278 | **Django negative/integration tests.** CatalogApiTests check bilingual Category search, duplicate siblings, deep cycle rejection, reparent collisions and Product-referenced category/parent deletion as 409. |
| ERP-0279 | **SQL concurrency and shared browser proof.** Disposable SQL Server verifies concurrent same-parent duplicate sibling creation [201,400] plus Product FK protection; Playwright uses shared React against Django and ASP.NET and tests Arabic hierarchy. |
| ERP-0280 | **Category closeout/security review.** Reviewed code duplication, FK/race handling, keyboard/RTL and master-data scope. Product UI/transaction posting WP16+, audit WP46, pagination WP48 and printed reports WP44 remain future-owned. |

## Contract and boundaries

- `GET /api/categories?search=<text>` checks code, English and Arabic names; `GET /api/categories` returns all categories. `GET /api/categories/{id}` returns one numeric-ID record.
- `POST /api/categories`, `PUT /api/categories/{id}`, `DELETE /api/categories/{id}` accept/produce camelCase JSON: code, nameEn, nameAr, parentId, isActive. Creation 201, edit/read 200, deletion 204; bad parent/cycle/duplicate 400, forbidden 403, absent 404, referenced delete 409.
- Code normalized uppercase and restricted to ASCII A-Z/0-9/_/-. Category code unique among siblings; root codes unique among roots; the same code can exist under different parents. `Product.CategoryId` uses a restricted FK; parent chain is checked for cycles before update.
- Global Catalog masters have no branch assignment. Branch-specific stock, invoicing, future persistent audit logs and PDF printing are explicitly owned by later packages.
- Parent labels follow English/Arabic UI language without changing machine codes. Client-side search and hierarchy ordering are implemented; server search is also available. Full pagination belongs WP48. Physical printing belongs WP44.
- Existing EF `CatalogMasters`/Django `catalog.0001_initial` migrations already provide BIGINT/Unicode/filtered unique indexes. No redundant migration created. CI exercised migrations on disposable SQL Server; no production downgrade.
- Tested single-operation cycle/reparent rejection and concurrent duplicate sibling codes. A simultaneous cross-reparent race across independent admin operations was not independently stress-tested; it remains a hardening consideration before high-concurrency production deployment.

## Test sources

`django/apps/catalog/tests.py`, `aspnet-core/tests/smoke_sqlserver.py`,
`aspnet-core/tests/ITRetailERP.Tests/CatalogValidationTests.cs`,
`frontend/e2e/erp.spec.ts`. The existing product API is sufficient to exercise FK linkage; Product Master UI is WP16 and has not been claimed complete.
