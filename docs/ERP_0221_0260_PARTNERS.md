# ERP-0221–0260 — Customer and Supplier work packages

Reviewed against SRS baseline and actual current code. Specification steps are not proof of deferred transaction modules.

## ERP-0221 — Customer SRS acceptance and owner mapping

SRS §§4,8,9,51,52,57 require Customer code, English/Arabic names/address, mobile, civil ID access controls, type, payment terms, opening balance, credit limit, searchable master and confidential attachments. Actual ledger/receivables belong WP32–WP33/WP43; posted invoice rules not owned by WP12. Current SRS baseline AT-02 spans quotation/print owners and cannot pass in WP12.

**Source evidence:** `docs/SRS_BASELINE.md`, `docs/ERP_REQUIREMENTS_GAP_MATRIX.md`, `django/apps/partners/models.py`, `frontend/src/components/Partners.tsx`. **Verification:** SRS/source mapping only; CI baseline 40056434243. No new runtime acceptance claimed.
