using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Contracts;

public sealed class CompanyRequest
{
    [Required, MaxLength(200)]
    public string NameEn { get; set; } = string.Empty;

    [MaxLength(200)]
    public string? NameAr { get; set; }

    [MaxLength(500)]
    public string? AddressEn { get; set; }

    [MaxLength(500)]
    public string? AddressAr { get; set; }

    [MaxLength(30)]
    public string? Telephone { get; set; }

    [MaxLength(30)]
    public string? Mobile { get; set; }

    [EmailAddress, MaxLength(200)]
    public string? Email { get; set; }

    [Url, MaxLength(250)]
    public string? Website { get; set; }

    [MaxLength(100)]
    public string? TaxNumber { get; set; }

    [MaxLength(100)]
    public string? CommercialRegistrationNumber { get; set; }

    public IFormFile? Logo { get; set; }
    public string? BankDetails { get; set; }
    public string? InvoiceHeader { get; set; }
    public string? InvoiceFooter { get; set; }
    public string? TermsAndConditions { get; set; }
    public string? SocialMedia { get; set; }
    public bool IsActive { get; set; } = true;
}
