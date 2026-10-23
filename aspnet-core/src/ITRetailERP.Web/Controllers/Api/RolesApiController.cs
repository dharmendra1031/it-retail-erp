using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Security;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using ITRetailERP.Web.Security;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Controllers.Api;

[ApiController]
[Authorize(Roles = "Admin")]
[Route("api/roles")]
public sealed class RolesApiController(
    RoleManager<IdentityRole<long>> roleManager,
    ApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> List()
    {
        var roles = await roleManager.Roles.AsNoTracking()
            .OrderBy(x => x.Name)
            .Select(x => new RoleResponse(x.Id, x.Name ?? string.Empty))
            .ToListAsync();

        return Ok(roles);
    }

    [HttpGet("{id:long}")]
    public async Task<IActionResult> Get(long id)
    {
        var role = await roleManager.FindByIdAsync(id.ToString());
        return role is null ? NotFound() : Ok(new RoleResponse(role.Id, role.Name ?? string.Empty));
    }

    [HttpPost]
    [ServiceFilter(typeof(ApiCsrfFilter))]
    public async Task<IActionResult> Create(RoleRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Name))
        {
            return BadRequest(new { detail = "Invalid request." });
        }

        var name = request.Name.Trim();
        if (await roleManager.RoleExistsAsync(name))
        {
            return BadRequest(new { detail = "Role name already exists." });
        }

        var role = new IdentityRole<long>(name);
        var result = await roleManager.CreateAsync(role);
        if (!result.Succeeded)
        {
            return BadRequest(new { detail = "Invalid request." });
        }

        return CreatedAtAction(nameof(Get), new { id = role.Id }, new RoleResponse(role.Id, name));
    }

    [HttpPut("{id:long}")]
    [ServiceFilter(typeof(ApiCsrfFilter))]
    public async Task<IActionResult> Update(long id, RoleRequest request)
    {
        var role = await roleManager.FindByIdAsync(id.ToString());
        if (role is null)
        {
            return NotFound();
        }
        if (string.Equals(role.Name, "Admin", StringComparison.OrdinalIgnoreCase))
        {
            return BadRequest(new { detail = "Admin role cannot be changed." });
        }

        var name = request.Name.Trim();
        var existing = await roleManager.FindByNameAsync(name);
        if (existing is not null && existing.Id != id)
        {
            return BadRequest(new { detail = "Role name already exists." });
        }

        role.Name = name;
        var result = await roleManager.UpdateAsync(role);
        return result.Succeeded
            ? Ok(new RoleResponse(role.Id, name))
            : BadRequest(new { detail = "Invalid request." });
    }

    [HttpGet("{id:long}/permissions")]
    public async Task<IActionResult> GetPermissions(long id)
    {
        var role = await roleManager.FindByIdAsync(id.ToString());
        if (role is null)
        {
            return NotFound();
        }

        var permissions = await db.RoleClaims.AsNoTracking()
            .Where(claim => claim.RoleId == id && claim.ClaimType == "erp.permission")
            .Select(claim => claim.ClaimValue!)
            .OrderBy(code => code)
            .ToListAsync();
        return Ok(new { permissions });
    }

    [HttpPut("{id:long}/permissions")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> SetPermissions(long id, RolePermissionsRequest request)
    {
        var role = await roleManager.FindByIdAsync(id.ToString());
        if (role is null)
        {
            return NotFound();
        }
        if (string.Equals(role.Name, "Admin", StringComparison.OrdinalIgnoreCase))
        {
            return BadRequest(new { detail = "Admin role cannot be changed." });
        }

        var codes = request.Permissions;
        if (codes is null || codes.Any(code => !PermissionCatalog.Codes.Contains(code)))
        {
            return BadRequest(new { detail = "Invalid request." });
        }

        var unique = codes.Distinct(StringComparer.Ordinal).OrderBy(code => code).ToArray();
        await using var transaction = await db.Database.BeginTransactionAsync();
        await db.RoleClaims.Where(claim => claim.RoleId == id && claim.ClaimType == "erp.permission")
            .ExecuteDeleteAsync();
        db.RoleClaims.AddRange(unique.Select(code => new IdentityRoleClaim<long>
        {
            RoleId = id,
            ClaimType = "erp.permission",
            ClaimValue = code,
        }));
        await db.SaveChangesAsync();
        await transaction.CommitAsync();
        return Ok(new { permissions = unique });
    }

    [HttpDelete("{id:long}")]
    [ServiceFilter(typeof(ApiCsrfFilter))]
    public async Task<IActionResult> Delete(long id)
    {
        var role = await roleManager.FindByIdAsync(id.ToString());
        if (role is null)
        {
            return NotFound();
        }
        if (string.Equals(role.Name, "Admin", StringComparison.OrdinalIgnoreCase))
        {
            return BadRequest(new { detail = "Admin role cannot be deleted." });
        }
        if (await db.UserRoles.AnyAsync(x => x.RoleId == id))
        {
            return Conflict(new { detail = "Role is assigned to users." });
        }

        var result = await roleManager.DeleteAsync(role);
        return result.Succeeded ? NoContent() : BadRequest(result.Errors);
    }
}
