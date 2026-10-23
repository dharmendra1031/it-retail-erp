import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_user_mobile"),
        ("companies", "0002_branch_warehouse"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="branch",
            field=models.ForeignKey(
                to="companies.branch",
                on_delete=django.db.models.deletion.PROTECT,
                null=True, blank=True,
            ),
        ),
    ]
