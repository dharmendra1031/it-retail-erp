# ERP-0011 — current ASP.NET/Django API contract comparison

**Reviewed development HEAD:** `6aa3b1190a454627c9bf5184968322a7121f561f`

Package 01 traceability itself has no runtime API. To satisfy the inventory/parity gate, this review documents the actual shared API surface currently consumed by React and records divergences rather than inventing endpoints.

| Path | Method | ASP.NET | Django | Current shared shape |
|---|---|---|---|---|
| /api/auth/csrf | GET | anonymous | anonymous | { csrfToken: string } |
| /api/auth/me | GET | authorized | IsAuthenticated | { id:number, name:string, email:string } |
| /api/auth/login | POST JSON | anonymous + antiforgery | AllowAny + csrf_protect | email, password, rememberMe -> current user; bad credentials 401 |
| /api/auth/logout | POST | authorized + antiforgery | IsAuthenticated + csrf_protect | 204 |
| /api/companies | GET | authorized | IsAuthenticated | unpaginated Company[] |
| /api/companies/{id} | GET | authorized | IsAuthenticated | Company or 404 |
| /api/companies | POST multipart | authorized + antiforgery | IsAuthenticated + session CSRF | Company; validation errors differ by framework |
| /api/companies/{id} | PUT multipart | authorized + antiforgery | IsAuthenticated + session CSRF | Company or 404 |
| /api/companies/{id} | DELETE | authorized + antiforgery | IsAuthenticated + session CSRF | 204 or 404 |

## Company response fields

Both implementations expose the React-facing camelCase fields: `id, nameEn, nameAr, addressEn, addressAr, telephone, mobile, email, website, taxNumber, commercialRegistrationNumber, logoUrl, bankDetails, invoiceHeader, invoiceFooter, termsAndConditions, socialMedia, isActive`.

IDs are numeric. Company writes are multipart because of optional logo.

## Known contract divergences / unverified behavior

1. Validation error payloads are framework-native and are not proven identical.
2. ASP.NET Company request uses DataAnnotations; Django serializer validation differs in default blank/null/error formatting.
3. Granular action permissions are absent; both currently enforce authentication only.
4. Company list is unpaginated in both implementations (DB-006).
5. Logo failure semantics are not equivalent/atomic (DB-005).
6. CSRF header/cookie behavior is intended to be shared through the frontend client but has not been E2E-tested against both backends in this step.
7. No Package-01 traceability endpoint is required because its persistence is version-controlled docs.

## Contract rule

Do not call the backends interchangeable until parity tests prove status codes, validation/error bodies, CSRF behavior and Company media behavior. Later operation/parity/test steps own those fixes. This documentation does not turn observed similarity into a passing runtime acceptance result.
