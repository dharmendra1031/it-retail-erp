using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using ITRetailERP.Web.Security;
using ITRetailERP.Web.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Controllers.Api;

[ApiController]
[Authorize]
[Route("api/product-licenses")]
public sealed class ProductLicensesApiController(
    ApplicationDbContext db, ProductLicenseCrypto crypto) : ControllerBase
{
    [HttpGet]
    [Authorize(Policy = "product-licenses.view")]
    public async Task<IActionResult> List([FromQuery] long productId)
    {
        if (productId <= 0) return BadRequest(new { detail = "Invalid request." });
        var rows = await db.ProductLicenses.AsNoTracking()
            .Where(x => x.ProductId == productId)
            .OrderByDescending(x => x.Id).ToListAsync();
        return Ok(rows.Select(ToResponse));
    }

    [HttpPost]
    [Authorize(Policy = "product-licenses.add")]
    [ServiceFilter(typeof(ApiCsrfFilter))]
    public async Task<IActionResult> Create(ProductLicenseRequest request)
    {
        var licenseKey = request.LicenseKey?.Trim();
        var number = request.LicenseNumber?.Trim() ?? "";
        if ((string.IsNullOrEmpty(licenseKey) && number.Length == 0) ||
            (licenseKey is not null && licenseKey.Any(char.IsControl)) ||
            (request.ActivationDate.HasValue && request.ExpiryDate.HasValue &&
             request.ExpiryDate < request.ActivationDate))
            return BadRequest(new { detail = "Invalid request." });

        if (!await db.Products.AnyAsync(x => x.Id == request.ProductId &&
            x.ProductType == "digital" && x.IsActive))
            return BadRequest(new { detail = "Invalid request." });

        var license = new ProductLicense
        {
            ProductId = request.ProductId,
            LicenseNumber = number,
            EncryptedKey = string.IsNullOrEmpty(licenseKey) ? null : crypto.Encrypt(licenseKey),
            KeyFingerprint = string.IsNullOrEmpty(licenseKey) ? null : crypto.Fingerprint(licenseKey),
            ActivationDate = request.ActivationDate,
            ExpiryDate = request.ExpiryDate,
        };
        db.ProductLicenses.Add(license);
        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateException ex) when (ex.InnerException is SqlException { Number: 2601 or 2627 })
        {
            return BadRequest(new { detail = "Active license key already exists." });
        }
        catch (DbUpdateException ex) when (ex.InnerException is SqlException { Number: 547 })
        {
            return BadRequest(new { detail = "Invalid request." });
        }
        return CreatedAtAction(nameof(Get), new { id = license.Id }, ToResponse(license));
    }

    [HttpGet("{id:long}")]
    [Authorize(Policy = "product-licenses.view")]
    public async Task<IActionResult> Get(long id)
    {
        var license = await db.ProductLicenses.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == id);
        return license is null ? NotFound() : Ok(ToResponse(license));
    }

    [HttpGet("{id:long}/reveal")]
    [Authorize(Policy = "product-licenses.reveal")]
    public async Task<IActionResult> Reveal(long id)
    {
        Response.Headers.CacheControl = "no-store";
        var license = await db.ProductLicenses.AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == id);
        if (license is null) return NotFound();
        return Ok(new { licenseKey = license.EncryptedKey is null
            ? null : crypto.Decrypt(license.EncryptedKey) });
    }

    [HttpDelete("{id:long}")]
    [Authorize(Policy = "product-licenses.revoke")]
    [ServiceFilter(typeof(ApiCsrfFilter))]
    public async Task<IActionResult> Revoke(long id)
    {
        var license = await db.ProductLicenses.FindAsync(id);
        if (license is null) return NotFound();
        if (!license.IsActive) return Ok(ToResponse(license));
        license.IsActive = false;
        license.UpdatedAtUtc = DateTime.UtcNow;
        await db.SaveChangesAsync();
        return Ok(ToResponse(license));
    }

    private static ProductLicenseResponse ToResponse(ProductLicense license) => new(
        license.Id, license.ProductId, license.LicenseNumber,
        license.EncryptedKey is not null, license.ActivationDate,
        license.ExpiryDate, license.IsActive);
}
