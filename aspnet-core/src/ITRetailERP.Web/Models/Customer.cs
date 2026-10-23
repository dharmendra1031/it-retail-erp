using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Models;

public sealed class Customer
{
    public long Id { get; set; }
    [Required, MaxLength(30)] public string Code { get; set; } = "";
    [Required, MaxLength(200)] public string NameEn { get; set; } = "";
    [MaxLength(200)] public string NameAr { get; set; } = "";
    [MaxLength(500)] public string AddressEn { get; set; } = "";
    [MaxLength(500)] public string AddressAr { get; set; } = "";
    [MaxLength(30)] public string Mobile { get; set; } = "";
    [MaxLength(30)] public string CivilId { get; set; } = "";
    [Required, MaxLength(20)] public string CustomerType { get; set; } = "retail";
    public int PaymentTermsDays { get; set; }
    public decimal CreditLimit { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAtUtc { get; set; } = DateTime.UtcNow;
}
