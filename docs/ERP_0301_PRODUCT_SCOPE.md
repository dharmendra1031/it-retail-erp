# ERP-0301 — Product / Item Master requirements

**Source:** [IT Retail SRS v1.0](https://docs.google.com/document/d/1Gb_pMJAN14UY0scLJjGBGiuRZdlXOWJARB1aLkzIobc/edit?usp=sharing), §§4, 12, 13, 14, 42, 43.
**Plan:** WP16 / ERP-0301–0320. **Reviewed code:** `f2296dd1`.
This is a requirements and ownership baseline, not Product Master delivery or runtime acceptance.

## Field requirements and current mapping

| SRS field / behavior | Existing source | Decision or next owner |
| --- | --- | --- |
| Item ID | Both Product models use numeric auto-increment BIGINT | Retain; never add UUID |
| Item Code and SKU | Both Product models have unique `sku`; no separate item code | Clarify whether distinct identifiers are required before schema/contract changes (WP16) |
| Barcode | Optional unique barcode in both models | Unique normalized value; scan-to-cart/labels in WP31/WP45 |
| Product name and description (EN/AR) | Separate Unicode fields in both models | Preserve both languages and round-trip tests (WP16) |
| Category and subcategory | Required Category FK; hierarchical Category already supports parent | Decide leaf/subcategory selection rule; retain valid active category (WP16) |
| Brand | Optional Brand FK | Confirm whether Brand is mandatory for selected products (WP16) |
| Model | No Product model field | Evaluate additive field/schema contract (WP16) |
| Unit | Required Unit FK | Active unit, valid fractional precision per existing Unit Master (WP16) |
| Product type | `stock`, `nonstock`, `digital` present | Type-specific stock, service and license behavior in WP17/21 |
| Purchase price and cost price | `costPrice` present; distinct purchase price absent | Confirm whether separate purchase-cost fields are needed (WP16/WP24/WP37) |
| Selling, wholesale and minimum selling price | `basePrice` and `minPrice` present; wholesale missing | Confirm `basePrice` as standard selling price; price lists/wholesale in WP20 |
| Tax category and tax percentage | No Product tax fields | Configurable tax configuration/calculation in WP18, never hard-code a rate |
| Reorder level | Existing `reorderLevel` | Nonnegative quantity; low-stock dashboard in WP40 |
| Opening and current stock | Neither is stored as an editable Product column | Initial stock and stock ledger/posting in WP21/WP25; no invented quantity mutations |
| Warranty period | Not in Product model | Product/serial warranty rules in WP22/WP23 |
| Active/inactive | `isActive` present | Inactive items must not be offered for new transactions; verify downstream posting rules |
| Product find/search | Current `/api/products?search=` matches SKU only | Product name/item code/barcode search in WP16; cross-module/global/serial search in WP45 |

## WP16 acceptance contract

- **Create:** Authorized user can create a stock product with English/Arabic names and descriptions, unique SKU and barcode, active category/unit, optional brand (until policy is confirmed), nonnegative three-decimal prices, six-decimal reorder level and status; both APIs return the same payload including numeric ID.
- **Reject:** Duplicate normalized SKU or barcode, unsupported identifier format, negative or overprecision price, minimum price greater than selling price, invalid/inactive category or unit, and mismatched type-specific settings. Failed writes must leave no Product row.
- **Read/edit/search:** List/detail/update must preserve bilingual Unicode; master search will cover SRS product name, identifiers and barcode; UI must be keyboard-first, responsive and EN/AR (including RTL).
- **Authorization:** `products.view/add/edit/delete` is server-enforced on both backends. Inactive/related-record delete behavior and concurrent duplicate handling require executable regression tests before WP16 closeout.

Existing API routes are `/api/products` and `/api/products/{id}` in both implementations. This contract does not claim their complete acceptance yet.

## Assumptions requiring confirmation

1. Is **Item Code** separate from **SKU**, or an alternative name for the same business identifier? Database ID remains separate either way.
2. Must a saleable product always be assigned to a **leaf subcategory**? Can brand be omitted for services or unbranded items?
3. Are **Purchase Price** and **Cost Price** distinct values (e.g. supplier price vs landed cost)? Is `basePrice` the SRS standard retail selling price?
4. Does **Warranty Period** belong to the Product default, the serial, or a sales-invoice warranty record? Ownership is WP23.
5. Does `openingStock` represent an opening-stock movement, rather than a directly editable current balance? Preserve stock-ledger integrity in WP21/WP25.
6. Tax rates and KWD rounding require accountant-approved configuration in WP18. No Kuwait tax rate is assumed.

These unanswered business rules are recorded, not guessed into database fields or pricing.

## Exclusions and dependencies

WP16 owns Product Master schema/API/UI, validation and search. WP17 owns stock/non-stock/digital transaction distinctions and license metadata; WP18 tax; WP20 multi-price lists; WP21/WP25 quantities and purchase posting; WP22/WP23 serial/warranty; WP31 barcode sale interaction; WP40 low-stock dashboard; WP44 printing; WP45 global search; WP46 persistent audit; WP48 broad pagination/performance; WP49 final system acceptance. SRS AT-01 (Product → Purchase → Stock Increase) remains pending the downstream posting modules.

## Source evidence and verification

Reviewed:
- `aspnet-core/src/ITRetailERP.Web/Models/Product.cs`, `Contracts/ProductRequest.cs`, `Controllers/Api/ProductsApiController.cs`, `Migrations/20261023140000_Products.cs`
- `django/apps/catalog/models.py`, `api.py`, `migrations/0002_product.py`, `tests.py`
- `frontend/src/api/catalog.ts`, `components/Catalog.tsx`, `aspnet-core/tests/ITRetailERP.Tests/CatalogValidationTests.cs`
- `docs/SRS_BASELINE.md` and `docs/ERP_PLAN_1000_STEPS.md`

**Result:** Requirements extracted and existing-vs-required fields traced to owners; no source code, database migration, UI or API changed. ERP-0301 is documentation-only; no new build, migration or E2E test was executed for this step. Existing baseline CI [40171067175](https://github.com/dharmendra1031/it-retail-erp/actions/runs/40171067175) passed 5/5 before this documentation update; it does not verify later WP16 features. The next step, ERP-0302, is detailed source inventory.
