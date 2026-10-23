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
[Route("api/warehouses")]
public sealed class WarehousesApiController(ApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> List()
    {
        var warehouses = db.Warehouses.AsNoTracking();
        if (!User.IsInRole("Admin"))
        {
            var branch = await AssignedBranch();
            warehouses = warehouses.Where(x => x.BranchId == branch);
        }
        return Ok(await warehouses.OrderBy(x => x.Code).ToListAsync());
    }

    [HttpGet("{id:long}")]
    public async Task<IActionResult> Get(long id)
    {
        var warehouse = await db.Warehouses.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        if (warehouse is null ||
            (!User.IsInRole("Admin") && warehouse.BranchId != await AssignedBranch()))
            return NotFound();
        return Ok(warehouse);
    }

    [HttpPost]
    [Authorize(Roles = "Admin")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(WarehouseRequest request)
    {
        if (!Valid(request) || !await db.Branches.AnyAsync(x => x.Id == request.BranchId))
            return BadRequest(new { detail = "Invalid request." });
        var code = request.Code.Trim().ToUpperInvariant();
        if (await db.Warehouses.AnyAsync(x => x.BranchId == request.BranchId && x.Code == code))
            return BadRequest(new { detail = "Warehouse code already exists." });
        var warehouse = new Warehouse
        {
            BranchId = request.BranchId, Code = code, NameEn = request.NameEn.Trim(),
            NameAr = request.NameAr, IsActive = request.IsActive,
        };
        db.Warehouses.Add(warehouse);
        await db.SaveChangesAsync();
        return CreatedAtAction(nameof(Get), new { id = warehouse.Id }, warehouse);
    }

    [HttpPut("{id:long}")]
    [Authorize(Roles = "Admin")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update(long id, WarehouseRequest request)
    {
        var warehouse = await db.Warehouses.FindAsync(id);
        if (warehouse is null) return NotFound();
        if (!Valid(request) || !await db.Branches.AnyAsync(x => x.Id == request.BranchId))
            return BadRequest(new { detail = "Invalid request." });
        var code = request.Code.Trim().ToUpperInvariant();
        if (await db.Warehouses.AnyAsync(x => x.Id != id && x.BranchId == request.BranchId && x.Code == code))
            return BadRequest(new { detail = "Warehouse code already exists." });
        warehouse.BranchId = request.BranchId;
        warehouse.Code = code;
        warehouse.NameEn = request.NameEn.Trim();
        warehouse.NameAr = request.NameAr;
        warehouse.IsActive = request.IsActive;
        await db.SaveChangesAsync();
        return Ok(warehouse);
    }

    [HttpDelete("{id:long}")]
    [Authorize(Roles = "Admin")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(long id)
    {
        var warehouse = await db.Warehouses.FindAsync(id);
        if (warehouse is null) return NotFound();
        db.Warehouses.Remove(warehouse);
        await db.SaveChangesAsync();
        return NoContent();
    }

    private async Task<long?> AssignedBranch()
    {
        if (!long.TryParse(User.FindFirstValue(ClaimTypes.NameIdentifier), out var id))
            return null;
        return await db.Users.Where(x => x.Id == id).Select(x => x.BranchId).FirstOrDefaultAsync();
    }

    private static bool Valid(WarehouseRequest request) =>
        !string.IsNullOrWhiteSpace(request.Code) && !string.IsNullOrWhiteSpace(request.NameEn);
}
