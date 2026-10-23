using ITRetailERP.Web.Data;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ITRetailERP.Web.Migrations;

[DbContext(typeof(ApplicationDbContext))]
[Migration("20261023110000_BranchesWarehouses")]
public partial class BranchesWarehouses : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Branches",
            columns: table => new
            {
                Id = table.Column<long>(type: "bigint", nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                CompanyId = table.Column<long>(type: "bigint", nullable: false),
                Code = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                NameEn = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                NameAr = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                IsActive = table.Column<bool>(type: "bit", nullable: false),
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Branches", x => x.Id);
                table.ForeignKey("FK_Branches_Companies_CompanyId", x => x.CompanyId, "Companies", "Id", onDelete: ReferentialAction.Restrict);
            });
        migrationBuilder.CreateIndex("IX_Branches_CompanyId_Code", "Branches", new[] { "CompanyId", "Code" }, unique: true);

        migrationBuilder.CreateTable(
            name: "Warehouses",
            columns: table => new
            {
                Id = table.Column<long>(type: "bigint", nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                BranchId = table.Column<long>(type: "bigint", nullable: false),
                Code = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                NameEn = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                NameAr = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                IsActive = table.Column<bool>(type: "bit", nullable: false),
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Warehouses", x => x.Id);
                table.ForeignKey("FK_Warehouses_Branches_BranchId", x => x.BranchId, "Branches", "Id", onDelete: ReferentialAction.Restrict);
            });
        migrationBuilder.CreateIndex("IX_Warehouses_BranchId_Code", "Warehouses", new[] { "BranchId", "Code" }, unique: true);

        migrationBuilder.AddColumn<long>(name: "BranchId", table: "AspNetUsers", type: "bigint", nullable: true);
        migrationBuilder.CreateIndex("IX_AspNetUsers_BranchId", "AspNetUsers", "BranchId");
        migrationBuilder.AddForeignKey(
            name: "FK_AspNetUsers_Branches_BranchId",
            table: "AspNetUsers",
            column: "BranchId",
            principalTable: "Branches",
            principalColumn: "Id",
            onDelete: ReferentialAction.Restrict);
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropForeignKey("FK_AspNetUsers_Branches_BranchId", "AspNetUsers");
        migrationBuilder.DropIndex("IX_AspNetUsers_BranchId", "AspNetUsers");
        migrationBuilder.DropColumn("BranchId", "AspNetUsers");
        migrationBuilder.DropTable("Warehouses");
        migrationBuilder.DropTable("Branches");
    }
}
