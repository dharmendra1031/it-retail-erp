using System.ComponentModel.DataAnnotations;

namespace ITRetailERP.Web.Contracts;

public sealed class UserRequest
{
    [Required, MaxLength(150)]
    public string Username { get; set; } = string.Empty;

    [Required, EmailAddress, MaxLength(254)]
    public string Email { get; set; } = string.Empty;

    [MaxLength(150)]
    public string FullName { get; set; } = string.Empty;

    [MaxLength(30)]
    public string Mobile { get; set; } = string.Empty;

    public bool IsActive { get; set; } = true;
    public long? BranchId { get; set; }

    [Required]
    public long[] RoleIds { get; set; } = [];

    public string? Password { get; set; }
}

public sealed class PasswordRequest
{
    [Required]
    public string Password { get; set; } = string.Empty;
}

public sealed record UserResponse(
    long Id, string Username, string FullName, string Email,
    string Mobile, bool IsActive, long[] RoleIds, long? BranchId);
