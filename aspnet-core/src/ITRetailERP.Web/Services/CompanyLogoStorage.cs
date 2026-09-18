namespace ITRetailERP.Web.Services;

public sealed class CompanyLogoStorage(IWebHostEnvironment environment)
{
    private const long MaxFileSize = 2 * 1024 * 1024;

    private static readonly HashSet<string> AllowedExtensions =
        new(StringComparer.OrdinalIgnoreCase) { ".jpg", ".jpeg", ".png", ".webp" };

    public string? Validate(IFormFile? file)
    {
        if (file is null)
        {
            return null;
        }

        if (file.Length == 0 || file.Length > MaxFileSize)
        {
            return "Logo must be smaller than 2 MB.";
        }

        return AllowedExtensions.Contains(Path.GetExtension(file.FileName))
            ? null
            : "Logo must be JPG, PNG or WebP.";
    }

    public async Task<string> SaveAsync(long companyId, IFormFile file)
    {
        var extension = Path.GetExtension(file.FileName).ToLowerInvariant();
        var directory = GetDirectory();

        Directory.CreateDirectory(directory);

        var fileName = $"company-{companyId}{extension}";
        var filePath = Path.Combine(directory, fileName);

        await using var stream = new FileStream(filePath, FileMode.Create);
        await file.CopyToAsync(stream);

        return $"/uploads/companies/{fileName}";
    }

    public void Delete(string? logoPath)
    {
        if (string.IsNullOrWhiteSpace(logoPath))
        {
            return;
        }

        var filePath = Path.Combine(GetDirectory(), Path.GetFileName(logoPath));
        if (File.Exists(filePath))
        {
            File.Delete(filePath);
        }
    }

    private string GetDirectory()
    {
        var webRoot = environment.WebRootPath ?? Path.Combine(environment.ContentRootPath, "wwwroot");
        return Path.Combine(webRoot, "uploads", "companies");
    }
}
