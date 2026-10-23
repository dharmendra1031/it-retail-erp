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
[Route("api/customers")]
public sealed class CustomersApiController(ApplicationDbContext db) : ControllerBase
{
    [HttpGet]
    [Authorize(Policy = "customers.view")]
    public async Task<IActionResult> List()
    {
        var customers = await db.Customers.AsNoTracking().OrderBy(x => x.Code).ToListAsync();
        return Ok(customers.Select(ToResponse));
    }

    [HttpGet("{id:long}")]
    [Authorize(Policy = "customers.view")]
    public async Task<IActionResult> Get(long id)
    {
        var customer = await db.Customers.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return customer is null ? NotFound() : Ok(ToResponse(customer));
    }

    [HttpPost]
    [Authorize(Policy = "customers.add")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(CustomerRequest request)
    {
        if (!Valid(request)) return BadRequest(new { detail = "Invalid request." });
        var code = request.Code.Trim().ToUpperInvariant();
        if (await db.Customers.AnyAsync(x => x.Code == code))
            return BadRequest(new { detail = "Code already exists." });

        var customer = new Customer();
        Apply(customer, request);
        db.Customers.Add(customer);
        await db.SaveChangesAsync();
        return CreatedAtAction(nameof(Get), new { id = customer.Id }, ToResponse(customer));
    }

    [HttpPut("{id:long}")]
    [Authorize(Policy = "customers.edit")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update(long id, CustomerRequest request)
    {
        var customer = await db.Customers.FindAsync(id);
        if (customer is null) return NotFound();
        if (!Valid(request)) return BadRequest(new { detail = "Invalid request." });
        var code = request.Code.Trim().ToUpperInvariant();
        if (await db.Customers.AnyAsync(x => x.Id != id && x.Code == code))
            return BadRequest(new { detail = "Code already exists." });

        Apply(customer, request);
        customer.UpdatedAtUtc = DateTime.UtcNow;
        await db.SaveChangesAsync();
        return Ok(ToResponse(customer));
    }

    [HttpDelete("{id:long}")]
    [Authorize(Policy = "customers.delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(long id)
    {
        var customer = await db.Customers.FindAsync(id);
        if (customer is null) return NotFound();
        if (await db.PartnerDocuments.AnyAsync(x => x.CustomerId == id))
            return Conflict(new { detail = "Protected documents exist." });
        db.Customers.Remove(customer);
        await db.SaveChangesAsync();
        return NoContent();
    }

    [HttpGet("{id:long}/documents")]
    [Authorize(Roles = "Admin")]
    public async Task<IActionResult> Documents(long id)
    {
        if (!await db.Customers.AnyAsync(x => x.Id == id)) return NotFound();
        var documents = await db.PartnerDocuments.AsNoTracking()
            .Where(x => x.CustomerId == id).OrderBy(x => x.Id).ToListAsync();
        return Ok(documents.Select(PartnerDocumentStorage.Describe));
    }

    [HttpPost("{id:long}/documents")]
    [Authorize(Roles = "Admin")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Upload(long id, IFormFile? file)
    {
        if (!await db.Customers.AnyAsync(x => x.Id == id)) return NotFound();
        var bytes = await PartnerDocumentStorage.ReadAsync(file);
        if (bytes is null) return BadRequest(new { detail = "Invalid document." });

        var document = new PartnerDocument
        {
            CustomerId = id,
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
            .FirstOrDefaultAsync(x => x.CustomerId == id && x.Id == documentId);
        return document is null ? NotFound() :
            File(document.Content, document.ContentType, document.FileName);
    }

    private static bool Valid(CustomerRequest request) =>
        PartnerValidation.IsValid(request) &&
        PartnerValidation.Amount(request.CreditLimit) &&
        PartnerValidation.Amount(request.OpeningBalance) &&
        PartnerValidation.OptionalEmail(request.Email) &&
        request.CustomerType is "retail" or "wholesale" or "corporate"
            or "cash" or "credit" or "individual" or "company" or "government" or "other";

    private static void Apply(Customer model, CustomerRequest request)
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
        model.CivilId = request.CivilId.Trim();
        model.CompanyName = request.CompanyName.Trim();
        model.Email = request.Email?.Trim() ?? "";
        model.TaxNumber = request.TaxNumber.Trim();
        model.OpeningBalance = request.OpeningBalance;
        model.CustomerType = request.CustomerType;
        model.PaymentTermsDays = request.PaymentTermsDays;
        model.CreditLimit = request.CreditLimit;
        model.IsActive = request.IsActive;
    }

    private CustomerResponse ToResponse(Customer customer) => new(
        customer.Id, customer.Code, customer.NameEn, customer.NameAr, customer.AddressEn,
        customer.AddressAr, customer.Mobile,
        User.IsInRole("Admin") ? customer.CivilId : null,
        customer.CustomerType, customer.PaymentTermsDays,
        PartnerValidation.Money(customer.CreditLimit), customer.IsActive,
        customer.ContactPerson, customer.Telephone, customer.Remarks, customer.CompanyName,
        customer.Email, customer.TaxNumber, PartnerValidation.Money(customer.OpeningBalance));
}
