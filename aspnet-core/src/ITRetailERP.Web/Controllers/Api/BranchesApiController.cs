using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Security.Claims;

namespace ITRetailERP.Web.Controllers.Api;

[ApiController]
[Authorize]
[Route("api/branches")]
public sealed class BranchesApiController(ApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> List()
    {
        var branches = db.Branches.AsNoTracking();
        if (!User.IsInRole("Admin"))
        {
            var branchId = await AssignedBranch();
            branches = branches.Where(x => x.Id == branchId);
        }
        return Ok(await branches.OrderBy(x => x.Code).ToListAsync());
    }

    [HttpGet("{id:long}")]
    public async Task<IActionResult> Get(long id)
    {
        if (!User.IsInRole("Admin") && await AssignedBranch() != id) return NotFound();
        var branch = await db.Branches.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return branch is null ? NotFound() : Ok(branch);
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(BranchRequest request)
    {
        if (!Valid(request) || !await db.Companies.AnyAsync(x => x.Id == request.CompanyId))
            return BadRequest(new { detail = "Invalid request." });
        var code = request.Code.Trim().ToUpperInvariant();
        if (await db.Branches.AnyAsync(x => x.CompanyId == request.CompanyId && x.Code == code))
            return BadRequest(new { detail = "Branch code already exists." });
        var branch = new Branch
        {
            CompanyId = request.CompanyId, Code = code, NameEn = request.NameEn.Trim(),
            NameAr = request.NameAr, IsActive = request.IsActive,
        };
        db.Branches.Add(branch);
        await db.SaveChangesAsync();
        return CreatedAtAction(nameof(Get), new { id = branch.Id }, branch);
    }

    [HttpPut("{id:long}")]
    [Authorize(Roles = "Admin")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update(long id, BranchRequest request)
    {
        var branch = await db.Branches.FindAsync(id);
        if (branch is null) return NotFound();
        if (!Valid(request) || !await db.Companies.AnyAsync(x => x.Id == request.CompanyId))
            return BadRequest(new { detail = "Invalid request." });
        var code = request.Code.Trim().ToUpperInvariant();
        if (await db.Branches.AnyAsync(x => x.Id != id && x.CompanyId == request.CompanyId && x.Code == code))
            return BadRequest(new { detail = "Branch code already exists." });
        branch.CompanyId = request.CompanyId;
        branch.Code = code;
        branch.NameEn = request.NameEn.Trim();
        branch.NameAr = request.NameAr;
        branch.IsActive = request.IsActive;
        await db.SaveChangesAsync();
        return Ok(branch);
    }

    [HttpDelete("{id:long}")]
    [Authorize(Roles = "Admin")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(long id)
    {
        var branch = await db.Branches.FindAsync(id);
        if (branch is null) return NotFound();
        if (await db.Warehouses.AnyAsync(x => x.BranchId == id)
            || await db.Users.AnyAsync(x => x.BranchId == id))
            return Conflict(new { detail = "Branch is in use." });
        db.Branches.Remove(branch);
        await db.SaveChangesAsync();
        return NoContent();
    }

    private async Task<long?> AssignedBranch()
    {
        if (!long.TryParse(User.FindFirstValue(ClaimTypes.NameIdentifier), out var id))
            return null;
        return await db.Users.Where(x => x.Id == id).Select(x => x.BranchId).FirstOrDefaultAsync();
    }

    private static bool Valid(BranchRequest request) =>
        !string.IsNullOrWhiteSpace(request.Code) && !string.IsNullOrWhiteSpace(request.NameEn);
}
