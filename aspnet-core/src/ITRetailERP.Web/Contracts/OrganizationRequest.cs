using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Contracts;

public sealed class BranchRequest
{
    [Range(1, long.MaxValue)]
    public long CompanyId { get; set; }
    [Required, MaxLength(30)]
    public string Code { get; set; } = string.Empty;
    [Required, MaxLength(200)]
    public string NameEn { get; set; } = string.Empty;
    [MaxLength(200)]
    public string NameAr { get; set; } = string.Empty;
    public bool IsActive { get; set; } = true;
}

public sealed class WarehouseRequest
{
    [Range(1, long.MaxValue)]
    public long BranchId { get; set; }
    [Required, MaxLength(30)]
    public string Code { get; set; } = string.Empty;
    [Required, MaxLength(200)]
    public string NameEn { get; set; } = string.Empty;
    [MaxLength(200)]
    public string NameAr { get; set; } = string.Empty;
    public bool IsActive { get; set; } = true;
}
