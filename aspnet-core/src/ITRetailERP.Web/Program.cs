using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using ITRetailERP.Web.Services;
using ITRetailERP.Web.Security;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

var envFile = Path.GetFullPath(
    Path.Combine(builder.Environment.ContentRootPath, "..", "..", ".env"));

if (File.Exists(envFile))
{
    DotNetEnv.Env.NoClobber().Load(envFile);
    builder.Configuration.AddEnvironmentVariables();
}

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")
    ?? throw new InvalidOperationException("Connection string 'DefaultConnection' was not found.");

builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(connectionString));

builder.Services
    .AddIdentity<ApplicationUser, IdentityRole<long>>(options =>
    {
        options.User.RequireUniqueEmail = true;
        options.Password.RequiredLength = 8;
        options.Lockout.AllowedForNewUsers = true;
        options.Lockout.MaxFailedAccessAttempts = 5;
        options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
    })
    .AddEntityFrameworkStores<ApplicationDbContext>()
    .AddDefaultTokenProviders();

builder.Services.ConfigureApplicationCookie(options =>
{
    options.ExpireTimeSpan = TimeSpan.FromMinutes(30);
    options.SlidingExpiration = true;
    options.Cookie.HttpOnly = true;
    options.Cookie.SameSite = SameSiteMode.Lax;
    options.Cookie.SecurePolicy = builder.Environment.IsDevelopment()
        ? CookieSecurePolicy.SameAsRequest
        : CookieSecurePolicy.Always;
    options.Events.OnValidatePrincipal = async context =>
    {
        var manager = context.HttpContext.RequestServices.GetRequiredService<UserManager<ApplicationUser>>();
        var user = context.Principal is null ? null : await manager.GetUserAsync(context.Principal);
        if (user is null || !user.IsActive)
        {
            context.RejectPrincipal();
            await context.HttpContext.SignOutAsync(IdentityConstants.ApplicationScheme);
        }
    };
    options.Events.OnRedirectToLogin = context =>
    {
        context.Response.StatusCode = StatusCodes.Status401Unauthorized;
        return Task.CompletedTask;
    };

    options.Events.OnRedirectToAccessDenied = context =>
    {
        context.Response.StatusCode = StatusCodes.Status403Forbidden;
        return Task.CompletedTask;
    };
});

builder.Services.AddAntiforgery(options =>
{
    options.HeaderName = "X-CSRF-TOKEN";
});

builder.Services.AddScoped<CompanyLogoStorage>();
builder.Services.AddScoped<DocumentNumberService>();
builder.Services.AddScoped<ProductLicenseCrypto>();
builder.Services.AddScoped<ApiCsrfFilter>();
builder.Services.AddScoped<IAuthorizationHandler, PermissionHandler>();
builder.Services.AddAuthorization(options =>
{
    foreach (var code in PermissionCatalog.Codes)
    {
        options.AddPolicy(code, policy => policy.RequireAuthenticatedUser()
            .AddRequirements(new PermissionRequirement(code)));
    }
});
builder.Services.AddControllersWithViews();
builder.Services.Configure<ApiBehaviorOptions>(options =>
{
    options.InvalidModelStateResponseFactory = _ =>
        new BadRequestObjectResult(new { detail = "Invalid request." });
});

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

using (var scope = app.Services.CreateScope())
{
    await IdentitySeeder.SeedAsync(scope.ServiceProvider, app.Configuration);
}

app.Run();
