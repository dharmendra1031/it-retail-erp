using ITRetailERP.Web.Security;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace ITRetailERP.Web.Controllers.Api;

[ApiController]
[Route("api/permissions")]
[Authorize(Policy = "roles.view")]
public sealed class PermissionsApiController : ControllerBase
{
    [HttpGet]
    public IActionResult List() => Ok(PermissionCatalog.Items);
}
