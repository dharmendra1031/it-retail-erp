using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Controllers;

public sealed class CompaniesController(ApplicationDbContext db, IWebHostEnvironment environment) : Controller
{
    private const long MaxLogoBytes = 2 * 1024 * 1024;
    private static readonly HashSet<string> AllowedLogoExtensions =
        new(StringComparer.OrdinalIgnoreCase) { ".jpg", ".jpeg", ".png", ".webp" };

    public async Task<IActionResult> Index()
    {
        var companies = await db.Companies
            .AsNoTracking()
            .OrderBy(x => x.NameEn)
            .ToListAsync();

        return View(companies);
    }

    public async Task<IActionResult> Details(long id)
    {
        var company = await db.Companies
            .AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == id);

        return company is null ? NotFound() : View(company);
    }

    public IActionResult Create() => View(new Company());

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(Company input, IFormFile? logoFile)
    {
        ValidateLogo(logoFile);

        if (!ModelState.IsValid)
        {
            return View(input);
        }

        input.Id = 0;
        input.CreatedAt = DateTime.UtcNow;
        input.UpdatedAt = input.CreatedAt;
        input.LogoPath = await SaveLogoAsync(logoFile);

        db.Companies.Add(input);
        await db.SaveChangesAsync();

        return RedirectToAction(nameof(Index));
    }

    public async Task<IActionResult> Edit(long id)
    {
        var company = await db.Companies.FindAsync(id);
        return company is null ? NotFound() : View(company);
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(long id, Company input, IFormFile? logoFile)
    {
        var company = await db.Companies.FindAsync(id);
        if (company is null)
        {
            return NotFound();
        }

        ValidateLogo(logoFile);

        if (!ModelState.IsValid)
        {
            input.Id = id;
            input.LogoPath = company.LogoPath;
            return View(input);
        }

        ApplyChanges(company, input);

        var previousLogo = company.LogoPath;
        if (logoFile is not null)
        {
            company.LogoPath = await SaveLogoAsync(logoFile);
        }

        company.UpdatedAt = DateTime.UtcNow;
        await db.SaveChangesAsync();

        if (logoFile is not null)
        {
            DeleteLogo(previousLogo);
        }

        return RedirectToAction(nameof(Index));
    }

    public async Task<IActionResult> Delete(long id)
    {
        var company = await db.Companies
            .AsNoTracking()
            .FirstOrDefaultAsync(x => x.Id == id);

        return company is null ? NotFound() : View(company);
    }

    [HttpPost, ActionName("Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteConfirmed(long id)
    {
        var company = await db.Companies.FindAsync(id);
        if (company is null)
        {
            return NotFound();
        }

        db.Companies.Remove(company);
        await db.SaveChangesAsync();
        DeleteLogo(company.LogoPath);

        return RedirectToAction(nameof(Index));
    }

    private void ValidateLogo(IFormFile? logoFile)
    {
        if (logoFile is null)
        {
            return;
        }

        if (logoFile.Length == 0 || logoFile.Length > MaxLogoBytes)
        {
            ModelState.AddModelError("LogoPath", "Logo must be smaller than 2 MB.");
            return;
        }

        var extension = Path.GetExtension(logoFile.FileName);
        if (!AllowedLogoExtensions.Contains(extension))
        {
            ModelState.AddModelError("LogoPath", "Logo must be JPG, PNG or WebP.");
        }
    }

    private async Task<string?> SaveLogoAsync(IFormFile? logoFile)
    {
        if (logoFile is null)
        {
            return null;
        }

        var extension = Path.GetExtension(logoFile.FileName).ToLowerInvariant();
        var webRoot = environment.WebRootPath ?? Path.Combine(environment.ContentRootPath, "wwwroot");
        var directory = Path.Combine(webRoot, "uploads", "companies");
        Directory.CreateDirectory(directory);

        var fileName = $"{Guid.NewGuid():N}{extension}";
        var filePath = Path.Combine(directory, fileName);

        await using var stream = System.IO.File.Create(filePath);
        await logoFile.CopyToAsync(stream);

        return $"/uploads/companies/{fileName}";
    }

    private void DeleteLogo(string? logoPath)
    {
        if (string.IsNullOrWhiteSpace(logoPath))
        {
            return;
        }

        var webRoot = environment.WebRootPath ?? Path.Combine(environment.ContentRootPath, "wwwroot");
        var relativePath = logoPath.TrimStart('/').Replace('/', Path.DirectorySeparatorChar);
        var filePath = Path.Combine(webRoot, relativePath);

        if (System.IO.File.Exists(filePath))
        {
            System.IO.File.Delete(filePath);
        }
    }

    private static void ApplyChanges(Company target, Company source)
    {
        target.NameEn = source.NameEn;
        target.NameAr = source.NameAr;
        target.AddressEn = source.AddressEn;
        target.AddressAr = source.AddressAr;
        target.Telephone = source.Telephone;
        target.Mobile = source.Mobile;
        target.Email = source.Email;
        target.Website = source.Website;
        target.TaxNumber = source.TaxNumber;
        target.CommercialRegistrationNumber = source.CommercialRegistrationNumber;
        target.BankDetails = source.BankDetails;
        target.InvoiceHeader = source.InvoiceHeader;
        target.InvoiceFooter = source.InvoiceFooter;
        target.TermsAndConditions = source.TermsAndConditions;
        target.SocialMedia = source.SocialMedia;
        target.IsActive = source.IsActive;
    }
}
