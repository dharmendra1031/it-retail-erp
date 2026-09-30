# ERP-0005 — verification

Reviewed current `development` source for Company authorization and the existing requirement-gap evidence.

1. PASS — SRS permission/security requirement has an owner.
2. PASS — Concrete negative case uses an existing Company endpoint.
3. PASS — ASP.NET evidence confirms authentication-only Company controller authorization.
4. PASS — Django evidence confirms `IsAuthenticated` only on CompanyViewSet.
5. PASS — Django Role/AccessPermission foundations are identified without claiming endpoint enforcement.
6. PASS — Required authenticated denial is defined as 403.
7. PASS — Unauthenticated 401 is separated from authorization denial.
8. PASS — Data non-mutation after denial is required.
9. PASS — Both backend parity is required.
10. PASS — Audit evidence is required at the owning implementation gate.
11. PASS — Current AT-12 remains unverified; no runtime pass is fabricated.
12. PASS — A second missing-evidence example (Product Master) is explicitly owned by WP16.
13. PASS — No schema change is required for this documentation step.
14. PASS — Numeric ID policy remains unchanged.
15. PASS — Existing DB-001–DB-006 remain open.
16. PASS — ERP-0006 is the next plan step after this specification.

**Runtime tests:** not run. **SQL migration:** not run. **E2E:** not run. This step verifies the negative-case specification against source, not the eventual authorization implementation.
