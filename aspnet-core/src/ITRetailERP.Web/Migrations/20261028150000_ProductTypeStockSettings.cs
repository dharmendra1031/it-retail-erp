using ITRetailERP.Web.Data;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ITRetailERP.Web.Migrations;

[DbContext(typeof(ApplicationDbContext))]
[Migration("20261028150000_ProductTypeStockSettings")]
public partial class ProductTypeStockSettings : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddCheckConstraint(
            name: "CK_Products_TypeStockSettings",
            table: "Products",
            sql: "[ProductType] = N'stock' OR " +
                 "([ProductType] IN (N'nonstock', N'digital') AND " +
                 "[SerialTracked] = 0 AND [ReorderLevel] = 0)");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropCheckConstraint(
            name: "CK_Products_TypeStockSettings",
            table: "Products");
    }
}
