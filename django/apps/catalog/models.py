from django.db import models

from apps.core.models import TimeStampedModel


class Category(TimeStampedModel):
    code = models.CharField(max_length=30)
    name_en = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="children"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("parent", "code"), condition=models.Q(parent__isnull=False),
                name="uq_category_sibling",
            ),
            models.UniqueConstraint(
                fields=("code",), condition=models.Q(parent__isnull=True),
                name="uq_category_root",
            ),
        ]


class Brand(TimeStampedModel):
    code = models.CharField(max_length=30, unique=True)
    name_en = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)


class Unit(TimeStampedModel):
    code = models.CharField(max_length=30, unique=True)
    name_en = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)
    decimal_places = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.CheckConstraint(
            condition=models.Q(decimal_places__gte=0, decimal_places__lte=6),
            name="ck_unit_decimal_places",
        )]


class Product(TimeStampedModel):
    TYPES = [("stock", "Stock"), ("nonstock", "Non-stock"), ("digital", "Digital")]

    sku = models.CharField(max_length=40, unique=True)
    barcode = models.CharField(max_length=64, null=True, blank=True, unique=True)
    name_en = models.CharField(max_length=200)
    name_ar = models.CharField(max_length=200, blank=True)
    description_en = models.CharField(max_length=1000, blank=True)
    description_ar = models.CharField(max_length=1000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, null=True, blank=True,
                              on_delete=models.PROTECT, related_name="products")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="products")
    product_type = models.CharField(max_length=20, choices=TYPES, default="stock")
    serial_tracked = models.BooleanField(default=False)
    cost_price = models.DecimalField(max_digits=18, decimal_places=3)
    base_price = models.DecimalField(max_digits=18, decimal_places=3)
    min_price = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    reorder_level = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    is_active = models.BooleanField(default=True)
