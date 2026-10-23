namespace ITRetailERP.Web.Services;

public static class PartnerDocumentStorage
{
    public const long MaximumBytes = 5 * 1024 * 1024;

    public static async Task<byte[]?> ReadAsync(IFormFile? file)
    {
        if (file is null || file.Length == 0 || file.Length > MaximumBytes)
            return null;

        await using var stream = new MemoryStream();
        await file.CopyToAsync(stream);
        var content = stream.ToArray();
        var valid = file.ContentType switch
        {
            "application/pdf" => content.AsSpan().StartsWith("%PDF-"u8),
            "image/png" => content.AsSpan().StartsWith(new byte[] { 137, 80, 78, 71, 13, 10, 26, 10 }),
            "image/jpeg" => content.AsSpan().StartsWith(new byte[] { 0xFF, 0xD8, 0xFF }),
            _ => false,
        };
        return valid ? content : null;
    }

    public static object Describe(Models.PartnerDocument document) => new
    {
        document.Id, document.FileName, document.ContentType, Size = document.Content.Length
    };

    public static string SafeName(string name)
    {
        var result = Path.GetFileName(name.Replace('\\', '/'));
        var safe = string.Concat(result.Where(c => !char.IsControl(c) && c != '"'));
        return safe[..Math.Min(200, safe.Length)];
    }
}
