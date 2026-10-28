using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Controllers.Api;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace ITRetailERP.Tests;

public sealed class ProductConflictTests
{
    [Theory]
    [InlineData(true)]
    [InlineData(false)]
    public async Task CreateMapsDatabaseUniqueConflictToBadRequest(bool duplicateSku)
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        Assert.False(string.IsNullOrWhiteSpace(connection), "Disposable SQL Server connection is required.");

        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connection)
            .Options;
        await using var db = new ApplicationDbContext(options);
        await using var transaction = await db.Database.BeginTransactionAsync();

        var suffix = Guid.NewGuid().ToString("N")[..8].ToUpperInvariant();
        var category = new Category { Code = $"C-{suffix}", NameEn = "Product conflict category" };
        var unit = new Unit { Code = $"U-{suffix}", NameEn = "Piece" };
        db.Categories.Add(category);
        db.Units.Add(unit);
        await db.SaveChangesAsync();

        var sku = $"P-{suffix}";
        var barcode = $"B-{suffix}";
        db.Products.Add(new Product
        {
            Sku = sku,
            Barcode = barcode,
            NameEn = "Pending first Product",
            CategoryId = category.Id,
            UnitId = unit.Id,
        });

        // The unsaved Product is invisible to the API's database duplicate precheck.
        // SQL Server's unique index must still prevent the second insert.
        var request = new ProductRequest
        {
            Sku = duplicateSku ? sku : $"Q-{suffix}",
            Barcode = duplicateSku ? $"Q-{suffix}" : barcode,
            NameEn = "Second Product",
            CategoryId = category.Id,
            UnitId = unit.Id,
        };

        var controller = new ProductsApiController(db);
        var result = Assert.IsType<BadRequestObjectResult>(await controller.Create(request));
        Assert.Equal(400, result.StatusCode);
        Assert.Equal("SKU or barcode already exists.",
            result.Value?.GetType().GetProperty("detail")?.GetValue(result.Value));
        Assert.Equal(0, await db.Products.CountAsync(x => x.Sku == sku || x.Barcode == barcode));

        await transaction.RollbackAsync();
    }
}
