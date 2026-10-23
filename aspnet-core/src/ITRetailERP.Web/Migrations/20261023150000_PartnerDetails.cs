using ITRetailERP.Web.Data;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ITRetailERP.Web.Migrations;

[DbContext(typeof(ApplicationDbContext))]
[Migration("20261023150000_PartnerDetails")]
public partial class PartnerDetails : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.AddColumn<string>(
            name: "ContactPerson", table: "Customers",
            type: "nvarchar(150)", nullable: false, maxLength: 150,
            defaultValue: "");

        migrationBuilder.AddColumn<string>(
            name: "Telephone", table: "Customers",
            type: "nvarchar(30)", nullable: false, maxLength: 30,
            defaultValue: "");

        migrationBuilder.AddColumn<string>(
            name: "Remarks", table: "Customers",
            type: "nvarchar(1000)", nullable: false, maxLength: 1000,
            defaultValue: "");

        migrationBuilder.AddColumn<string>(
            name: "CompanyName", table: "Customers",
            type: "nvarchar(200)", nullable: false, maxLength: 200,
            defaultValue: "");

        migrationBuilder.AddColumn<string>(
            name: "Email", table: "Customers",
            type: "nvarchar(200)", nullable: false, maxLength: 200,
            defaultValue: "");

        migrationBuilder.AddColumn<string>(
            name: "TaxNumber", table: "Customers",
            type: "nvarchar(100)", nullable: false, maxLength: 100,
            defaultValue: "");

        migrationBuilder.AddColumn<decimal>(
            name: "OpeningBalance", table: "Customers",
            type: "decimal(18,3)", nullable: false,
            defaultValue: 0m);

        migrationBuilder.AddColumn<string>(
            name: "ContactPerson", table: "Suppliers",
            type: "nvarchar(150)", nullable: false, maxLength: 150,
            defaultValue: "");

        migrationBuilder.AddColumn<string>(
            name: "Telephone", table: "Suppliers",
            type: "nvarchar(30)", nullable: false, maxLength: 30,
            defaultValue: "");

        migrationBuilder.AddColumn<string>(
            name: "Remarks", table: "Suppliers",
            type: "nvarchar(1000)", nullable: false, maxLength: 1000,
            defaultValue: "");

        migrationBuilder.AddColumn<decimal>(
            name: "CreditLimit", table: "Suppliers",
            type: "decimal(18,3)", nullable: false,
            defaultValue: 0m);
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropColumn(name: "CreditLimit", table: "Suppliers");
        migrationBuilder.DropColumn(name: "Remarks", table: "Suppliers");
        migrationBuilder.DropColumn(name: "Telephone", table: "Suppliers");
        migrationBuilder.DropColumn(name: "ContactPerson", table: "Suppliers");
        migrationBuilder.DropColumn(name: "OpeningBalance", table: "Customers");
        migrationBuilder.DropColumn(name: "TaxNumber", table: "Customers");
        migrationBuilder.DropColumn(name: "Email", table: "Customers");
        migrationBuilder.DropColumn(name: "CompanyName", table: "Customers");
        migrationBuilder.DropColumn(name: "Remarks", table: "Customers");
        migrationBuilder.DropColumn(name: "Telephone", table: "Customers");
        migrationBuilder.DropColumn(name: "ContactPerson", table: "Customers");
    }
}
