using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Data;

public static class IdentitySeeder
{
    public static async Task SeedAsync(IServiceProvider services, IConfiguration configuration)
    {
        var email = configuration["ERP_ADMIN_EMAIL"];
        var password = configuration["ERP_ADMIN_PASSWORD"];
        if (string.IsNullOrWhiteSpace(email) || string.IsNullOrWhiteSpace(password))
        {
            return;
        }

        var db = services.GetRequiredService<ApplicationDbContext>();
        if (!await db.Database.CanConnectAsync())
        {
            return;
        }

        var roleManager = services.GetRequiredService<RoleManager<IdentityRole<long>>>();
        if (!await roleManager.RoleExistsAsync("Admin"))
        {
            var roleResult = await roleManager.CreateAsync(new IdentityRole<long>("Admin"));
            EnsureSuccess(roleResult);
        }

        var userManager = services.GetRequiredService<UserManager<ApplicationUser>>();
        var user = await userManager.FindByEmailAsync(email);
        if (user is null)
        {
            user = new ApplicationUser
            {
                UserName = email,
                Email = email,
                EmailConfirmed = true,
                FullName = configuration["ERP_ADMIN_NAME"] ?? "Administrator",
            };
            EnsureSuccess(await userManager.CreateAsync(user, password));
        }

        if (!await userManager.IsInRoleAsync(user, "Admin"))
        {
            EnsureSuccess(await userManager.AddToRoleAsync(user, "Admin"));
        }
    }

    private static void EnsureSuccess(IdentityResult result)
    {
        if (!result.Succeeded)
        {
            throw new InvalidOperationException(
                string.Join("; ", result.Errors.Select(error => error.Description)));
        }
    }
}
