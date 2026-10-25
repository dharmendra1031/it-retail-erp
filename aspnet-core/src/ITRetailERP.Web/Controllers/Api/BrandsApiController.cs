using ITRetailERP.Web.Services;
using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Controllers.Api;

[ApiController]
[Authorize]
[Route("api/brands")]
public sealed class BrandsApiController(ApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    [Authorize(Policy = "brands.view")]
    public async Task<IActionResult> List() =>
        Ok(await db.Brands.AsNoTracking().OrderBy(x => x.Code).ToListAsync());

    [HttpGet("{id:long}")]
    [Authorize(Policy = "brands.view")]
    public async Task<IActionResult> Get(long id)
    {
        var row = await db.Brands.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return row is null ? NotFound() : Ok(row);
    }

    [HttpPost]
    [Authorize(Policy = "brands.add")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(NamedCatalogRequest request)
    {
        var code = CatalogValidation.Code(request);
        if (code is null) return BadRequest(new { detail = "Invalid request." });
        if (await db.Brands.AnyAsync(x => x.Code == code))
            return BadRequest(new { detail = "Brand code already exists." });
        var row = new Brand();
        Apply(row, request, code);
        db.Brands.Add(row);
        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateException error) when (SqlConstraintErrors.IsDuplicate(error))
        {
            return BadRequest(new { detail = "Brand code already exists." });
        }
        return CreatedAtAction(nameof(Get), new { id = row.Id }, row);
    }

    [HttpPut("{id:long}")]
    [Authorize(Policy = "brands.edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update(long id, NamedCatalogRequest request)
    {
        var row = await db.Brands.FindAsync(id);
        if (row is null) return NotFound();
        var code = CatalogValidation.Code(request);
        if (code is null) return BadRequest(new { detail = "Invalid request." });
        if (await db.Brands.AnyAsync(x => x.Id != id && x.Code == code))
            return BadRequest(new { detail = "Brand code already exists." });
        Apply(row, request, code);
        row.UpdatedAtUtc = DateTime.UtcNow;
        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateException error) when (SqlConstraintErrors.IsDuplicate(error))
        {
            return BadRequest(new { detail = "Brand code already exists." });
        }
        return Ok(row);
    }

    [HttpDelete("{id:long}")]
    [Authorize(Policy = "brands.delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(long id)
    {
        var row = await db.Brands.FindAsync(id);
        if (row is null) return NotFound();
        if (await db.Products.AnyAsync(x => x.BrandId == id))
            return Conflict(new { detail = "Record is in use." });
        db.Brands.Remove(row);
        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateException error) when (SqlConstraintErrors.IsForeignKeyViolation(error))
        {
            return Conflict(new { detail = "Record is in use." });
        }
        return NoContent();
    }

    private static void Apply(Brand model, NamedCatalogRequest request, string code)
    {
        model.Code = code;
        model.NameEn = request.NameEn.Trim();
        model.NameAr = request.NameAr.Trim();
        model.IsActive = request.IsActive;
    }
}
