# ERP-0251 — Supplier API parity and secured document contract

Source review on 2026-10-24: `aspnet-core/src/ITRetailERP.Web/Controllers/Api/SuppliersApiController.cs`, `aspnet-core/src/ITRetailERP.Web/Contracts/PartnerRequests.cs`, `django/apps/partners/api.py`, `django/config/exceptions.py`, `frontend/src/api/partners.ts`.

## Endpoints and methods

| Method | Route | Request | Successful response | Authorization |
|---|---|---|---|---|
| GET | /api/suppliers | none | 200 Supplier[] | authenticated + suppliers.view |
| GET | /api/suppliers/{id} | none | 200 Supplier, 404 if absent | authenticated + suppliers.view |
| POST | /api/suppliers | application/json SupplierValues | 201 Supplier with numeric id | suppliers.add + CSRF |
| PUT | /api/suppliers/{id} | application/json SupplierValues | 200 Supplier; 404 if absent | suppliers.edit + CSRF |
| DELETE | /api/suppliers/{id} | none | 204; 409 if documents exist | suppliers.delete + CSRF |
| GET | /api/suppliers/{id}/documents | none | 200 Document[] | Admin only |
| POST | /api/suppliers/{id}/documents | multipart file | 201 Document | Admin + CSRF |
| GET | /api/suppliers/{id}/documents/{documentId} | none | Binary attachment, 404 if not owned by supplier | Admin only |

Current user-facing response fields: `id` numeric BIGINT identity, `code` uppercase ASCII `[A-Z0-9_-]{1,30}`, `nameEn`, `nameAr`, `addressEn`, `addressAr`, `mobile`, `telephone`, `contactPerson`, `remarks`, `email`, `taxNumber`, `paymentTermsDays`, `openingBalance`, `creditLimit`, `isActive`. Amounts are invariant three-decimal strings e.g. `"135.500"` and `"800.500"`, not JavaScript numeric posting values. Both implementations use numeric BIGINT primary keys and SQL DECIMAL(18,3). Validation requires code and English name, terms between 0 and 365 days, nonnegative representable 3-place amounts; optional email may be blank. Supplier does not require Arabic name or mobile (Customer rules may differ).

Document metadata: `{id, fileName, contentType, size}`. Maximum upload 5 MiB; PDF, PNG, JPG/JPEG with matching MIME/extension and magic prefix only. Forbidden/mismatched uploads return 400 and do not persist file content. Download response has attachment filename, `X-Content-Type-Options: nosniff` and `Cache-Control: no-store`; an unrelated supplier ID cannot download the document. All document operations require Admin, independent of view grants. No public download URL/token is added.

## Error envelope / known parity

* 400 invalid payload: `{"detail":"Invalid request."}` unless a specifically classified error applies.
* 400 duplicate normalized supplier code: `{"detail":"Code already exists."}` in both implementations (Django handling aligned in commit `5b1b8512`; this contract is pending complete CI verification).
* 400 invalid/oversized document: `{"detail":"Invalid document."}`.
* 409 delete supplier that owns documents: `{"detail":"Protected documents exist."}`.
* 401 unauthorized/not logged in; 403 insufficient grants/CSRF; 404 missing resource. Framework HTTP body and auth status details must be verified by cross-backend tests and should not be assumed identical without them.

## Dependency boundaries

Supplier master is create/update metadata and secure-file management, not procurement posting. First purchase link, payable ledger balance, sequence and invoice/statement printing are future WP24–WP27/WP44 capabilities. Existing admin access and permission strings must be checked at API boundaries rather than relying on React visibility. No replacement table, UUID, transaction ledger, PDF printer or production migration belongs in ERP-0251. A duplicate supplier create must return 400 without mutating any existing supplier.

## Verification

Existing CI 40061876358 succeeded on the pre-ERP-0251 source. Django duplicate-code parity regression was added with the backend change, but **no assertion that it passed on the new commit** should be made before its workflow completes. The shared frontend uses `apiRequest` and `languageError` to present translated API errors, and does not use floating-point arithmetic to post financial balances.
