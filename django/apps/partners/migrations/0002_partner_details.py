from decimal import Decimal

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("partners", "0001_initial")]

    operations = [
        migrations.AddField(model_name="customer", name="contact_person",
                            field=models.CharField(max_length=150, blank=True, default=""),
                            preserve_default=False),
        migrations.AddField(model_name="customer", name="telephone",
                            field=models.CharField(max_length=30, blank=True, default=""),
                            preserve_default=False),
        migrations.AddField(model_name="customer", name="remarks",
                            field=models.CharField(max_length=1000, blank=True, default=""),
                            preserve_default=False),
        migrations.AddField(model_name="supplier", name="contact_person",
                            field=models.CharField(max_length=150, blank=True, default=""),
                            preserve_default=False),
        migrations.AddField(model_name="supplier", name="telephone",
                            field=models.CharField(max_length=30, blank=True, default=""),
                            preserve_default=False),
        migrations.AddField(model_name="supplier", name="remarks",
                            field=models.CharField(max_length=1000, blank=True, default=""),
                            preserve_default=False),
        migrations.AddField(model_name="customer", name="company_name",
                            field=models.CharField(max_length=200, blank=True, default=""), preserve_default=False),
        migrations.AddField(model_name="customer", name="email",
                            field=models.EmailField(max_length=200, blank=True, default=""), preserve_default=False),
        migrations.AddField(model_name="customer", name="tax_number",
                            field=models.CharField(max_length=100, blank=True, default=""), preserve_default=False),
        migrations.AddField(model_name="customer", name="opening_balance",
                            field=models.DecimalField(max_digits=18, decimal_places=3, default=Decimal("0.000"))),
        migrations.AddField(model_name="supplier", name="credit_limit",
                            field=models.DecimalField(max_digits=18, decimal_places=3, default=Decimal("0.000"))),
        migrations.AlterField(
            model_name="customer", name="customer_type",
            field=models.CharField(max_length=20, default="retail",
                choices=[(key, key.title()) for key in (
                    "retail", "wholesale", "corporate", "cash", "credit",
                    "individual", "company", "government", "other",
                )]),
        ),
    ]
