from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("catalog", "0003_unit_precision_check")]

    operations = [
        migrations.AddConstraint(
            model_name="product",
            constraint=models.CheckConstraint(
                condition=(models.Q(product_type="stock") |
                           models.Q(product_type__in=("nonstock", "digital"),
                                    serial_tracked=False, reorder_level=0)),
                name="ck_product_type_stock_settings",
            ),
        ),
    ]
