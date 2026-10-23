using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Models;

public sealed class Supplier
{
    public long Id { get; set; }
    [Required, MaxLength(30)] public string Code { get; set; } = "";
    [Required, MaxLength(200)] public string NameEn { get; set; } = "";
    [MaxLength(200)] public string NameAr { get; set; } = "";
    [MaxLength(500)] public string AddressEn { get; set; } = "";
    [MaxLength(500)] public string AddressAr { get; set; } = "";
    [MaxLength(30)] public string Mobile { get; set; } = "";
    [MaxLength(150)] public string ContactPerson { get; set; } = "";
    [MaxLength(30)] public string Telephone { get; set; } = "";
    [MaxLength(1000)] public string Remarks { get; set; } = "";
    [MaxLength(200)] public string Email { get; set; } = "";
    [MaxLength(100)] public string TaxNumber { get; set; } = "";
    public int PaymentTermsDays { get; set; }
    public decimal OpeningBalance { get; set; }
    public decimal CreditLimit { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAtUtc { get; set; } = DateTime.UtcNow;
}
