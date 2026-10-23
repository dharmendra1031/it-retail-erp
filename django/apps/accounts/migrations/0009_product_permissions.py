from django.db import migrations


def seed_permissions(apps, schema_editor):
    permission = apps.get_model("accounts", "AccessPermission")
    for action in ("view", "add", "edit", "delete"):
        permission.objects.get_or_create(
            code=f"products.{action}",
            defaults={"name": f"Products - {action.title()}"},
        )


class Migration(migrations.Migration):
    dependencies = [("accounts", "0008_catalog_permissions")]
    operations = [migrations.RunPython(seed_permissions, migrations.RunPython.noop)]
