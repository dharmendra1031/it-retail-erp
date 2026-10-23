using ITRetailERP.Web.Data;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ITRetailERP.Web.Migrations;

[DbContext(typeof(ApplicationDbContext))]
[Migration("20261023070000_DocumentSequences")]
public partial class DocumentSequences : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "DocumentSequences",
            columns: table => new
            {
                Id = table.Column<long>(type: "bigint", nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                Series = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                FiscalYear = table.Column<int>(type: "int", nullable: false),
                BranchId = table.Column<long>(type: "bigint", nullable: false),
                LastNumber = table.Column<long>(type: "bigint", nullable: false),
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_DocumentSequences", x => x.Id);
            });

        migrationBuilder.CreateIndex(
            name: "IX_DocumentSequences_Series_FiscalYear_BranchId",
            table: "DocumentSequences",
            columns: new[] { "Series", "FiscalYear", "BranchId" },
            unique: true);
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "DocumentSequences");
    }
}
