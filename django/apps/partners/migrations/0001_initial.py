import decimal
import django.db.models.deletion
from django.db import migrations, models


def common_fields():
    return [
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("created_at", models.DateTimeField(auto_now_add=True)),
        ("updated_at", models.DateTimeField(auto_now=True)),
        ("code", models.CharField(max_length=30, unique=True)),
        ("name_en", models.CharField(max_length=200)),
        ("name_ar", models.CharField(max_length=200, blank=True)),
        ("address_en", models.CharField(max_length=500, blank=True)),
        ("address_ar", models.CharField(max_length=500, blank=True)),
        ("mobile", models.CharField(max_length=30, blank=True)),
        ("payment_terms_days", models.PositiveSmallIntegerField(default=0)),
        ("is_active", models.BooleanField(default=True)),
    ]


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=common_fields() + [
                ("civil_id", models.CharField(max_length=30, blank=True)),
                ("customer_type", models.CharField(max_length=20, choices=[
                    ("retail", "Retail"), ("wholesale", "Wholesale"), ("corporate", "Corporate")
                ], default="retail")),
                ("credit_limit", models.DecimalField(max_digits=18, decimal_places=3,
                    default=decimal.Decimal("0.000"))),
            ],
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=common_fields() + [
                ("email", models.EmailField(max_length=200, blank=True)),
                ("tax_number", models.CharField(max_length=100, blank=True)),
                ("opening_balance", models.DecimalField(max_digits=18, decimal_places=3,
                    default=decimal.Decimal("0.000"))),
            ],
        ),
        migrations.CreateModel(
            name="PartnerDocument",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("file_name", models.CharField(max_length=200)),
                ("content_type", models.CharField(max_length=50)),
                ("content", models.BinaryField()),
                ("customer", models.ForeignKey(null=True, blank=True, related_name="documents",
                    on_delete=django.db.models.deletion.PROTECT, to="partners.customer")),
                ("supplier", models.ForeignKey(null=True, blank=True, related_name="documents",
                    on_delete=django.db.models.deletion.PROTECT, to="partners.supplier")),
            ],
        ),
        migrations.AddConstraint(
            model_name="partnerdocument",
            constraint=models.CheckConstraint(
                condition=models.Q(customer__isnull=False, supplier__isnull=True)
                | models.Q(customer__isnull=True, supplier__isnull=False),
                name="ck_partner_document_one_owner",
            ),
        ),
    ]
