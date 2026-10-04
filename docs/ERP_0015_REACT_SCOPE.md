# ERP-0015 — React scope and downstream ownership review

**Reviewed branch:** `development` @ `1086de3293d8f335a266b9fbfa0cd9677433967c`
**Package:** WP01 — SRS baseline and delivery boundaries
**Decision:** no React source change belongs to WP01. This step verifies the current frontend inventory and records the correct owning packages instead of creating placeholder UI.

## Current React evidence

| Surface | Actual evidence | Status / owner |
|---|---|---|
| Session bootstrap | `frontend/src/App.tsx` calls `getCurrentUser` and renders Login when unauthenticated. | Existing foundation; WP05 owns auth behavior. |
| Login API | `frontend/src/api/auth.ts` uses `/api/auth/me`, `/api/auth/login`, `/api/auth/logout`. | Existing foundation; WP05. |
| Shared API client | `frontend/src/api/client.ts` uses same-origin cookies and `X-CSRF-TOKEN`. | Existing foundation; WP02/WP05. |
| Company UI | `Companies.tsx`, Company form/table and `api/companies.ts` provide current Company CRUD integration. | Partial existing feature; WP10 owns completion, pagination/media/error fixes. |
| Navigation | `AppShell.tsx` currently exposes only Company Master. | Expected current limitation; permission-aware navigation belongs WP07–WP11 and module routes to their feature packages. |
| Business modules | No Product, Customer, Supplier, Purchase, Sales, Inventory, Service or Reports UI is rendered from `App.tsx`. | Correctly remains future work; WP12–WP45. |
| Bilingual/RTL UI | Company inputs include bilingual data in existing code, but no application-wide locale/RTL system is owned by WP01. | WP11 owns localization/RTL; WP44 owns bilingual print/export. |

## User-feedback gaps recorded, not prematurely fixed

- `apiRequest` has a dedicated 401 marker but no shared 403/validation-error model yet; authorization/validation UX must align with WP02/WP06–WP10.
- Company errors are generic (`Unable to load/save/delete company`) and discard backend field-level validation details; WP10 should fix this with backend contract parity.
- Current navigation is static and Company-only; role/permission-aware menu behavior is deferred until WP06–WP09 exist.
- Company list/search is client-side and unpaginated, already tracked as DB/API scalability finding DB-006; WP10/WP48 own the fix.
- No placeholder screens are added for missing modules because their APIs/schema/workflows do not exist yet.

## Downstream frontend ownership

`WP05 Auth → WP06–WP09 Permission-aware access/navigation → WP10 Company → WP11 RTL/localization → WP12–WP20 Masters/config → WP21–WP39 transactions/service → WP40 Dashboard → WP41–WP45 reports/print/search → WP46 audit/security UI → WP49 E2E`

**ERP-0015 result:** complete as source inventory/ownership review. No runtime UI feature is falsely claimed complete, and no speculative React screen was added.
