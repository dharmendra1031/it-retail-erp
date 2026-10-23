from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("accounts", "0004_permission_catalog")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="mobile",
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
