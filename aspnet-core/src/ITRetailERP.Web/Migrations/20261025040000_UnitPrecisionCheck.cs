using ITRetailERP.Web.Data;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ITRetailERP.Web.Migrations;

[DbContext(typeof(ApplicationDbContext))]
[Migration("20261025040000_UnitPrecisionCheck")]
public partial class UnitPrecisionCheck : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddCheckConstraint(
            name: "CK_Units_DecimalPlaces",
            table: "Units",
            sql: "[DecimalPlaces] BETWEEN 0 AND 6");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropCheckConstraint(
            name: "CK_Units_DecimalPlaces",
            table: "Units");
    }
}
