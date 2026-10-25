from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("catalog", "0002_product")]

    operations = [
        migrations.AddConstraint(
            model_name="unit",
            constraint=models.CheckConstraint(
                condition=models.Q(decimal_places__gte=0, decimal_places__lte=6),
                name="ck_unit_decimal_places",
            ),
        ),
    ]
