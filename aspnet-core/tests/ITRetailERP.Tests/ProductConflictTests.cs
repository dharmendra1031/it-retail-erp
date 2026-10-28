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
    public async Task SimultaneousCreatesPersistExactlyOneProduct(bool duplicateSku)
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        Assert.False(string.IsNullOrWhiteSpace(connection), "Disposable SQL Server connection is required.");

        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connection).Options;
        var suffix = Guid.NewGuid().ToString("N")[..8].ToUpperInvariant();
        var category = new Category { Code = $"C-{suffix}", NameEn = "Concurrent Product category" };
        var unit = new Unit { Code = $"U-{suffix}", NameEn = "Piece" };
        await using (var setup = new ApplicationDbContext(options))
        {
            setup.Categories.Add(category);
            setup.Units.Add(unit);
            await setup.SaveChangesAsync();
        }

        var sku = $"P-{suffix}";
        var barcode = $"B-{suffix}";
        using var start = new ManualResetEventSlim();
        try
        {
            async Task<IActionResult> Create(int attempt)
            {
                await Task.Run(() => start.Wait());
                await using var db = new ApplicationDbContext(options);
                return await new ProductsApiController(db).Create(new ProductRequest
                {
                    Sku = duplicateSku ? sku : $"{attempt}-{sku}",
                    Barcode = duplicateSku ? $"{attempt}-{barcode}" : barcode,
                    NameEn = $"Concurrent Product {attempt}",
                    CategoryId = category.Id,
                    UnitId = unit.Id,
                    CostPrice = 1.000m,
                    BasePrice = 2.000m,
                    MinPrice = 1.000m,
                });
            }

            var first = Create(1);
            var second = Create(2);
            start.Set();
            var results = await Task.WhenAll(first, second);
            Assert.Single(results.OfType<CreatedAtActionResult>());
            var rejection = Assert.Single(results.OfType<BadRequestObjectResult>());
            Assert.Equal("SKU or barcode already exists.",
                rejection.Value?.GetType().GetProperty("detail")?.GetValue(rejection.Value));

            await using var check = new ApplicationDbContext(options);
            Assert.Equal(1, await check.Products.CountAsync(x =>
                duplicateSku ? x.Sku == sku : x.Barcode == barcode));
        }
        finally
        {
            await using var cleanup = new ApplicationDbContext(options);
            await cleanup.Products.Where(x => x.CategoryId == category.Id).ExecuteDeleteAsync();
            await cleanup.Categories.Where(x => x.Id == category.Id).ExecuteDeleteAsync();
            await cleanup.Units.Where(x => x.Id == unit.Id).ExecuteDeleteAsync();
        }
    }

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
