import decimal

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sku", models.CharField(max_length=40, unique=True)),
                ("barcode", models.CharField(max_length=64, null=True, blank=True, unique=True)),
                ("name_en", models.CharField(max_length=200)),
                ("name_ar", models.CharField(max_length=200, blank=True)),
                ("description_en", models.CharField(max_length=1000, blank=True)),
                ("description_ar", models.CharField(max_length=1000, blank=True)),
                ("product_type", models.CharField(max_length=20, choices=[
                    ("stock", "Stock"), ("nonstock", "Non-stock"), ("digital", "Digital")
                ], default="stock")),
                ("serial_tracked", models.BooleanField(default=False)),
                ("cost_price", models.DecimalField(max_digits=18, decimal_places=3)),
                ("base_price", models.DecimalField(max_digits=18, decimal_places=3)),
                ("min_price", models.DecimalField(max_digits=18, decimal_places=3,
                    default=decimal.Decimal("0"))),
                ("reorder_level", models.DecimalField(max_digits=18, decimal_places=6,
                    default=decimal.Decimal("0"))),
                ("is_active", models.BooleanField(default=True)),
                ("category", models.ForeignKey(to="catalog.category", related_name="products",
                    on_delete=django.db.models.deletion.PROTECT)),
                ("brand", models.ForeignKey(to="catalog.brand", null=True, blank=True,
                    related_name="products", on_delete=django.db.models.deletion.PROTECT)),
                ("unit", models.ForeignKey(to="catalog.unit", related_name="products",
                    on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
