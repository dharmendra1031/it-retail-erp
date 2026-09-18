# Generated for the initial Company Master schema.

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("public_id", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name_en", models.CharField(max_length=200)),
                ("name_ar", models.CharField(blank=True, max_length=200)),
                ("address_en", models.CharField(blank=True, max_length=500)),
                ("address_ar", models.CharField(blank=True, max_length=500)),
                ("telephone", models.CharField(blank=True, max_length=30)),
                ("mobile", models.CharField(blank=True, max_length=30)),
                ("email", models.EmailField(blank=True, max_length=200)),
                ("website", models.URLField(blank=True, max_length=250)),
                ("tax_number", models.CharField(blank=True, db_index=True, max_length=100)),
                ("commercial_registration_number", models.CharField(blank=True, db_index=True, max_length=100)),
                ("logo", models.ImageField(blank=True, upload_to="company/")),
                ("bank_details", models.TextField(blank=True)),
                ("invoice_header", models.TextField(blank=True)),
                ("invoice_footer", models.TextField(blank=True)),
                ("terms_and_conditions", models.TextField(blank=True)),
                ("social_media", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name_plural": "Companies",
                "ordering": ("name_en",),
            },
        ),
    ]
