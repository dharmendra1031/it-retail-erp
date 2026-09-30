# ERP-0009 — Django model/serializer/configuration review

**Reviewed development HEAD:** `01fea9b21326396810caeacde9ccf17b763420a1`

## Scope decision

Package 01 traceability is version-controlled engineering metadata, not runtime ERP data. Consistent with ERP-0006 and ERP-0008, **no Django model, serializer, viewset or SQL table is added** for requirement/acceptance tracking.

Creating a Django-only Requirement model would break backend parity and duplicate the canonical Git-backed documents.

## Actual Django source reviewed

- `config/settings.py`: SQL Server through `mssql`, `DEFAULT_AUTO_FIELD = django.db.models.BigAutoField`, custom User model and session/CSRF configuration.
- `apps/core/models.py`: abstract timestamp base.
- `apps/accounts/models.py` and initial migration: User, Role and AccessPermission with BigAutoField IDs; permission/role relationships.
- `apps/accounts/api.py`: CSRF, login, me and logout API behavior.
- `apps/companies/models.py` and initial migration: Company with BigAutoField ID, bilingual fields and current indexes.
- `apps/companies/serializers.py`: camelCase Company API mapping and logo validation/storage.
- `apps/companies/api.py`: authenticated ModelViewSet.
- `config/urls.py`: API routing root.

## Findings

1. Reviewed persisted Django application entities use BigAutoField under the numeric-ID policy.
2. Company bilingual strings are represented by Django Unicode strings and SQL Server-backed character fields; live Arabic round-trip remains untested.
3. Role/AccessPermission relationships exist, but CompanyViewSet currently enforces only IsAuthenticated. Granular authorization remains a later gate.
4. Company serializer writes the Company row and logo storage in separate operations. Storage/DB failure consistency remains DB-005 and is not falsely marked fixed here.
5. Company query remains unbounded; DB-006 stays open.
6. No Package-01 money/stock model exists; DB-003 remains open.
7. No Package-01 traceability serializer/model is missing because docs are its approved canonical persistence.

## Implementation result

**N/A with source evidence.** No application code or migration change is justified for ERP-0009. Existing runtime defects remain explicitly tracked rather than being mixed into this metadata step.

No production data is touched. No runtime build, migration or E2E pass is claimed.
