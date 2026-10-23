using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Models;

public sealed class DocumentSequence
{
    public long Id { get; set; }

    [Required, MaxLength(20)]
    public string Series { get; set; } = string.Empty;

    public int FiscalYear { get; set; }
    public long BranchId { get; set; }
    public long LastNumber { get; set; }
}
