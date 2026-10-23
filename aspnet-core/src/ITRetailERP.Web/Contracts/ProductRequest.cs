using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace ITRetailERP.Web.Contracts;

public sealed class ProductRequest
{
    [Required, MaxLength(40)] public string Sku { get; set; } = "";
    [MaxLength(64)] public string? Barcode { get; set; }
    [Required, MaxLength(200)] public string NameEn { get; set; } = "";
    [MaxLength(200)] public string NameAr { get; set; } = "";
    [MaxLength(1000)] public string DescriptionEn { get; set; } = "";
    [MaxLength(1000)] public string DescriptionAr { get; set; } = "";
    [Range(1, long.MaxValue)] public long CategoryId { get; set; }
    public long? BrandId { get; set; }
    [Range(1, long.MaxValue)] public long UnitId { get; set; }
    [Required] public string ProductType { get; set; } = "stock";
    public bool SerialTracked { get; set; }
    [JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)] public decimal CostPrice { get; set; }
    [JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)] public decimal BasePrice { get; set; }
    [JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)] public decimal MinPrice { get; set; }
    [JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)] public decimal ReorderLevel { get; set; }
    public bool IsActive { get; set; } = true;
}

public sealed record ProductResponse(
    long Id, string Sku, string? Barcode, string NameEn, string NameAr,
    string DescriptionEn, string DescriptionAr, long CategoryId, long? BrandId,
    long UnitId, string ProductType, bool SerialTracked,
    string CostPrice, string BasePrice, string MinPrice, string ReorderLevel, bool IsActive);
