using ITRetailERP.Web.Data;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ITRetailERP.Web.Migrations;

[DbContext(typeof(ApplicationDbContext))]
[Migration("20261023080000_UniqueNormalizedEmail")]
public partial class UniqueNormalizedEmail : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql("""
            IF EXISTS (
                SELECT 1 FROM [AspNetUsers]
                WHERE [NormalizedEmail] IS NOT NULL
                GROUP BY [NormalizedEmail]
                HAVING COUNT_BIG(*) > 1
            )
                THROW 50002, 'Resolve duplicate normalized emails before upgrading.', 1;
            """);

        migrationBuilder.DropIndex(name: "EmailIndex", table: "AspNetUsers");
        migrationBuilder.CreateIndex(
            name: "EmailIndex",
            table: "AspNetUsers",
            column: "NormalizedEmail",
            unique: true,
            filter: "[NormalizedEmail] IS NOT NULL");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropIndex(name: "EmailIndex", table: "AspNetUsers");
        migrationBuilder.CreateIndex(
            name: "EmailIndex",
            table: "AspNetUsers",
            column: "NormalizedEmail");
    }
}
