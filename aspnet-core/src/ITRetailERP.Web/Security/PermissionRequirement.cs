using System.Security.Claims;
using ITRetailERP.Web.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Security;

public sealed record PermissionRequirement(string Code) : IAuthorizationRequirement;

public sealed class PermissionHandler(ApplicationDbContext db)
    : AuthorizationHandler<PermissionRequirement>
{
    protected override async Task HandleRequirementAsync(
        AuthorizationHandlerContext context, PermissionRequirement requirement)
    {
        if (!long.TryParse(context.User.FindFirstValue(ClaimTypes.NameIdentifier), out var userId))
        {
            return;
        }

        var isAdmin = await (from membership in db.UserRoles
                             join role in db.Roles on membership.RoleId equals role.Id
                             where membership.UserId == userId && role.NormalizedName == "ADMIN"
                             select role.Id).AnyAsync();

        var canAccess = isAdmin || await (from membership in db.UserRoles
                                          join claim in db.RoleClaims on membership.RoleId equals claim.RoleId
                                          where membership.UserId == userId
                                                && claim.ClaimType == "erp.permission"
                                                && claim.ClaimValue == requirement.Code
                                          select claim.Id).AnyAsync();

        if (canAccess)
        {
            context.Succeed(requirement);
        }
    }
}
