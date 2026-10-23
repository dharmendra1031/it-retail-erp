using Microsoft.AspNetCore.Identity;

namespace ITRetailERP.Web.Models;

public sealed class ApplicationUser : IdentityUser<long>
{
    public string? FullName { get; set; }
    public bool IsActive { get; set; } = true;
    public long? BranchId { get; set; }
}
