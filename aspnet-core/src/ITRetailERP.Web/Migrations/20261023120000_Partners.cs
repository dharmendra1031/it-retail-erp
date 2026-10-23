using ITRetailERP.Web.Data;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ITRetailERP.Web.Migrations;

[DbContext(typeof(ApplicationDbContext))]
[Migration("20261023120000_Partners")]
public partial class Partners : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Customers",
            columns: table => new
            {
                Id = table.Column<long>(type: "bigint", nullable: false).Annotation("SqlServer:Identity", "1, 1"),
                Code = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                NameEn = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                NameAr = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                AddressEn = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                AddressAr = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                Mobile = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                CivilId = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                CustomerType = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                PaymentTermsDays = table.Column<int>(type: "int", nullable: false),
                CreditLimit = table.Column<decimal>(type: "decimal(18,3)", nullable: false),
                IsActive = table.Column<bool>(type: "bit", nullable: false),
                CreatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
                UpdatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
            },
            constraints: table => table.PrimaryKey("PK_Customers", x => x.Id));
        migrationBuilder.CreateIndex("IX_Customers_Code", "Customers", "Code", unique: true);

        migrationBuilder.CreateTable(
            name: "Suppliers",
            columns: table => new
            {
                Id = table.Column<long>(type: "bigint", nullable: false).Annotation("SqlServer:Identity", "1, 1"),
                Code = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                NameEn = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                NameAr = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                AddressEn = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                AddressAr = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                Mobile = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                Email = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                TaxNumber = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                PaymentTermsDays = table.Column<int>(type: "int", nullable: false),
                OpeningBalance = table.Column<decimal>(type: "decimal(18,3)", nullable: false),
                IsActive = table.Column<bool>(type: "bit", nullable: false),
                CreatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
                UpdatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
            },
            constraints: table => table.PrimaryKey("PK_Suppliers", x => x.Id));
        migrationBuilder.CreateIndex("IX_Suppliers_Code", "Suppliers", "Code", unique: true);

        migrationBuilder.CreateTable(
            name: "PartnerDocuments",
            columns: table => new
            {
                Id = table.Column<long>(type: "bigint", nullable: false).Annotation("SqlServer:Identity", "1, 1"),
                CustomerId = table.Column<long>(type: "bigint", nullable: true),
                SupplierId = table.Column<long>(type: "bigint", nullable: true),
                FileName = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                ContentType = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false),
                Content = table.Column<byte[]>(type: "varbinary(max)", nullable: false),
                CreatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
                UpdatedAtUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_PartnerDocuments", x => x.Id);
                table.CheckConstraint("CK_PartnerDocuments_OneOwner",
                    "([CustomerId] IS NOT NULL AND [SupplierId] IS NULL) OR ([CustomerId] IS NULL AND [SupplierId] IS NOT NULL)");
                table.ForeignKey("FK_PartnerDocuments_Customers_CustomerId", x => x.CustomerId, "Customers", "Id", onDelete: ReferentialAction.Restrict);
                table.ForeignKey("FK_PartnerDocuments_Suppliers_SupplierId", x => x.SupplierId, "Suppliers", "Id", onDelete: ReferentialAction.Restrict);
            });
        migrationBuilder.CreateIndex("IX_PartnerDocuments_CustomerId", "PartnerDocuments", "CustomerId");
        migrationBuilder.CreateIndex("IX_PartnerDocuments_SupplierId", "PartnerDocuments", "SupplierId");
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable("PartnerDocuments");
        migrationBuilder.DropTable("Suppliers");
        migrationBuilder.DropTable("Customers");
    }
}
