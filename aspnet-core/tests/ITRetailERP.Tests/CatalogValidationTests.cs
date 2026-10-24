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
