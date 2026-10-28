using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Controllers.Api;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace ITRetailERP.Tests;

public sealed class ProductCreationTests
{
    [Fact]
    public async Task DatabaseRejectsInventorySettingsOnNonstockProduct()
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        Assert.False(string.IsNullOrWhiteSpace(connection), "Disposable SQL Server connection is required.");

        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connection).Options;
        await using var db = new ApplicationDbContext(options);
        await using var transaction = await db.Database.BeginTransactionAsync();
        var suffix = Guid.NewGuid().ToString("N")[..8].ToUpperInvariant();
        var category = new Category { Code = $"C-{suffix}", NameEn = "Type category" };
        var unit = new Unit { Code = $"U-{suffix}", NameEn = "Piece" };
        db.Categories.Add(category);
        db.Units.Add(unit);
        await db.SaveChangesAsync();

        db.Products.Add(new Product
        {
            Sku = $"P-{suffix}", NameEn = "Service", CategoryId = category.Id,
            UnitId = unit.Id, ProductType = "nonstock", ReorderLevel = 1m,
        });
        await Assert.ThrowsAsync<DbUpdateException>(() => db.SaveChangesAsync());
        db.ChangeTracker.Clear();
        Assert.False(await db.Products.AsNoTracking().AnyAsync(x => x.Sku == $"P-{suffix}"));
        await transaction.RollbackAsync();
    }

    [Theory]
    [InlineData("nonstock")]
    [InlineData("digital")]
    public async Task NonstockAndDigitalProductsHaveNoInventorySettings(string productType)
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        Assert.False(string.IsNullOrWhiteSpace(connection), "Disposable SQL Server connection is required.");

        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connection).Options;
        await using var db = new ApplicationDbContext(options);
        await using var transaction = await db.Database.BeginTransactionAsync();
        var suffix = Guid.NewGuid().ToString("N")[..8].ToUpperInvariant();
        var category = new Category { Code = $"C-{suffix}", NameEn = "Type category" };
        var unit = new Unit { Code = $"U-{suffix}", NameEn = "Piece" };
        db.Categories.Add(category);
        db.Units.Add(unit);
        await db.SaveChangesAsync();

        var response = Assert.IsType<CreatedAtActionResult>(await new ProductsApiController(db)
            .Create(new ProductRequest
            {
                Sku = $"P-{suffix}", NameEn = "Service or license",
                CategoryId = category.Id, UnitId = unit.Id, ProductType = productType,
                CostPrice = 1.000m, BasePrice = 2.000m,
            }));
        var created = Assert.IsType<ProductResponse>(response.Value);
        Assert.Equal(productType, created.ProductType);
        Assert.False(created.SerialTracked);
        Assert.Equal("0.000000", created.ReorderLevel);

        db.ChangeTracker.Clear();
        var saved = await db.Products.AsNoTracking().SingleAsync(x => x.Id == created.Id);
        Assert.Equal(productType, saved.ProductType);
        Assert.False(saved.SerialTracked);
        Assert.Equal(0m, saved.ReorderLevel);
        await transaction.RollbackAsync();
    }

    [Fact]
    public async Task StockProductPreservesBilingualFieldsAndExactMoneyOnCreateAndUpdate()
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        Assert.False(string.IsNullOrWhiteSpace(connection), "Disposable SQL Server connection is required.");

        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connection).Options;
        await using var db = new ApplicationDbContext(options);
        await using var transaction = await db.Database.BeginTransactionAsync();

        var suffix = Guid.NewGuid().ToString("N")[..8].ToUpperInvariant();
        var category = new Category { Code = $"CAT-{suffix}", NameEn = "Notebooks", NameAr = "أجهزة الحاسوب" };
        var unit = new Unit { Code = $"PCS-{suffix}", NameEn = "Piece", NameAr = "قطعة" };
        var brand = new Brand { Code = $"BR-{suffix}", NameEn = "Brand", NameAr = "علامة" };
        db.Categories.Add(category);
        db.Units.Add(unit);
        db.Brands.Add(brand);
        await db.SaveChangesAsync();

        var controller = new ProductsApiController(db);
        var request = new ProductRequest
        {
            Sku = $"laptop-{suffix.ToLowerInvariant()}",
            Barcode = $"abc-{suffix.ToLowerInvariant()}",
            NameEn = "Arabic Notebook",
            NameAr = "حاسوب مُتنقّل",
            DescriptionEn = "Laptop with multilingual notes",
            DescriptionAr = "حاسوب تجريبي بذاكرة كبيرة",
            CategoryId = category.Id,
            BrandId = brand.Id,
            UnitId = unit.Id,
            ProductType = "stock",
            SerialTracked = true,
            CostPrice = 123.456m,
            BasePrice = 150.500m,
            MinPrice = 120.125m,
            ReorderLevel = 4.123456m,
        };

        var created = Assert.IsType<CreatedAtActionResult>(await controller.Create(request));
        var response = Assert.IsType<ProductResponse>(created.Value);
        Assert.True(response.Id > 0);
        Assert.Equal(request.Sku.ToUpperInvariant(), response.Sku);
        Assert.Equal(request.Barcode!.ToUpperInvariant(), response.Barcode);
        Assert.Equal(request.NameAr, response.NameAr);
        Assert.Equal(request.DescriptionAr, response.DescriptionAr);
        Assert.Equal("123.456", response.CostPrice);
        Assert.Equal("150.500", response.BasePrice);
        Assert.Equal("120.125", response.MinPrice);
        Assert.Equal("4.123456", response.ReorderLevel);

        db.ChangeTracker.Clear();
        var saved = await db.Products.AsNoTracking().SingleAsync(x => x.Id == response.Id);
        Assert.Equal(request.NameAr, saved.NameAr);
        Assert.Equal(request.DescriptionAr, saved.DescriptionAr);
        Assert.Equal(request.CostPrice, saved.CostPrice);
        Assert.Equal(request.ReorderLevel, saved.ReorderLevel);

        request.DescriptionAr = "تفاصيل مُحدّثة";
        request.NameEn = "Arabic Notebook Updated";
        var updated = Assert.IsType<OkObjectResult>(await controller.Update(response.Id, request));
        var changed = Assert.IsType<ProductResponse>(updated.Value);
        Assert.Equal(request.DescriptionAr, changed.DescriptionAr);
        Assert.Equal(request.NameEn, changed.NameEn);
        Assert.Equal("123.456", changed.CostPrice);

        db.ChangeTracker.Clear();
        saved = await db.Products.AsNoTracking().SingleAsync(x => x.Id == response.Id);
        Assert.Equal("تفاصيل مُحدّثة", saved.DescriptionAr);
        Assert.Equal("Arabic Notebook Updated", saved.NameEn);
        Assert.Equal(4.123456m, saved.ReorderLevel);
        await transaction.RollbackAsync();
    }

    [Fact]
    public async Task InvalidPriceOrMissingActiveCategoryCannotCreateProduct()
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        Assert.False(string.IsNullOrWhiteSpace(connection), "Disposable SQL Server connection is required.");

        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connection).Options;
        await using var db = new ApplicationDbContext(options);
        await using var transaction = await db.Database.BeginTransactionAsync();

        var suffix = Guid.NewGuid().ToString("N")[..8].ToUpperInvariant();
        var category = new Category { Code = $"CAT-{suffix}", NameEn = "Test Category", IsActive = false };
        var unit = new Unit { Code = $"UNIT-{suffix}", NameEn = "Piece" };
        db.Categories.Add(category);
        db.Units.Add(unit);
        await db.SaveChangesAsync();

        var request = new ProductRequest
        {
            Sku = $"BAD-{suffix}",
            NameEn = "Invalid Product",
            CategoryId = category.Id,
            UnitId = unit.Id,
            CostPrice = 1m,
            BasePrice = 5m,
            MinPrice = 2m,
        };
        var controller = new ProductsApiController(db);
        Assert.IsType<BadRequestObjectResult>(await controller.Create(request));

        request.CategoryId = 999999999;
        Assert.IsType<BadRequestObjectResult>(await controller.Create(request));
        request.CategoryId = category.Id;
        category.IsActive = true;
        await db.SaveChangesAsync();

        request.MinPrice = 6m;
        Assert.IsType<BadRequestObjectResult>(await controller.Create(request));
        request.MinPrice = 2m;
        request.CostPrice = 1.1234m;
        Assert.IsType<BadRequestObjectResult>(await controller.Create(request));
        request.CostPrice = 1m;
        request.UnitId = 999999999;
        Assert.IsType<BadRequestObjectResult>(await controller.Create(request));
        request.UnitId = unit.Id;
        request.BasePrice = -1m;
        Assert.IsType<BadRequestObjectResult>(await controller.Create(request));
        request.BasePrice = 5m;
        request.ProductType = "nonstock";
        request.SerialTracked = true;
        Assert.IsType<BadRequestObjectResult>(await controller.Create(request));
        request.SerialTracked = false;
        request.ReorderLevel = 1m;
        Assert.IsType<BadRequestObjectResult>(await controller.Create(request));
        Assert.False(await db.Products.AsNoTracking().AnyAsync(x => x.Sku == request.Sku));
        await transaction.RollbackAsync();
    }
}
