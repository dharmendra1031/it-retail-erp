import django.db.models.deletion
from django.db import migrations, models


def common_fields():
    return [
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("created_at", models.DateTimeField(auto_now_add=True)),
        ("updated_at", models.DateTimeField(auto_now=True)),
        ("code", models.CharField(max_length=30)),
        ("name_en", models.CharField(max_length=200)),
        ("name_ar", models.CharField(max_length=200, blank=True)),
        ("is_active", models.BooleanField(default=True)),
    ]


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=common_fields() + [
                ("parent", models.ForeignKey(
                    null=True, blank=True, related_name="children",
                    on_delete=django.db.models.deletion.PROTECT, to="catalog.category",
                )),
            ],
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(fields=("parent", "code"),
                condition=models.Q(parent__isnull=False), name="uq_category_sibling"),
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(fields=("code",),
                condition=models.Q(parent__isnull=True), name="uq_category_root"),
        ),
        migrations.CreateModel(
            name="Brand",
            fields=[(key, models.CharField(max_length=30, unique=True)) if key == "code"
                    else (key, field) for key, field in common_fields()],
        ),
        migrations.CreateModel(
            name="Unit",
            fields=[(key, models.CharField(max_length=30, unique=True)) if key == "code"
                    else (key, field) for key, field in common_fields()] + [
                ("decimal_places", models.PositiveSmallIntegerField(default=0)),
            ],
        ),
    ]
