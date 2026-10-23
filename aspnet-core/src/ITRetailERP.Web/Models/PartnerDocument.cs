using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Models;

public sealed class PartnerDocument
{
    public long Id { get; set; }
    public long? CustomerId { get; set; }
    public long? SupplierId { get; set; }
    [Required, MaxLength(200)] public string FileName { get; set; } = "";
    [Required, MaxLength(50)] public string ContentType { get; set; } = "";
    public byte[] Content { get; set; } = [];
    public DateTime CreatedAtUtc { get; set; } = DateTime.UtcNow;
    public DateTime UpdatedAtUtc { get; set; } = DateTime.UtcNow;
}
