using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using ITRetailERP.Web.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using ITRetailERP.Web.Security;
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
    [Authorize(Policy = "companies.add")]
    [ServiceFilter(typeof(ApiCsrfFilter))]
    public async Task<ActionResult<CompanyResponse>> Create([FromForm] CompanyRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.NameEn) || !ValidateLogo(request.Logo))
        {
            return BadRequest(new { detail = "Invalid request." });
        }

        var company = new Company();
        Apply(company, request);
        company.CreatedAt = DateTime.UtcNow;
        company.UpdatedAt = company.CreatedAt;

        string? newLogo = null;
        await using var transaction = await db.Database.BeginTransactionAsync();
        try
        {
            db.Companies.Add(company);
            await db.SaveChangesAsync();
            if (request.Logo is not null)
            {
                newLogo = await logoStorage.SaveAsync(company.Id, request.Logo);
                company.LogoPath = newLogo;
                await db.SaveChangesAsync();
            }
            await transaction.CommitAsync();
        }
        catch
        {
            logoStorage.Delete(newLogo);
            throw;
        }

        return CreatedAtAction(nameof(Get), new { id = company.Id }, CompanyResponse.FromEntity(company));
    }

    [HttpPut("{id:long}")]
    [Authorize(Policy = "companies.edit")]
    [ServiceFilter(typeof(ApiCsrfFilter))]
    public async Task<ActionResult<CompanyResponse>> Update(long id, [FromForm] CompanyRequest request)
    {
        var company = await db.Companies.FindAsync(id);
        if (company is null)
        {
            return NotFound();
        }

        if (string.IsNullOrWhiteSpace(request.NameEn) || !ValidateLogo(request.Logo))
        {
            return BadRequest(new { detail = "Invalid request." });
        }

        var previousLogo = company.LogoPath;
        string? newLogo = null;
        await using var transaction = await db.Database.BeginTransactionAsync();
        try
        {
            Apply(company, request);
            company.UpdatedAt = DateTime.UtcNow;
            if (request.Logo is not null)
            {
                newLogo = await logoStorage.SaveAsync(company.Id, request.Logo);
                company.LogoPath = newLogo;
            }
            await db.SaveChangesAsync();
            await transaction.CommitAsync();
        }
        catch
        {
            logoStorage.Delete(newLogo);
            throw;
        }

        if (newLogo is not null && previousLogo != newLogo)
            logoStorage.Delete(previousLogo);

        return Ok(CompanyResponse.FromEntity(company));
    }

    [HttpDelete("{id:long}")]
    [Authorize(Policy = "companies.delete")]
    [ServiceFilter(typeof(ApiCsrfFilter))]
    public async Task<IActionResult> Delete(long id)
    {
        var company = await db.Companies.FindAsync(id);
        if (company is null)
        {
            return NotFound();
        }

        if (await db.Branches.AnyAsync(x => x.CompanyId == id))
            return Conflict(new { detail = "Company has assigned branches." });

        var logoPath = company.LogoPath;
        db.Companies.Remove(company);
        await db.SaveChangesAsync();
        logoStorage.Delete(logoPath);

        return NoContent();
    }

    private bool ValidateLogo(IFormFile? logo)
    {
        var error = logoStorage.Validate(logo);
        if (error is null)
        {
            return true;
        }

        ModelState.AddModelError(nameof(CompanyRequest.Logo), error);
        return false;
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
