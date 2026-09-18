# ASP.NET Core implementation

ASP.NET Core MVC implementation of IT Retail ERP.

## Stack

- .NET 10
- ASP.NET Core MVC
- Entity Framework Core
- ASP.NET Core Identity
- Microsoft SQL Server 2019

## Run locally

```bash
dotnet restore src/ITRetailERP.Web/ITRetailERP.Web.csproj
dotnet run --project src/ITRetailERP.Web/ITRetailERP.Web.csproj
```

Configure `ConnectionStrings:DefaultConnection` through appsettings, user-secrets, environment variables, or deployment configuration.
