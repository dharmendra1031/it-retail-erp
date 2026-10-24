using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using ITRetailERP.Web.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Controllers.Api;

[ApiController]
[Authorize]
[Route("api/suppliers")]
public sealed class SuppliersApiController(ApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    [Authorize(Policy = "suppliers.view")]
    public async Task<IActionResult> List()
    {
        var suppliers = await db.Suppliers.AsNoTracking().OrderBy(x => x.Code).ToListAsync();
        return Ok(suppliers.Select(ToResponse));
    }

    [HttpGet("{id:long}")]
    [Authorize(Policy = "suppliers.view")]
    public async Task<IActionResult> Get(long id)
    {
        var supplier = await db.Suppliers.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return supplier is null ? NotFound() : Ok(ToResponse(supplier));
    }

    [HttpPost]
    [Authorize(Policy = "suppliers.add")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(SupplierRequest request)
    {
        if (!Valid(request)) return BadRequest(new { detail = "Invalid request." });
        var code = request.Code.Trim().ToUpperInvariant();
        if (await db.Suppliers.AnyAsync(x => x.Code == code))
            return BadRequest(new { detail = "Code already exists." });

        var supplier = new Supplier();
        Apply(supplier, request);
        db.Suppliers.Add(supplier);
        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateException error) when (SqlConstraintErrors.IsDuplicate(error))
        {
            return BadRequest(new { detail = "Code already exists." });
        }
        return CreatedAtAction(nameof(Get), new { id = supplier.Id }, ToResponse(supplier));
    }

    [HttpPut("{id:long}")]
    [Authorize(Policy = "suppliers.edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update(long id, SupplierRequest request)
    {
        var supplier = await db.Suppliers.FindAsync(id);
        if (supplier is null) return NotFound();
        if (!Valid(request)) return BadRequest(new { detail = "Invalid request." });
        var code = request.Code.Trim().ToUpperInvariant();
        if (await db.Suppliers.AnyAsync(x => x.Id != id && x.Code == code))
            return BadRequest(new { detail = "Code already exists." });

        Apply(supplier, request);
        supplier.UpdatedAtUtc = DateTime.UtcNow;
        try
        {
            await db.SaveChangesAsync();
        }
        catch (DbUpdateException error) when (SqlConstraintErrors.IsDuplicate(error))
        {
            return BadRequest(new { detail = "Code already exists." });
        }
        return Ok(ToResponse(supplier));
    }

    [HttpDelete("{id:long}")]
    [Authorize(Policy = "suppliers.delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(long id)
    {
        var supplier = await db.Suppliers.FindAsync(id);
        if (supplier is null) return NotFound();
        if (await db.PartnerDocuments.AnyAsync(x => x.SupplierId == id))
            return Conflict(new { detail = "Protected documents exist." });
        db.Suppliers.Remove(supplier);
        await db.SaveChangesAsync();
        return NoContent();
    }

    [HttpGet("{id:long}/documents")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Documents(long id)
    {
        if (!await db.Suppliers.AnyAsync(x => x.Id == id)) return NotFound();
        var documents = await db.PartnerDocuments.AsNoTracking()
            .Where(x => x.SupplierId == id).OrderBy(x => x.Id).ToListAsync();
        return Ok(documents.Select(PartnerDocumentStorage.Describe));
    }

    [HttpPost("{id:long}/documents")]
    [Authorize(Roles = "Admin")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Upload(long id, IFormFile? file)
    {
        if (!await db.Suppliers.AnyAsync(x => x.Id == id)) return NotFound();
        var bytes = await PartnerDocumentStorage.ReadAsync(file);
        if (bytes is null) return BadRequest(new { detail = "Invalid document." });

        var document = new PartnerDocument
        {
            SupplierId = id,
            FileName = PartnerDocumentStorage.SafeName(file!.FileName),
            ContentType = file.ContentType,
            Content = bytes,
        };
        db.PartnerDocuments.Add(document);
        await db.SaveChangesAsync();
        return StatusCode(201, PartnerDocumentStorage.Describe(document));
    }

    [HttpGet("{id:long}/documents/{documentId:long}")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Download(long id, long documentId)
    {
        var document = await db.PartnerDocuments.AsNoTracking()
            .FirstOrDefaultAsync(x => x.SupplierId == id && x.Id == documentId);
        if (document is null) return NotFound();
        Response.Headers["X-Content-Type-Options"] = "nosniff";
        Response.Headers["Cache-Control"] = "no-store";
        return File(document.Content, document.ContentType, document.FileName);
    }

    private static bool Valid(SupplierRequest request) =>
        PartnerValidation.IsValid(request) && PartnerValidation.Amount(request.OpeningBalance)
        && PartnerValidation.Amount(request.CreditLimit)
        && PartnerValidation.OptionalEmail(request.Email);

    private static void Apply(Supplier model, SupplierRequest request)
    {
        model.Code = request.Code.Trim().ToUpperInvariant();
        model.NameEn = request.NameEn.Trim();
        model.NameAr = request.NameAr.Trim();
        model.AddressEn = request.AddressEn.Trim();
        model.AddressAr = request.AddressAr.Trim();
        model.Mobile = request.Mobile.Trim();
        model.ContactPerson = request.ContactPerson.Trim();
        model.Telephone = request.Telephone.Trim();
        model.Remarks = request.Remarks.Trim();
        model.Email = request.Email?.Trim() ?? "";
        model.TaxNumber = request.TaxNumber.Trim();
        model.PaymentTermsDays = request.PaymentTermsDays;
        model.OpeningBalance = request.OpeningBalance;
        model.CreditLimit = request.CreditLimit;
        model.IsActive = request.IsActive;
    }

    private static SupplierResponse ToResponse(Supplier supplier) => new(
        supplier.Id, supplier.Code, supplier.NameEn, supplier.NameAr, supplier.AddressEn,
        supplier.AddressAr, supplier.Mobile, supplier.Email, supplier.TaxNumber,
        supplier.PaymentTermsDays, PartnerValidation.Money(supplier.OpeningBalance),
        supplier.IsActive, supplier.ContactPerson, supplier.Telephone, supplier.Remarks,
        PartnerValidation.Money(supplier.CreditLimit));
}
