using ITRetailERP.Web.Data;
using ITRetailERP.Web.Services;
using Microsoft.EntityFrameworkCore;
using Xunit;

namespace ITRetailERP.Tests;

public sealed class DocumentNumberTests
{
    private static ApplicationDbContext OpenDatabase()
    {
        var connection = Environment.GetEnvironmentVariable("ConnectionStrings__DefaultConnection");
        Assert.False(string.IsNullOrWhiteSpace(connection), "Disposable SQL Server connection is required.");
        var options = new DbContextOptionsBuilder<ApplicationDbContext>()
            .UseSqlServer(connection)
            .Options;
        return new ApplicationDbContext(options);
    }

    [Fact]
    public async Task SequencesAreIncrementalAndScoped()
    {
        await using var db = OpenDatabase();
        var numbering = new DocumentNumberService(db);

        Assert.Equal(1, await numbering.NextAsync("TEST_PO", 2026, 1));
        Assert.Equal(2, await numbering.NextAsync("TEST_PO", 2026, 1));
        Assert.Equal(1, await numbering.NextAsync("TEST_PO", 2026, 2));
        Assert.Equal(1, await numbering.NextAsync("TEST_PO", 2027, 1));
        Assert.Equal(1, await numbering.NextAsync("TEST_INV", 2026, 1));
    }

    [Fact]
    public async Task ConcurrentRequestsGetDifferentNumbers()
    {
        var tasks = Enumerable.Range(0, 6).Select(async _ =>
        {
            await using var db = OpenDatabase();
            return await new DocumentNumberService(db).NextAsync("TEST_CONCURRENT", 2026, 1);
        });

        var actual = (await Task.WhenAll(tasks)).OrderBy(x => x).ToArray();
        Assert.Equal(new long[] { 1, 2, 3, 4, 5, 6 }, actual);
    }

    [Fact]
    public async Task InvalidSeriesDoesNotAllocate()
    {
        await using var db = OpenDatabase();
        var numbering = new DocumentNumberService(db);
        await Assert.ThrowsAsync<ArgumentException>(() => numbering.NextAsync("bad code!", 2026));
        await Assert.ThrowsAsync<ArgumentException>(() => numbering.NextAsync("TEST", 1999));
    }
}
