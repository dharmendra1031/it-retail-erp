import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("catalog", "0004_product_type_stock_settings")]

    operations = [
        migrations.CreateModel(
            name="ProductLicense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True,
                                            serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("license_number", models.CharField(blank=True, max_length=100)),
                ("encrypted_key", models.BinaryField(blank=True, null=True)),
                ("key_fingerprint", models.BinaryField(blank=True, max_length=32, null=True)),
                ("activation_date", models.DateField(blank=True, null=True)),
                ("expiry_date", models.DateField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                              related_name="licenses", to="catalog.product")),
            ],
        ),
        migrations.AddConstraint(
            model_name="productlicense",
            constraint=models.UniqueConstraint(
                fields=("key_fingerprint",),
                condition=models.Q(is_active=True, key_fingerprint__isnull=False),
                name="uq_active_product_license_key",
            ),
        ),
        migrations.AddConstraint(
            model_name="productlicense",
            constraint=models.CheckConstraint(
                condition=(
                    (models.Q(encrypted_key__isnull=False) | ~models.Q(license_number="")) &
                    (models.Q(activation_date__isnull=True) |
                     models.Q(expiry_date__isnull=True) |
                     models.Q(expiry_date__gte=models.F("activation_date"))) &
                    ((models.Q(encrypted_key__isnull=True) & models.Q(key_fingerprint__isnull=True)) |
                     (models.Q(encrypted_key__isnull=False) & models.Q(key_fingerprint__isnull=False)))
                ),
                name="ck_product_license_dates_identity",
            ),
        ),
    ]
