from django.db import migrations


def seed_permissions(apps, schema_editor):
    permission = apps.get_model("accounts", "AccessPermission")
    for module in ("customers", "suppliers"):
        for action in ("view", "add", "edit", "delete"):
            permission.objects.get_or_create(
                code=f"{module}.{action}",
                defaults={"name": f"{module.title()} - {action.title()}"},
            )


class Migration(migrations.Migration):
    dependencies = [("accounts", "0006_user_branch")]
    operations = [migrations.RunPython(seed_permissions, migrations.RunPython.noop)]
