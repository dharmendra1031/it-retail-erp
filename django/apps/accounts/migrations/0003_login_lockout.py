from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("accounts", "0002_admin_role")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="failed_login_attempts",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="locked_until",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
