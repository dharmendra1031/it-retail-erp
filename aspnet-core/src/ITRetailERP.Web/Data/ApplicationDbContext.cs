using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Data;

public sealed class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
    : IdentityDbContext<ApplicationUser, IdentityRole<long>, long>(options)
{
    public DbSet<Company> Companies => Set<Company>();
    public DbSet<Customer> Customers => Set<Customer>();
    public DbSet<Supplier> Suppliers => Set<Supplier>();
    public DbSet<PartnerDocument> PartnerDocuments => Set<PartnerDocument>();
    public DbSet<Branch> Branches => Set<Branch>();
    public DbSet<Warehouse> Warehouses => Set<Warehouse>();
    public DbSet<DocumentSequence> DocumentSequences => Set<DocumentSequence>();

    protected override void OnModelCreating(ModelBuilder builder)
    {
        base.OnModelCreating(builder);

        builder.Entity<ApplicationUser>()
            .HasOne<Branch>().WithMany()
            .HasForeignKey(x => x.BranchId).OnDelete(DeleteBehavior.Restrict);

        builder.Entity<Branch>(entity =>
        {
            entity.HasIndex(x => new { x.CompanyId, x.Code }).IsUnique();
            entity.HasOne<Company>().WithMany().HasForeignKey(x => x.CompanyId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        builder.Entity<Warehouse>(entity =>
        {
            entity.HasIndex(x => new { x.BranchId, x.Code }).IsUnique();
            entity.HasOne<Branch>().WithMany().HasForeignKey(x => x.BranchId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        builder.Entity<ApplicationUser>()
            .HasIndex(x => x.NormalizedEmail)
            .IsUnique()
            .HasDatabaseName("EmailIndex")
            .HasFilter("[NormalizedEmail] IS NOT NULL");

        builder.Entity<DocumentSequence>(entity =>
            entity.HasIndex(x => new { x.Series, x.FiscalYear, x.BranchId }).IsUnique());

        builder.Entity<Customer>(entity =>
        {
            entity.HasIndex(x => x.Code).IsUnique();
            entity.Property(x => x.CreditLimit).HasPrecision(18, 3);
        });

        builder.Entity<Supplier>(entity =>
        {
            entity.HasIndex(x => x.Code).IsUnique();
            entity.Property(x => x.OpeningBalance).HasPrecision(18, 3);
        });

        builder.Entity<PartnerDocument>(entity =>
        {
            entity.HasOne<Customer>().WithMany().HasForeignKey(x => x.CustomerId)
                .OnDelete(DeleteBehavior.Restrict);
            entity.HasOne<Supplier>().WithMany().HasForeignKey(x => x.SupplierId)
                .OnDelete(DeleteBehavior.Restrict);
            entity.ToTable(table => table.HasCheckConstraint(
                "CK_PartnerDocuments_OneOwner",
                "([CustomerId] IS NOT NULL AND [SupplierId] IS NULL) OR ([CustomerId] IS NULL AND [SupplierId] IS NOT NULL)"));
        });

        builder.Entity<Company>(entity =>
        {
            entity.HasIndex(x => x.TaxNumber);
            entity.HasIndex(x => x.CommercialRegistrationNumber);
        });
    }
}
