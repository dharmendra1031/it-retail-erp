using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Data;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
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
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(RoleRequest request)
    {
        var name = request.Name.Trim();
        if (await roleManager.RoleExistsAsync(name))
        {
            return BadRequest(new { detail = "Role name already exists." });
        }

        var role = new IdentityRole<long>(name);
        var result = await roleManager.CreateAsync(role);
        if (!result.Succeeded)
        {
            return BadRequest(result.Errors);
        }

        return CreatedAtAction(nameof(Get), new { id = role.Id }, new RoleResponse(role.Id, name));
    }

    [HttpPut("{id:long}")]
    [ValidateAntiForgeryToken]
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
            : BadRequest(result.Errors);
    }

    [HttpDelete("{id:long}")]
    [ValidateAntiForgeryToken]
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
