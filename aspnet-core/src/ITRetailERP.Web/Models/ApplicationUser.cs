using Microsoft.AspNetCore.Identity;

namespace ITRetailERP.Web.Models;

public sealed class ApplicationUser : IdentityUser
{
    public string? FullName { get; set; }
}
