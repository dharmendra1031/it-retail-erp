using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Models;

public sealed class Warehouse
{
    public long Id { get; set; }
    public long BranchId { get; set; }
    [Required, MaxLength(30)]
    public string Code { get; set; } = string.Empty;
    [Required, MaxLength(200)]
    public string NameEn { get; set; } = string.Empty;
    [MaxLength(200)]
    public string NameAr { get; set; } = string.Empty;
    public bool IsActive { get; set; } = true;
}
