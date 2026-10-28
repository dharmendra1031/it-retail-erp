using ITRetailERP.Web.Data;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ITRetailERP.Web.Migrations;

[DbContext(typeof(ApplicationDbContext))]
[Migration("20261028160000_ProductLicenses")]
public partial class ProductLicenses : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "ProductLicenses",
            columns: table => new
            {
                Id = table.Column<long>(type: "bigint", nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                ProductId = table.Column<long>(type: "bigint", nullable: false),
                LicenseNumber = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                EncryptedKey = table.Column<byte[]>(type: "varbinary(max)", nullable: true),
                KeyFingerprint = table.Column<byte[]>(type: "varbinary(32)", maxLength: 32, nullable: true),
                ActivationDate = table.Column<DateOnly>(type: "date", nullable: true),
                ExpiryDate = table.Column<DateOnly>(type: "date", nullable: true),
                IsActive = table.Column<bool>(type: "bit", nullable: false),
                CreatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
                UpdatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_ProductLicenses", x => x.Id);
                table.ForeignKey("FK_ProductLicenses_Products_ProductId", x => x.ProductId,
                    "Products", "Id", onDelete: ReferentialAction.Restrict);
                table.CheckConstraint("CK_ProductLicenses_DatesAndIdentity",
                    "([EncryptedKey] IS NOT NULL OR LEN([LicenseNumber]) > 0) AND " +
                    "([ActivationDate] IS NULL OR [ExpiryDate] IS NULL OR [ExpiryDate] >= [ActivationDate]) AND " +
                    "(([EncryptedKey] IS NULL AND [KeyFingerprint] IS NULL) OR " +
                    "([EncryptedKey] IS NOT NULL AND [KeyFingerprint] IS NOT NULL))");
            });
        migrationBuilder.CreateIndex("IX_ProductLicenses_ProductId", "ProductLicenses", "ProductId");
        migrationBuilder.CreateIndex("IX_ProductLicenses_KeyFingerprint", "ProductLicenses",
            "KeyFingerprint", unique: true,
            filter: "[IsActive] = 1 AND [KeyFingerprint] IS NOT NULL");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable("ProductLicenses");
    }
}
