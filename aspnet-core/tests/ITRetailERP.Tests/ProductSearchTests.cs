using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Controllers.Api;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace ITRetailERP.Tests;

public sealed class ProductSearchTests
{
    [Fact]
    public async Task ListFindsProductByEnglishNameArabicNameAndBarcode()
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        Assert.False(string.IsNullOrWhiteSpace(connection), "Disposable SQL Server connection is required.");

        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connection)
            .Options;
        await using var db = new ApplicationDbContext(options);
        await using var transaction = await db.Database.BeginTransactionAsync();

        var suffix = Guid.NewGuid().ToString("N")[..8].ToUpperInvariant();
        var category = new Category { Code = $"CAT-{suffix}", NameEn = "Search test category" };
        var unit = new Unit { Code = $"UNIT-{suffix}", NameEn = "Piece" };
        db.Categories.Add(category);
        db.Units.Add(unit);
        await db.SaveChangesAsync();

        var product = new Product
        {
            Sku = $"SKU-{suffix}",
            Barcode = $"BAR-{suffix}",
            NameEn = $"Notebook {suffix}",
            NameAr = $"حاسوب {suffix}",
            DescriptionEn = "Portable computer",
            DescriptionAr = "حاسوب محمول",
            CategoryId = category.Id,
            UnitId = unit.Id,
        };
        db.Products.Add(product);
        await db.SaveChangesAsync();

        var controller = new ProductsApiController(db);
        foreach (var search in new[] { $"Notebook {suffix}", $"حاسوب {suffix}", $"BAR-{suffix}" })
        {
            var result = Assert.IsType<OkObjectResult>(await controller.List(search));
            var rows = Assert.IsAssignableFrom<IEnumerable<ProductResponse>>(result.Value);
            Assert.Contains(rows, row => row.Id == product.Id);
        }

        var paged = Assert.IsType<OkObjectResult>(await controller.List(null, 1, 1));
        using (var json = System.Text.Json.JsonDocument.Parse(
            System.Text.Json.JsonSerializer.Serialize(paged.Value)))
        {
            Assert.Equal(1, json.RootElement.GetProperty("total").GetInt32());
            Assert.Equal(1, json.RootElement.GetProperty("page").GetInt32());
            Assert.Equal(1, json.RootElement.GetProperty("pageSize").GetInt32());
            Assert.Equal(product.Id, json.RootElement.GetProperty("items")[0].GetProperty("Id").GetInt64());
        }
        Assert.IsType<BadRequestObjectResult>(await controller.List(null, 0, 25));

        await transaction.RollbackAsync();
    }
}
