using ITRetailERP.Web.Models;

namespace ITRetailERP.Web.Contracts;

public sealed record CompanyResponse(
    long Id,
    string NameEn,
    string NameAr,
    string AddressEn,
    string AddressAr,
    string Telephone,
    string Mobile,
    string Email,
    string Website,
    string TaxNumber,
    string CommercialRegistrationNumber,
    string LogoUrl,
    string BankDetails,
    string InvoiceHeader,
    string InvoiceFooter,
    string TermsAndConditions,
    string SocialMedia,
    bool IsActive)
{
    public static CompanyResponse FromEntity(Company company) => new(
        company.Id,
        company.NameEn,
        company.NameAr ?? string.Empty,
        company.AddressEn ?? string.Empty,
        company.AddressAr ?? string.Empty,
        company.Telephone ?? string.Empty,
        company.Mobile ?? string.Empty,
        company.Email ?? string.Empty,
        company.Website ?? string.Empty,
        company.TaxNumber ?? string.Empty,
        company.CommercialRegistrationNumber ?? string.Empty,
        company.LogoPath ?? string.Empty,
        company.BankDetails ?? string.Empty,
        company.InvoiceHeader ?? string.Empty,
        company.InvoiceFooter ?? string.Empty,
        company.TermsAndConditions ?? string.Empty,
        company.SocialMedia ?? string.Empty,
        company.IsActive);
}
