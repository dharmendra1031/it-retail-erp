using System.Security.Cryptography;

namespace ITRetailERP.Web.Services;

public sealed class CompanyLogoStorage(IWebHostEnvironment environment)
{
    private const long MaxFileSize = 2 * 1024 * 1024;

    public string? Validate(IFormFile? file)
    {
        if (file is null) return null;
        if (file.Length == 0 || file.Length > MaxFileSize)
            return "Logo must be smaller than 2 MB.";

        var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
        if (!((ext is ".jpg" or ".jpeg") && file.ContentType == "image/jpeg"
            || ext == ".png" && file.ContentType == "image/png"
            || ext == ".webp" && file.ContentType == "image/webp"))
            return "Invalid logo file type.";

        Span<byte> header = stackalloc byte[12];
        using var stream = file.OpenReadStream();
        if (stream.ReadAtLeast(header, 12, throwOnEndOfStream: false) != 12)
            return "Invalid logo file type.";

        var valid = ext switch
        {
            ".jpg" or ".jpeg" => header[0] == 0xFF && header[1] == 0xD8 && header[2] == 0xFF,
            ".png" => header[..8].SequenceEqual(new byte[] { 137, 80, 78, 71, 13, 10, 26, 10 }),
            ".webp" => header[..4].SequenceEqual("RIFF"u8) && header[8..12].SequenceEqual("WEBP"u8),
            _ => false,
        };
        return valid ? null : "Invalid logo file type.";
    }

    public async Task<string> SaveAsync(long companyId, IFormFile file)
    {
        var extension = Path.GetExtension(file.FileName).ToLowerInvariant();
        var folder = GetDirectory();
        Directory.CreateDirectory(folder);
        var name = $"company-{companyId}-{RandomNumberGenerator.GetHexString(12).ToLowerInvariant()}{extension}";
        var path = Path.Combine(folder, name);
        try
        {
            await using var output = new FileStream(path, FileMode.CreateNew);
            await file.CopyToAsync(output);
        }
        catch
        {
            if (File.Exists(path)) File.Delete(path);
            throw;
        }
        return $"/uploads/companies/{name}";
    }

    public void Delete(string? logoPath)
    {
        if (string.IsNullOrWhiteSpace(logoPath)) return;
        var path = Path.Combine(GetDirectory(), Path.GetFileName(logoPath));
        if (File.Exists(path)) File.Delete(path);
    }

    private string GetDirectory()
    {
        var webRoot = environment.WebRootPath ?? Path.Combine(environment.ContentRootPath, "wwwroot");
        return Path.Combine(webRoot, "uploads", "companies");
    }
}
