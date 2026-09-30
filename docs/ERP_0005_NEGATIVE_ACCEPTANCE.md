# ERP-0005 — negative and authorization acceptance specification

**SRS trace:** §7 User Permissions; §59 Security Requirements; §65 minimum acceptance criterion “Unauthorized restricted action denied”. **Plan:** Package 01, ERP-0005. **Status:** negative acceptance specification; current source does not satisfy granular Company authorization.

## NEG-01: authenticated user without Company.Delete must be denied

### Requirement
Permissions are configurable by user/role and include View, Add, Edit, Delete, Print, Export, Approve, Cancel, Post and Reverse. Authentication alone must not grant a restricted action.

### Current source evidence
- ASP.NET `CompaniesApiController` has controller-level `[Authorize]`, but `DELETE /api/companies/{id}` has no Company Delete policy/role check. `Program.cs` registers authentication/authorization middleware but no Company action policy.
- Django `CompanyViewSet` uses only `permission_classes = [IsAuthenticated]`; its inherited destroy action has no ERP Company Delete permission check.
- Django defines `Role` and `AccessPermission` models, but the Company endpoint does not consume them.
- The existing requirements matrix records this as GAP-001/GAP-007 and AT-12 remains pending.

### Test setup
Use disposable SQL Server test databases only. Create two numeric-ID users: an administrator allowed to manage Company and an authenticated restricted user whose assigned role deliberately lacks `Company.Delete`. Create a Company fixture with a numeric auto-increment ID.

### Expected negative test
1. Login as the restricted user through each backend's normal auth flow and obtain required CSRF state.
2. Send `DELETE /api/companies/{id}`.
3. Expect **403 Forbidden** for the authenticated-but-not-authorized user.
4. Verify the Company row still exists and its data is unchanged.
5. Verify a denied-action audit event once audit logging is implemented.
6. Run the equivalent request against ASP.NET and Django and require the same business result/status contract.
7. Separately verify an unauthenticated request returns **401 Unauthorized**; this does not substitute for the 403 permission test.

### Current result
**FAIL BY SOURCE INSPECTION / NOT RUNTIME-EXECUTED.** Both Company APIs currently gate only on authentication, so there is no source evidence that an authenticated restricted user would receive the required action-level denial. Do not mark AT-12 passed.

### Ownership and exit gate
Implementation ownership is WP06–WP10 and WP46. Define the shared permission codes/policies, assign them through Role/User management, enforce them server-side on View/Add/Edit/Delete, add immutable audit evidence for sensitive mutations, then run ASP.NET + Django integration tests and React behavior tests. ERP-0005 only identifies and specifies the missing-evidence case; it does not prematurely implement later-package authorization.

## NEG-02: requirement with missing implementation evidence

SRS §12 Product / Item Master is owned by WP16, but the reviewed source inventory contains no Product entity/API/screen/migration. Therefore its implementation evidence is explicitly **missing**, rather than inferred or fabricated. It remains ABSENT until WP16 provides source, database and test evidence.

## Database impact
None. This specification introduces no entity, migration, FK, index or production-data change. Existing DB-001–DB-006 remain open. Numeric auto-increment ID policy is unchanged.
