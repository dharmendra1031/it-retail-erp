using ITRetailERP.Web.Data;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ITRetailERP.Web.Migrations;

[DbContext(typeof(ApplicationDbContext))]
[Migration("20261023140000_Products")]
public partial class Products : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Products",
            columns: table => new
            {
                Id = table.Column<long>(type: "bigint", nullable: false).Annotation("SqlServer:Identity", "1, 1"),
                Sku = table.Column<string>(type: "nvarchar(40)", maxLength: 40, nullable: false),
                Barcode = table.Column<string>(type: "nvarchar(64)", maxLength: 64, nullable: true),
                NameEn = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                NameAr = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                DescriptionEn = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: false),
                DescriptionAr = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: false),
                CategoryId = table.Column<long>(type: "bigint", nullable: false),
                BrandId = table.Column<long>(type: "bigint", nullable: true),
                UnitId = table.Column<long>(type: "bigint", nullable: false),
                ProductType = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                SerialTracked = table.Column<bool>(type: "bit", nullable: false),
                CostPrice = table.Column<decimal>(type: "decimal(18,3)", nullable: false),
                BasePrice = table.Column<decimal>(type: "decimal(18,3)", nullable: false),
                MinPrice = table.Column<decimal>(type: "decimal(18,3)", nullable: false),
                ReorderLevel = table.Column<decimal>(type: "decimal(18,6)", nullable: false),
                IsActive = table.Column<bool>(type: "bit", nullable: false),
                CreatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
                UpdatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Products", x => x.Id);
                table.ForeignKey("FK_Products_Categories_CategoryId", x => x.CategoryId,
                    "Categories", "Id", onDelete: ReferentialAction.Restrict);
                table.ForeignKey("FK_Products_Brands_BrandId", x => x.BrandId,
                    "Brands", "Id", onDelete: ReferentialAction.Restrict);
                table.ForeignKey("FK_Products_Units_UnitId", x => x.UnitId,
                    "Units", "Id", onDelete: ReferentialAction.Restrict);
            });
        migrationBuilder.CreateIndex("IX_Products_Sku", "Products", "Sku", unique: true);
        migrationBuilder.CreateIndex("IX_Products_Barcode", "Products", "Barcode", unique: true, filter: "[Barcode] IS NOT NULL");
        migrationBuilder.CreateIndex("IX_Products_CategoryId", "Products", "CategoryId");
        migrationBuilder.CreateIndex("IX_Products_BrandId", "Products", "BrandId");
        migrationBuilder.CreateIndex("IX_Products_UnitId", "Products", "UnitId");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable("Products");
    }
}
