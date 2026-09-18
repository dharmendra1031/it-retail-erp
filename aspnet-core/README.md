# ASP.NET Core backend

ASP.NET Core API implementation of IT Retail ERP.

## Stack

- .NET 10
- ASP.NET Core Controllers
- Entity Framework Core
- ASP.NET Core Identity
- Microsoft SQL Server 2019

## Run locally

1. Configure `ConnectionStrings:DefaultConnection`.
2. Apply EF Core migrations.
3. Optionally set `ERP_ADMIN_EMAIL`, `ERP_ADMIN_PASSWORD`, and `ERP_ADMIN_NAME` to bootstrap the first user.
4. Run `dotnet run --project src/ITRetailERP.Web/ITRetailERP.Web.csproj`.

The React frontend communicates through the `/api` contract.
