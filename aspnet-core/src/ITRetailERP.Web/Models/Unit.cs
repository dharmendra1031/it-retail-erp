using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Models;

public sealed class Unit
{
    public long Id { get; set; }
    [Required, MaxLength(30)] public string Code { get; set; } = "";
    [Required, MaxLength(200)] public string NameEn { get; set; } = "";
    [MaxLength(200)] public string NameAr { get; set; } = "";
    public int DecimalPlaces { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAtUtc { get; set; } = DateTime.UtcNow;
}
