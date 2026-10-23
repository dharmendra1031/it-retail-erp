# ASP.NET Core backend

ASP.NET Core API implementation of IT Retail ERP.

## Stack

- .NET 10
- ASP.NET Core Controllers
- Entity Framework Core
- ASP.NET Core Identity
- Microsoft SQL Server 2019

## Local configuration

Create the local environment file once:

```powershell
cd aspnet-core
Copy-Item .env.example .env
```

Update `.env` if your SQL Server or bootstrap admin credentials are different.

The local `.env` file is ignored by Git and is loaded automatically by the API. System environment variables take precedence, so production can use server-level environment variables instead of a checked-in file.

## Run locally

```powershell
cd src\ITRetailERP.Web
dotnet restore
dotnet ef database update
dotnet run --urls http://localhost:5000
```

The React frontend communicates through the `/api` contract.


## Verification

```powershell
dotnet restore src/ITRetailERP.Web/ITRetailERP.Web.csproj
dotnet build src/ITRetailERP.Web/ITRetailERP.Web.csproj -c Release
dotnet ef database update --project src/ITRetailERP.Web
```

CI uses a disposable SQL Server to run EF migrations, REST authentication/Role/Company smoke tests and `tests/ITRetailERP.Tests` document-sequence integration tests. The tests require `ConnectionStrings__DefaultConnection` for a test-only database. Never point the test runner at production.

For deployment supply the connection string and bootstrap admin credentials through protected server environment variables; don't use the example password.
