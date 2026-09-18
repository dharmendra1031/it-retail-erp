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
[Route("api/companies")]
public sealed class CompaniesApiController(
    ApplicationDbContext db,
    CompanyLogoStorage logoStorage) : ControllerBase
{
    [HttpGet]
    public async Task<ActionResult<IReadOnlyList<CompanyResponse>>> List()
    {
        var companies = await db.Companies
            .AsNoTracking()
            .OrderBy(x => x.NameEn)
            .ToListAsync();

        return Ok(companies.Select(CompanyResponse.FromEntity));
    }

    [HttpGet("{id:long}")]
    public async Task<ActionResult<CompanyResponse>> Get(long id)
    {
        var company = await db.Companies.AsNoTracking().FirstOrDefaultAsync(x => x.Id == id);
        return company is null ? NotFound() : Ok(CompanyResponse.FromEntity(company));
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<ActionResult<CompanyResponse>> Create([FromForm] CompanyRequest request)
    {
        var logoError = logoStorage.Validate(request.Logo);
        if (logoError is not null)
        {
            return ValidationProblem(new Dictionary<string, string[]>
            {
                [nameof(request.Logo)] = [logoError],
            });
        }

        var company = new Company();
        Apply(company, request);
        company.CreatedAt = DateTime.UtcNow;
        company.UpdatedAt = company.CreatedAt;

        db.Companies.Add(company);
        await db.SaveChangesAsync();

        if (request.Logo is not null)
        {
            company.LogoPath = await logoStorage.SaveAsync(company.Id, request.Logo);
            await db.SaveChangesAsync();
        }

        return CreatedAtAction(nameof(Get), new { id = company.Id }, CompanyResponse.FromEntity(company));
    }

    [HttpPut("{id:long}")]
    [ValidateAntiForgeryToken]
    public async Task<ActionResult<CompanyResponse>> Update(long id, [FromForm] CompanyRequest request)
    {
        var company = await db.Companies.FindAsync(id);
        if (company is null)
        {
            return NotFound();
        }

        var logoError = logoStorage.Validate(request.Logo);
        if (logoError is not null)
        {
            return ValidationProblem(new Dictionary<string, string[]>
            {
                [nameof(request.Logo)] = [logoError],
            });
        }

        Apply(company, request);
        company.UpdatedAt = DateTime.UtcNow;

        var previousLogo = company.LogoPath;
        if (request.Logo is not null)
        {
            company.LogoPath = await logoStorage.SaveAsync(company.Id, request.Logo);
        }

        await db.SaveChangesAsync();

        if (request.Logo is not null && previousLogo != company.LogoPath)
        {
            logoStorage.Delete(previousLogo);
        }

        return Ok(CompanyResponse.FromEntity(company));
    }

    [HttpDelete("{id:long}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Delete(long id)
    {
        var company = await db.Companies.FindAsync(id);
        if (company is null)
        {
            return NotFound();
        }

        var logoPath = company.LogoPath;
        db.Companies.Remove(company);
        await db.SaveChangesAsync();
        logoStorage.Delete(logoPath);

        return NoContent();
    }

    private static void Apply(Company company, CompanyRequest request)
    {
        company.NameEn = request.NameEn.Trim();
        company.NameAr = Clean(request.NameAr);
        company.AddressEn = Clean(request.AddressEn);
        company.AddressAr = Clean(request.AddressAr);
        company.Telephone = Clean(request.Telephone);
        company.Mobile = Clean(request.Mobile);
        company.Email = Clean(request.Email);
        company.Website = Clean(request.Website);
        company.TaxNumber = Clean(request.TaxNumber);
        company.CommercialRegistrationNumber = Clean(request.CommercialRegistrationNumber);
        company.BankDetails = Clean(request.BankDetails);
        company.InvoiceHeader = Clean(request.InvoiceHeader);
        company.InvoiceFooter = Clean(request.InvoiceFooter);
        company.TermsAndConditions = Clean(request.TermsAndConditions);
        company.SocialMedia = Clean(request.SocialMedia);
        company.IsActive = request.IsActive;
    }

    private static string? Clean(string? value) =>
        string.IsNullOrWhiteSpace(value) ? null : value.Trim();
}
