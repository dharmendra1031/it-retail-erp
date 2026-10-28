using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Contracts;

public sealed class ProductLicenseRequest
{
    [Range(1, long.MaxValue)] public long ProductId { get; set; }
    [MaxLength(512)] public string? LicenseKey { get; set; }
    [MaxLength(100)] public string LicenseNumber { get; set; } = "";
    public DateOnly? ActivationDate { get; set; }
    public DateOnly? ExpiryDate { get; set; }
}

public sealed record ProductLicenseResponse(
    long Id, long ProductId, string LicenseNumber, bool HasKey,
    DateOnly? ActivationDate, DateOnly? ExpiryDate, bool IsActive);
