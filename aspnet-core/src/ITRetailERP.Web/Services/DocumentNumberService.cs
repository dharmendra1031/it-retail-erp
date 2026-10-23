using System.Text.RegularExpressions;
using ITRetailERP.Web.Data;
using ITRetailERP.Web.Models;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Services;

public sealed class DocumentNumberService(ApplicationDbContext db)
{
    public async Task<long> NextAsync(string series, int fiscalYear, long branchId = 0)
    {
        series = series.Trim().ToUpperInvariant();
        if (!Regex.IsMatch(series, @"\A[A-Z0-9_-]{1,20}\z") ||
            fiscalYear < 2000 || fiscalYear > 9999 || branchId < 0)
        {
            throw new ArgumentException("Invalid document number series, fiscal year or branch.");
        }

        await using var transaction = db.Database.CurrentTransaction is null
            ? await db.Database.BeginTransactionAsync()
            : null;
        var resource = $"erp:sequence:{series}:{fiscalYear}:{branchId}";
        await db.Database.ExecuteSqlInterpolatedAsync($"""
            DECLARE @result int;
            EXEC @result = sp_getapplock @Resource = {resource},
                 @LockMode = 'Exclusive', @LockOwner = 'Transaction', @LockTimeout = 10000;
            IF @result < 0 THROW 50001, 'Unable to lock document number series.', 1;
            """);

        var counter = await db.DocumentSequences.SingleOrDefaultAsync(x =>
            x.Series == series && x.FiscalYear == fiscalYear && x.BranchId == branchId);

        if (counter is null)
        {
            counter = new DocumentSequence
            {
                Series = series,
                FiscalYear = fiscalYear,
                BranchId = branchId,
            };
            db.DocumentSequences.Add(counter);
        }

        counter.LastNumber++;
        await db.SaveChangesAsync();
        if (transaction is not null)
        {
            await transaction.CommitAsync();
        }
        return counter.LastNumber;
    }
}
