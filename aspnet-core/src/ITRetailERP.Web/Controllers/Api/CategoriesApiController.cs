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
[Route("api/categories")]
public sealed class CategoriesApiController(ApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    [Authorize(Policy = "categories.view")]
    public async Task<IActionResult> List([FromQuery] string? search)
    {
        var categories = db.Categories.AsNoTracking();
        if (!string.IsNullOrWhiteSpace(search))
        {
            var term = search.Trim();
            categories = categories.Where(x =>
                x.Code.Contains(term) || x.NameEn.Contains(term) || x.NameAr.Contains(term));
        }
        return Ok(await categories.OrderBy(x => x.Code).ToListAsync());
    }

    [HttpGet("{id:long}")]
    [Authorize(Policy = "categories.view")]
    public async Task<IActionResult> Get(long id)
    {
        var category = await db.Categories.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return category is null ? NotFound() : Ok(category);
    }

    [HttpPost]
    [Authorize(Policy = "categories.add")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(CategoryRequest request)
    {
        var code = CatalogValidation.Code(request);
        if (code is null || !await ValidParent(request.ParentId, null))
            return BadRequest(new { detail = "Invalid request." });
        if (await db.Categories.AnyAsync(x => x.ParentId == request.ParentId && x.Code == code))
            return BadRequest(new { detail = "Category code already exists." });
        var category = new Category();
        Apply(category, request, code);
        db.Categories.Add(category);
        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateException error) when (SqlConstraintErrors.IsDuplicate(error))
        {
            return BadRequest(new { detail = "Category code already exists." });
        }
        return CreatedAtAction(nameof(Get), new { id = category.Id }, category);
    }

    [HttpPut("{id:long}")]
    [Authorize(Policy = "categories.edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update(long id, CategoryRequest request)
    {
        var category = await db.Categories.FindAsync(id);
        if (category is null) return NotFound();
        var code = CatalogValidation.Code(request);
        if (code is null || !await ValidParent(request.ParentId, id))
            return BadRequest(new { detail = "Invalid request." });
        if (await db.Categories.AnyAsync(x =>
            x.Id != id && x.ParentId == request.ParentId && x.Code == code))
            return BadRequest(new { detail = "Category code already exists." });
        Apply(category, request, code);
        category.UpdatedAtUtc = DateTime.UtcNow;
        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateException error) when (SqlConstraintErrors.IsDuplicate(error))
        {
            return BadRequest(new { detail = "Category code already exists." });
        }
        return Ok(category);
    }

    [HttpDelete("{id:long}")]
    [Authorize(Policy = "categories.delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(long id)
    {
        var category = await db.Categories.FindAsync(id);
        if (category is null) return NotFound();
        if (await db.Categories.AnyAsync(x => x.ParentId == id)
            || await db.Products.AnyAsync(x => x.CategoryId == id))
            return Conflict(new { detail = "Record is in use." });
        db.Categories.Remove(category);
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

    private async Task<bool> ValidParent(long? parentId, long? selfId)
    {
        var visited = new HashSet<long>();
        while (parentId.HasValue)
        {
            if (parentId <= 0 || parentId == selfId || !visited.Add(parentId.Value))
                return false;
            var category = await db.Categories.AsNoTracking()
                .Where(x => x.Id == parentId).Select(x => new { x.ParentId }).FirstOrDefaultAsync();
            if (category is null) return false;
            parentId = category.ParentId;
        }
        return true;
    }

    private static void Apply(Category category, CategoryRequest request, string code)
    {
        category.Code = code;
        category.NameEn = request.NameEn.Trim();
        category.NameAr = request.NameAr.Trim();
        category.ParentId = request.ParentId;
        category.IsActive = request.IsActive;
    }
}
