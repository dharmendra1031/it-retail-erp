using ITRetailERP.Web.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace ITRetailERP.Web.Data;

public sealed class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
    : IdentityDbContext<ApplicationUser, IdentityRole<long>, long>(options)
{
    public DbSet<Company> Companies => Set<Company>();
    public DbSet<Category> Categories => Set<Category>();
    public DbSet<Product> Products => Set<Product>();
    public DbSet<Brand> Brands => Set<Brand>();
    public DbSet<Unit> Units => Set<Unit>();
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

        builder.Entity<Product>(entity =>
        {
            entity.HasIndex(x => x.Sku).IsUnique();
            entity.HasIndex(x => x.Barcode).IsUnique().HasFilter("[Barcode] IS NOT NULL");
            entity.Property(x => x.CostPrice).HasPrecision(18, 3);
            entity.Property(x => x.BasePrice).HasPrecision(18, 3);
            entity.Property(x => x.MinPrice).HasPrecision(18, 3);
            entity.Property(x => x.ReorderLevel).HasPrecision(18, 6);
            entity.HasOne<Category>().WithMany().HasForeignKey(x => x.CategoryId)
                .OnDelete(DeleteBehavior.Restrict);
            entity.HasOne<Brand>().WithMany().HasForeignKey(x => x.BrandId)
                .OnDelete(DeleteBehavior.Restrict);
            entity.HasOne<Unit>().WithMany().HasForeignKey(x => x.UnitId)
                .OnDelete(DeleteBehavior.Restrict);
        });

        builder.Entity<Category>(entity =>
        {
            entity.HasOne<Category>().WithMany()
                .HasForeignKey(x => x.ParentId).OnDelete(DeleteBehavior.Restrict);
            entity.HasIndex(x => new { x.ParentId, x.Code }).IsUnique()
                .HasFilter("[ParentId] IS NOT NULL");
            entity.HasIndex(x => x.Code).IsUnique()
                .HasDatabaseName("IX_Categories_RootCode")
                .HasFilter("[ParentId] IS NULL");
        });

        builder.Entity<Brand>(entity => entity.HasIndex(x => x.Code).IsUnique());
        builder.Entity<Unit>(entity => entity.HasIndex(x => x.Code).IsUnique());

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
