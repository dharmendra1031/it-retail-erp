using System.ComponentModel.DataAnnotations;
using System.Text.RegularExpressions;

namespace ITRetailERP.Web.Contracts;

public class NamedCatalogRequest
{
    [Required, MaxLength(30)] public string Code { get; set; } = "";
    [Required, MaxLength(200)] public string NameEn { get; set; } = "";
    [MaxLength(200)] public string NameAr { get; set; } = "";
    public bool IsActive { get; set; } = true;
}

public sealed class CategoryRequest : NamedCatalogRequest
{
    public long? ParentId { get; set; }
}

public sealed class UnitRequest : NamedCatalogRequest
{
    [Range(0, 6)] public int DecimalPlaces { get; set; }
}

public static class CatalogValidation
{
    public static string? Code(NamedCatalogRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.NameEn)) return null;
        var code = request.Code?.Trim().ToUpperInvariant();
        return code is not null && Regex.IsMatch(code, @"\A[A-Z0-9_-]{1,30}\z")
            ? code : null;
    }
}
