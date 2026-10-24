using Microsoft.Data.SqlClient;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Services;

public static class SqlConstraintErrors
{
    public static bool IsDuplicate(DbUpdateException error) =>
        error.InnerException is SqlException { Number: 2601 or 2627 };
}
