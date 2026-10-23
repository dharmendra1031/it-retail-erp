using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Data;

public sealed class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
    : IdentityDbContext<ApplicationUser, IdentityRole<long>, long>(options)
{
    public DbSet<Company> Companies => Set<Company>();
    public DbSet<DocumentSequence> DocumentSequences => Set<DocumentSequence>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        builder.Entity<ApplicationUser>()
            .HasIndex(x => x.NormalizedEmail)
            .IsUnique()
            .HasDatabaseName("EmailIndex")
            .HasFilter("[NormalizedEmail] IS NOT NULL");

        builder.Entity<DocumentSequence>(entity =>
            entity.HasIndex(x => new { x.Series, x.FiscalYear, x.BranchId }).IsUnique());

        builder.Entity<Company>(entity =>
        {
            entity.HasIndex(x => x.TaxNumber);
            entity.HasIndex(x => x.CommercialRegistrationNumber);
        });
    }
}
