# ERP-0008 — ASP.NET entity/configuration/contract review

**Reviewed development HEAD:** `07344224f0358285d9ebaeb816ae2924c766b29a`

## Scope decision

ERP-0008 asks for ASP.NET entities/configuration/contracts for Package 01's ASP.NET feature/code inventory. ERP-0006 established that the Package 01 deliverable—requirement map, scope decisions and 13 acceptance cases—is version-controlled engineering metadata, not runtime ERP data.

**Implementation result: N/A; no ASP.NET runtime entity or API contract is added.** Adding a Requirement/Acceptance EF entity here would contradict the approved data design, duplicate Git-backed traceability and create unnecessary SQL/API state.

## Actual ASP.NET source reviewed

- `Models/ApplicationUser.cs`: ASP.NET Identity user with numeric `long` key.
- `Models/Company.cs`: numeric `long` Company ID and bilingual Company fields.
- `Data/ApplicationDbContext.cs`: `IdentityDbContext<..., long>`, Company DbSet and current indexes.
- `Contracts/LoginRequest.cs`: login validation contract.
- `Contracts/CompanyRequest.cs`: Company form validation contract.
- `Contracts/CompanyResponse.cs`: Company response with numeric `long Id`.
- `Controllers/Api/AuthController.cs` and `CompaniesApiController.cs`: actual consumers of these contracts.
- `ITRetailERP.Web.csproj`: .NET 10, EF Core/Identity/SQL Server dependencies.

## Findings

1. Existing persisted application entity keys follow the numeric-ID rule for the reviewed ASP.NET business/auth entities.
2. Existing Company request/response contracts are real runtime contracts; they are not repurposed for engineering traceability.
3. No Package-01 traceability entity/configuration/contract is missing because its canonical persistence is under `docs/`.
4. Known Company defects remain owned by later implementation gates: DB-005 logo/DB failure consistency, DB-006 pagination, and missing action-level authorization. ERP-0008 does not hide or mark them fixed.
5. DB-001 normalized-email uniqueness and DB-002 framework claim INT IDs remain open; no unsafe identity migration is introduced here.
6. No money/stock/ledger entity exists in this Package-01 scope; DB-003 remains open.

## Change decision

No application source edit is justified. The professional minimal change is to record the N/A implementation decision and evidence rather than create dead entities/contracts.

No migration is generated. No production data is touched. Runtime build/test is not required to prove absence of a new Package-01 runtime contract, but existing application behavior is also **not** newly certified by this review.
