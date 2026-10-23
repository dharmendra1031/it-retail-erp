using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Models;

public sealed class Product
{
    public long Id { get; set; }
    [Required, MaxLength(40)] public string Sku { get; set; } = "";
    [MaxLength(64)] public string? Barcode { get; set; }
    [Required, MaxLength(200)] public string NameEn { get; set; } = "";
    [MaxLength(200)] public string NameAr { get; set; } = "";
    [MaxLength(1000)] public string DescriptionEn { get; set; } = "";
    [MaxLength(1000)] public string DescriptionAr { get; set; } = "";
    public long CategoryId { get; set; }
    public long? BrandId { get; set; }
    public long UnitId { get; set; }
    [Required, MaxLength(20)] public string ProductType { get; set; } = "stock";
    public bool SerialTracked { get; set; }
    public decimal CostPrice { get; set; }
    public decimal BasePrice { get; set; }
    public decimal MinPrice { get; set; }
    public decimal ReorderLevel { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAtUtc { get; set; } = DateTime.UtcNow;
}
