using System.ComponentModel.DataAnnotations;
using System.Globalization;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;

namespace ITRetailERP.Web.Contracts;

public class PartnerRequest
{
    [Required, MaxLength(30)] public string Code { get; set; } = "";
    [Required, MaxLength(200)] public string NameEn { get; set; } = "";
    [MaxLength(200)] public string NameAr { get; set; } = "";
    [MaxLength(500)] public string AddressEn { get; set; } = "";
    [MaxLength(500)] public string AddressAr { get; set; } = "";
    [MaxLength(30)] public string Mobile { get; set; } = "";
    public int PaymentTermsDays { get; set; }
    public bool IsActive { get; set; } = true;
}

public sealed class CustomerRequest : PartnerRequest
{
    [MaxLength(30)] public string CivilId { get; set; } = "";
    [Required] public string CustomerType { get; set; } = "retail";
    [JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)]
    public decimal CreditLimit { get; set; }
}

public sealed class SupplierRequest : PartnerRequest
{
    [EmailAddress, MaxLength(200)] public string? Email { get; set; }
    [MaxLength(100)] public string TaxNumber { get; set; } = "";
    [JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)]
    public decimal OpeningBalance { get; set; }
}

public sealed record CustomerResponse(
    long Id, string Code, string NameEn, string NameAr, string AddressEn,
    string AddressAr, string Mobile,
    [property: JsonIgnore(Condition = JsonIgnoreCondition.WhenWritingNull)] string? CivilId,
    string CustomerType, int PaymentTermsDays, string CreditLimit, bool IsActive);

public sealed record SupplierResponse(
    long Id, string Code, string NameEn, string NameAr, string AddressEn,
    string AddressAr, string Mobile, string Email, string TaxNumber,
    int PaymentTermsDays, string OpeningBalance, bool IsActive);

public static class PartnerValidation
{
    public static bool IsValid(PartnerRequest request) =>
        !string.IsNullOrWhiteSpace(request.Code) &&
        Regex.IsMatch(request.Code.Trim().ToUpperInvariant(), @"\A[A-Z0-9_-]{1,30}\z") &&
        !string.IsNullOrWhiteSpace(request.NameEn) &&
        request.PaymentTermsDays is >= 0 and <= 365;

    public static bool Amount(decimal value) =>
        value >= 0 && value < 1000000000000000m &&
        decimal.Round(value, 3) == value;

    public static string Money(decimal value) => value.ToString("F3", CultureInfo.InvariantCulture);
}
