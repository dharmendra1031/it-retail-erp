using System.ComponentModel.DataAnnotations;
using ITRetailERP.Web.Contracts;
using Xunit;

namespace ITRetailERP.Tests;

public sealed class LocalizationContractTests
{
    [Fact]
    public void CompanyContractAcceptsArabicAndEnforcesLength()
    {
        var request = new CompanyRequest
        {
            NameEn = "Retail",
            NameAr = "مُعَدّات الحاسوب",
            AddressAr = "الكويت — شارع ١٢",
        };
        var context = new ValidationContext(request);

        Assert.True(Validator.TryValidateObject(request, context, new List<ValidationResult>(), true));

        request.NameAr = new string('س', 201);
        Assert.False(Validator.TryValidateObject(request, context, new List<ValidationResult>(), true));
    }

    [Fact]
    public void PartnerCodesAndMoneyRemainLocaleIndependent()
    {
        var request = new CustomerRequest
        {
            Code = "C-001",
            NameEn = "Retail",
            CustomerType = "corporate",
            PaymentTermsDays = 30,
        };

        Assert.True(PartnerValidation.IsValid(request));
        request.Code = "رمز-١";
        Assert.False(PartnerValidation.IsValid(request));

        Assert.True(PartnerValidation.Amount(1234.375m));
        Assert.False(PartnerValidation.Amount(1234.3751m));
        Assert.Equal("1234.375", PartnerValidation.Money(1234.375m));
    }
}
