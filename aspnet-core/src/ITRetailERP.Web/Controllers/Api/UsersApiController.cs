using ITRetailERP.Web.Contracts;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Controllers.Api;

[ApiController]
[Authorize(Roles = "Admin")]
[Route("api/users")]
public sealed class UsersApiController(
    ApplicationDbContext db, UserManager<ApplicationUser> users) : ControllerBase
{
    [HttpGet]
    public async Task<IActionResult> List()
    {
        var accounts = await db.Users.AsNoTracking().OrderBy(x => x.UserName).ToListAsync();
        var memberships = await db.UserRoles.AsNoTracking().ToListAsync();
        return Ok(accounts.Select(user => ToResponse(user,
            memberships.Where(x => x.UserId == user.Id).Select(x => x.RoleId))));
    }

    [HttpGet("{id:long}")]
    public async Task<IActionResult> Get(long id)
    {
        var user = await users.FindByIdAsync(id.ToString());
        if (user is null) return NotFound();
        return Ok(ToResponse(user, await db.UserRoles.Where(x => x.UserId == id)
            .Select(x => x.RoleId).ToListAsync()));
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(UserRequest request)
    {
        if (!Validate(request, creating: true))
            return BadRequest(new { detail = "Invalid request." });
        if (await users.FindByNameAsync(request.Username.Trim()) is not null
            || await users.FindByEmailAsync(request.Email.Trim()) is not null)
            return BadRequest(new { detail = "User already exists." });

        await using var transaction = await db.Database.BeginTransactionAsync();
        var user = new ApplicationUser
        {
            UserName = request.Username.Trim(),
            Email = request.Email.Trim().ToLowerInvariant(),
            FullName = request.FullName.Trim(),
            PhoneNumber = request.Mobile.Trim(),
            IsActive = request.IsActive,
            BranchId = request.BranchId,
        };
        var created = await users.CreateAsync(user, request.Password!);
        if (!created.Succeeded) return BadRequest(new { detail = "Invalid request." });
        db.UserRoles.AddRange(request.RoleIds.Distinct().Select(roleId =>
            new IdentityUserRole<long> { UserId = user.Id, RoleId = roleId }));
        await db.SaveChangesAsync();
        await transaction.CommitAsync();
        return CreatedAtAction(nameof(Get), new { id = user.Id },
            ToResponse(user, request.RoleIds));
    }

    [HttpPut("{id:long}")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update(long id, UserRequest request)
    {
        var user = await users.FindByIdAsync(id.ToString());
        if (user is null) return NotFound();
        if (!Validate(request, creating: false))
            return BadRequest(new { detail = "Invalid request." });
        var otherName = await users.FindByNameAsync(request.Username.Trim());
        var otherEmail = await users.FindByEmailAsync(request.Email.Trim());
        if ((otherName is not null && otherName.Id != id)
            || (otherEmail is not null && otherEmail.Id != id))
            return BadRequest(new { detail = "User already exists." });

        var adminRoleId = await db.Roles.Where(x => x.NormalizedName == "ADMIN")
            .Select(x => x.Id).FirstOrDefaultAsync();
        if (users.GetUserId(User) == id.ToString() &&
            (!request.IsActive || !request.RoleIds.Contains(adminRoleId)))
            return BadRequest(new { detail = "Cannot remove your own administrator access." });

        await using var transaction = await db.Database.BeginTransactionAsync();
        user.UserName = request.Username.Trim();
        user.Email = request.Email.Trim().ToLowerInvariant();
        user.FullName = request.FullName.Trim();
        user.PhoneNumber = request.Mobile.Trim();
        user.IsActive = request.IsActive;
        user.BranchId = request.BranchId;
        if (!(await users.UpdateAsync(user)).Succeeded)
            return BadRequest(new { detail = "Invalid request." });

        await db.UserRoles.Where(x => x.UserId == id).ExecuteDeleteAsync();
        db.UserRoles.AddRange(request.RoleIds.Distinct().Select(roleId =>
            new IdentityUserRole<long> { UserId = id, RoleId = roleId }));
        await db.SaveChangesAsync();
        await users.UpdateSecurityStampAsync(user);
        await transaction.CommitAsync();
        return Ok(ToResponse(user, request.RoleIds));
    }

    [HttpPut("{id:long}/password")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> ResetPassword(long id, PasswordRequest request)
    {
        var user = await users.FindByIdAsync(id.ToString());
        if (user is null) return NotFound();
        var token = await users.GeneratePasswordResetTokenAsync(user);
        var result = await users.ResetPasswordAsync(user, token, request.Password);
        return result.Succeeded ? NoContent() : BadRequest(new { detail = "Invalid request." });
    }

    private bool Validate(UserRequest request, bool creating)
    {
        if (string.IsNullOrWhiteSpace(request.Username) || string.IsNullOrWhiteSpace(request.Email)
            || request.FullName.Length > 150 || request.Mobile.Length > 30
            || (creating && string.IsNullOrWhiteSpace(request.Password))
            || request.RoleIds is null || request.RoleIds.Any(x => x <= 0)
            || (request.BranchId is not null &&
                !db.Branches.Any(branch => branch.Id == request.BranchId && branch.IsActive)))
            return false;
        return db.Roles.Count(role => request.RoleIds.Contains(role.Id)) ==
            request.RoleIds.Distinct().Count();
    }

    private static UserResponse ToResponse(ApplicationUser user, IEnumerable<long> roles) =>
        new(user.Id, user.UserName ?? "", user.FullName ?? "", user.Email ?? "",
            user.PhoneNumber ?? "", user.IsActive, roles.OrderBy(x => x).ToArray(), user.BranchId);
}
