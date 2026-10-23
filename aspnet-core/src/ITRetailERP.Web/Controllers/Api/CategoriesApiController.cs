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
    public async Task<IActionResult> List()
    {
        return Ok(await db.Categories.AsNoTracking().OrderBy(x => x.Code).ToListAsync());
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
        await db.SaveChangesAsync();
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
        await db.SaveChangesAsync();
        return Ok(category);
    }

    [HttpDelete("{id:long}")]
    [Authorize(Policy = "categories.delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(long id)
    {
        var category = await db.Categories.FindAsync(id);
        if (category is null) return NotFound();
        if (await db.Categories.AnyAsync(x => x.ParentId == id))
            return Conflict(new { detail = "Record is in use." });
        db.Categories.Remove(category);
        await db.SaveChangesAsync();
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
