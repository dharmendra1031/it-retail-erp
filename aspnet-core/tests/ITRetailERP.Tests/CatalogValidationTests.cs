using System.ComponentModel.DataAnnotations;
using ITRetailERP.Web.Contracts;
using Xunit;

namespace ITRetailERP.Tests;

public sealed class CatalogValidationTests
{
    [Fact]
    public void CodesAreNormalizedAndRejectNonAsciiIdentifiers()
    {
        var unit = new UnitRequest
        {
            Code = " pcs ",
            NameEn = "Pieces",
            NameAr = "قطعة",
            DecimalPlaces = 0,
        };

        Assert.Equal("PCS", CatalogValidation.Code(unit));

        unit.Code = "وحدة";
        Assert.Null(CatalogValidation.Code(unit));
        unit.Code = "bad space";
        Assert.Null(CatalogValidation.Code(unit));
    }

    [Fact]
    public void CategoriesNormalizeCodeAndRejectBlankNames()
    {
        var category = new CategoryRequest
        {
            Code = " ssd ",
            NameEn = "Solid State Drives",
            NameAr = "أقراص الحالة الصلبة",
        };

        Assert.Equal("SSD", CatalogValidation.Code(category));

        category.NameEn = "   ";
        Assert.Null(CatalogValidation.Code(category));
    }

    [Fact]
    public void UnitsAcceptMaximumSupportedPrecision()
    {
        var unit = new UnitRequest { Code = "KG", NameEn = "Kilogram", DecimalPlaces = 6 };
        var errors = new List<ValidationResult>();
        Assert.True(Validator.TryValidateObject(unit, new ValidationContext(unit), errors, true));
        Assert.Equal("KG", CatalogValidation.Code(unit));
    }

    [Theory]
    [InlineData(-1)]
    [InlineData(7)]
    public void UnitsRejectPrecisionOutsideSupportedRange(int precision)
    {
        var unit = new UnitRequest
        {
            Code = "PCS",
            NameEn = "Pieces",
            DecimalPlaces = precision,
        };
        var errors = new List<ValidationResult>();

        Assert.False(Validator.TryValidateObject(
            unit, new ValidationContext(unit), errors, true));
        Assert.NotEmpty(errors);
    }
}
