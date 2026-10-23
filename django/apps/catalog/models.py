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
