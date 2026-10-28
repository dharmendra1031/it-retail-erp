using System.Security.Cryptography;
using System.Text;
using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Controllers.Api;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using ITRetailERP.Web.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Xunit;

namespace ITRetailERP.Tests;

public sealed class ProductLicenseTests
{
    [Fact]
    public async Task DigitalLicenseIsEncryptedUniqueAndRevocable()
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        Assert.False(string.IsNullOrWhiteSpace(connection), "Disposable SQL Server connection is required.");
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connection).Options;
        await using var db = new ApplicationDbContext(options);
        await using var transaction = await db.Database.BeginTransactionAsync();
        var suffix = Guid.NewGuid().ToString("N")[..8].ToUpperInvariant();
        var category = new Category { Code = $"C-{suffix}", NameEn = "Software" };
        var unit = new Unit { Code = $"U-{suffix}", NameEn = "License" };
        db.Categories.Add(category);
        db.Units.Add(unit);
        await db.SaveChangesAsync();
        var product = new Product
        {
            Sku = $"LIC-{suffix}", NameEn = "Software License",
            CategoryId = category.Id, UnitId = unit.Id, ProductType = "digital",
        };
        db.Products.Add(product);
        await db.SaveChangesAsync();

        var secret = Convert.ToBase64String(RandomNumberGenerator.GetBytes(32));
        var config = new ConfigurationBuilder().AddInMemoryCollection(
            new Dictionary<string, string?> { ["PRODUCT_LICENSE_SECRET"] = secret }).Build();
        var controller = new ProductLicensesApiController(db, new ProductLicenseCrypto(config))
        {
            ControllerContext = new ControllerContext { HttpContext = new DefaultHttpContext() },
        };
        var key = $"AbC-{suffix}-key";
        var request = new ProductLicenseRequest
        {
            ProductId = product.Id, LicenseKey = key, LicenseNumber = $"NUM-{suffix}",
            ActivationDate = new DateOnly(2026, 10, 1),
            ExpiryDate = new DateOnly(2027, 10, 1),
        };
        var created = Assert.IsType<CreatedAtActionResult>(await controller.Create(request));
        var response = Assert.IsType<ProductLicenseResponse>(created.Value);
        Assert.True(response.HasKey);
        Assert.Equal(request.ExpiryDate, response.ExpiryDate);
        Assert.DoesNotContain(key, System.Text.Json.JsonSerializer.Serialize(response));

        db.ChangeTracker.Clear();
        var saved = await db.ProductLicenses.AsNoTracking().SingleAsync(x => x.Id == response.Id);
        var encrypted = Assert.IsType<byte[]>(saved.EncryptedKey);
        Assert.NotNull(saved.KeyFingerprint);
        Assert.DoesNotContain(key, Encoding.UTF8.GetString(encrypted));

        var typeChange = await new ProductsApiController(db).Update(product.Id,
            new ProductRequest
            {
                Sku = product.Sku, NameEn = product.NameEn,
                CategoryId = category.Id, UnitId = unit.Id,
                ProductType = "nonstock", BasePrice = 1.000m,
            });
        Assert.IsType<BadRequestObjectResult>(typeChange);
        Assert.Equal("digital", (await db.Products.AsNoTracking()
            .SingleAsync(x => x.Id == product.Id)).ProductType);
        Assert.IsType<ConflictObjectResult>(await new ProductsApiController(db).Delete(product.Id));
        db.ChangeTracker.Clear();

        var duplicate = Assert.IsType<BadRequestObjectResult>(await controller.Create(
            new ProductLicenseRequest { ProductId = product.Id, LicenseKey = $" {key.ToUpperInvariant()} " }));
        Assert.Equal("Active license key already exists.",
            duplicate.Value?.GetType().GetProperty("detail")?.GetValue(duplicate.Value));
        Assert.Equal(1, await db.ProductLicenses.CountAsync());
        db.ChangeTracker.Clear();

        var reveal = Assert.IsType<OkObjectResult>(await controller.Reveal(response.Id));
        Assert.Equal(key, reveal.Value?.GetType().GetProperty("licenseKey")?.GetValue(reveal.Value));
        Assert.Equal("no-store", controller.Response.Headers.CacheControl.ToString());

        var revoked = Assert.IsType<OkObjectResult>(await controller.Revoke(response.Id));
        Assert.False(Assert.IsType<ProductLicenseResponse>(revoked.Value).IsActive);
        Assert.IsType<CreatedAtActionResult>(await controller.Create(
            new ProductLicenseRequest { ProductId = product.Id, LicenseKey = key }));
        var numberOnly = Assert.IsType<CreatedAtActionResult>(await controller.Create(
            new ProductLicenseRequest { ProductId = product.Id, LicenseNumber = $"NUMBER-{suffix}" }));
        Assert.False(Assert.IsType<ProductLicenseResponse>(numberOnly.Value).HasKey);
        Assert.Equal(3, await db.ProductLicenses.CountAsync());
        await transaction.RollbackAsync();
    }
}
