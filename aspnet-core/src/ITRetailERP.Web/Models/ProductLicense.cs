using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Models;

public sealed class ProductLicense
{
    public long Id { get; set; }
    public long ProductId { get; set; }
    public Product Product { get; set; } = null!;
    [MaxLength(100)] public string LicenseNumber { get; set; } = "";
    public byte[]? EncryptedKey { get; set; }
    [MaxLength(32)] public byte[]? KeyFingerprint { get; set; }
    public DateOnly? ActivationDate { get; set; }
    public DateOnly? ExpiryDate { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAtUtc { get; set; } = DateTime.UtcNow;
}
