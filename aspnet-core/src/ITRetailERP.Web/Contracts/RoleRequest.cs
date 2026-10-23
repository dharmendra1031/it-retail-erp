using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Contracts;

public sealed class RoleRequest
{
    [Required, MaxLength(100)]
    public string Name { get; set; } = string.Empty;
}

public sealed record RoleResponse(long Id, string Name);

public sealed class RolePermissionsRequest
{
    [Required]
    public string[] Permissions { get; set; } = [];
}
