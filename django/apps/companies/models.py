from django.db import models

from apps.core.models import TimeStampedModel


class Company(TimeStampedModel):
    name_en = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)

    address_en = models.CharField(max_length=500, blank=True)
    address_ar = models.CharField(max_length=500, blank=True)

    telephone = models.CharField(max_length=30, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    website = models.URLField(max_length=250, blank=True)

    tax_number = models.CharField(max_length=100, blank=True, db_index=True)
    commercial_registration_number = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
    )

    logo = models.ImageField(upload_to="company/", blank=True)
    bank_details = models.TextField(blank=True)
    invoice_header = models.TextField(blank=True)
    invoice_footer = models.TextField(blank=True)
    terms_and_conditions = models.TextField(blank=True)
    social_media = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ("name_en",)

    def __str__(self):
        return self.name_en


class Branch(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name="branches")
    code = models.CharField(max_length=30)
    name_en = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("company", "code"), name="uq_branch_company_code")
        ]

    def __str__(self):
        return self.name_en


class Warehouse(TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="warehouses")
    code = models.CharField(max_length=30)
    name_en = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("branch", "code"), name="uq_warehouse_branch_code")
        ]

    def __str__(self):
        return self.name_en
