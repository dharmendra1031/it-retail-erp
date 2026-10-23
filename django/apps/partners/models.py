from decimal import Decimal

from django.db import models

from apps.core.models import TimeStampedModel


class PartnerBase(TimeStampedModel):
    code = models.CharField(max_length=30, unique=True)
    name_en = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)
    address_en = models.CharField(max_length=500, blank=True)
    address_ar = models.CharField(max_length=500, blank=True)
    mobile = models.CharField(max_length=30, blank=True)
    contact_person = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=30, blank=True)
    remarks = models.CharField(max_length=1000, blank=True)
    payment_terms_days = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Customer(PartnerBase):
    TYPES = [(kind, kind.title()) for kind in (
        "retail", "wholesale", "corporate", "cash", "credit",
        "individual", "company", "government", "other",
    )]
    civil_id = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    tax_number = models.CharField(max_length=100, blank=True)
    opening_balance = models.DecimalField(max_digits=18, decimal_places=3, default=Decimal("0.000"))
    customer_type = models.CharField(max_length=20, choices=TYPES, default="retail")
    credit_limit = models.DecimalField(max_digits=18, decimal_places=3, default=Decimal("0.000"))


class Supplier(PartnerBase):
    email = models.EmailField(max_length=200, blank=True)
    tax_number = models.CharField(max_length=100, blank=True)
    credit_limit = models.DecimalField(max_digits=18, decimal_places=3, default=Decimal("0.000"))
    opening_balance = models.DecimalField(max_digits=18, decimal_places=3, default=Decimal("0.000"))


class PartnerDocument(TimeStampedModel):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.PROTECT, related_name="documents")
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.PROTECT, related_name="documents")
    file_name = models.CharField(max_length=200)
    content_type = models.CharField(max_length=50)
    content = models.BinaryField()

    class Meta:
        constraints = [models.CheckConstraint(
            condition=models.Q(customer__isnull=False, supplier__isnull=True)
            | models.Q(customer__isnull=True, supplier__isnull=False),
            name="ck_partner_document_one_owner",
        )]
