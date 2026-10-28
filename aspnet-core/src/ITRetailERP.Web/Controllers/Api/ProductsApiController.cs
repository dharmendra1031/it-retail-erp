using System.Globalization;
using System.Text.RegularExpressions;
using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Controllers.Api;

[ApiController]
[Authorize]
[Route("api/products")]
public sealed class ProductsApiController(ApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    [Authorize(Policy = "products.view")]
    public async Task<IActionResult> List([FromQuery] string? search)
    {
        var products = db.Products.AsNoTracking().AsQueryable();
        if (!string.IsNullOrWhiteSpace(search))
        {
            var term = search.Trim();
            products = products.Where(x =>
                x.Sku.Contains(term) ||
                (x.Barcode != null && x.Barcode.Contains(term)) ||
                x.NameEn.Contains(term) ||
                x.NameAr.Contains(term));
        }
        return Ok((await products.OrderBy(x => x.Sku).ToListAsync()).Select(ToResponse));
    }

    [HttpGet("{id:long}")]
    [Authorize(Policy = "products.view")]
    public async Task<IActionResult> Get(long id)
    {
        var product = await db.Products.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return product is null ? NotFound() : Ok(ToResponse(product));
    }

    [HttpPost]
    [Authorize(Policy = "products.add")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(ProductRequest request)
    {
        if (!await Valid(request)) return BadRequest(new { detail = "Invalid request." });
        var sku = request.Sku.Trim().ToUpperInvariant();
        var barcode = Barcode(request.Barcode);
        if (await db.Products.AnyAsync(x => x.Sku == sku ||
            (barcode != null && x.Barcode == barcode)))
            return BadRequest(new { detail = "SKU or barcode already exists." });

        var product = new Product();
        Apply(product, request);
        db.Products.Add(product);
        await db.SaveChangesAsync();
        return CreatedAtAction(nameof(Get), new { id = product.Id }, ToResponse(product));
    }

    [HttpPut("{id:long}")]
    [Authorize(Policy = "products.edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update(long id, ProductRequest request)
    {
        var product = await db.Products.FindAsync(id);
        if (product is null) return NotFound();
        if (!await Valid(request)) return BadRequest(new { detail = "Invalid request." });
        var sku = request.Sku.Trim().ToUpperInvariant();
        var barcode = Barcode(request.Barcode);
        if (await db.Products.AnyAsync(x => x.Id != id &&
            (x.Sku == sku || (barcode != null && x.Barcode == barcode))))
            return BadRequest(new { detail = "SKU or barcode already exists." });
        Apply(product, request);
        product.UpdatedAtUtc = DateTime.UtcNow;
        await db.SaveChangesAsync();
        return Ok(ToResponse(product));
    }

    [HttpDelete("{id:long}")]
    [Authorize(Policy = "products.delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(long id)
    {
        var product = await db.Products.FindAsync(id);
        if (product is null) return NotFound();
        db.Products.Remove(product);
        await db.SaveChangesAsync();
        return NoContent();
    }

    private async Task<bool> Valid(ProductRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Sku) ||
            !Regex.IsMatch(request.Sku.Trim().ToUpperInvariant(), @"\A[A-Z0-9_-]{1,40}\z") ||
            string.IsNullOrWhiteSpace(request.NameEn) ||
            request.ProductType is not ("stock" or "nonstock" or "digital") ||
            (request.ProductType != "stock" &&
                (request.SerialTracked || request.ReorderLevel != 0)) ||
            !Money(request.CostPrice, 3) || !Money(request.BasePrice, 3) ||
            !Money(request.MinPrice, 3) || !Money(request.ReorderLevel, 6) ||
            request.MinPrice > request.BasePrice)
            return false;

        var barcode = Barcode(request.Barcode);
        if (!string.IsNullOrWhiteSpace(request.Barcode) && barcode is null) return false;
        if (!await db.Categories.AnyAsync(x => x.Id == request.CategoryId && x.IsActive) ||
            !await db.Units.AnyAsync(x => x.Id == request.UnitId && x.IsActive) ||
            (request.BrandId.HasValue &&
                !await db.Brands.AnyAsync(x => x.Id == request.BrandId && x.IsActive)))
            return false;
        return true;
    }

    private static bool Money(decimal value, int scale) =>
        value >= 0 && value < 1000000000000000m && decimal.Round(value, scale) == value;

    private static string? Barcode(string? value)
    {
        if (string.IsNullOrWhiteSpace(value)) return null;
        value = value.Trim().ToUpperInvariant();
        return Regex.IsMatch(value, @"\A[A-Z0-9_-]{3,64}\z") ? value : null;
    }

    private static void Apply(Product model, ProductRequest request)
    {
        model.Sku = request.Sku.Trim().ToUpperInvariant();
        model.Barcode = Barcode(request.Barcode);
        model.NameEn = request.NameEn.Trim();
        model.NameAr = request.NameAr.Trim();
        model.DescriptionEn = request.DescriptionEn.Trim();
        model.DescriptionAr = request.DescriptionAr.Trim();
        model.CategoryId = request.CategoryId;
        model.BrandId = request.BrandId;
        model.UnitId = request.UnitId;
        model.ProductType = request.ProductType;
        model.SerialTracked = request.SerialTracked;
        model.CostPrice = request.CostPrice;
        model.BasePrice = request.BasePrice;
        model.MinPrice = request.MinPrice;
        model.ReorderLevel = request.ReorderLevel;
        model.IsActive = request.IsActive;
    }

    private static ProductResponse ToResponse(Product model) => new(
        model.Id, model.Sku, model.Barcode, model.NameEn, model.NameAr,
        model.DescriptionEn, model.DescriptionAr, model.CategoryId, model.BrandId,
        model.UnitId, model.ProductType, model.SerialTracked,
        model.CostPrice.ToString("F3", CultureInfo.InvariantCulture),
        model.BasePrice.ToString("F3", CultureInfo.InvariantCulture),
        model.MinPrice.ToString("F3", CultureInfo.InvariantCulture),
        model.ReorderLevel.ToString("F6", CultureInfo.InvariantCulture), model.IsActive);
}
