from django.db import migrations


PERMISSION_ACTIONS = {
    'companies': [
        'view',
        'add',
        'edit',
        'delete'
    ],
    'roles': [
        'view',
        'add',
        'edit',
        'delete'
    ],
    'users': [
        'view',
        'add',
        'edit',
        'delete'
    ],
    'branches': [
        'view',
        'add',
        'edit',
        'delete'
    ],
    'warehouses': [
        'view',
        'add',
        'edit',
        'delete'
    ],
    'quotations': [
        'view',
        'add',
        'edit',
        'delete',
        'print',
        'export',
        'approve',
        'cancel',
        'post',
        'reverse'
    ],
    'sales': [
        'view',
        'add',
        'edit',
        'delete',
        'print',
        'export',
        'approve',
        'cancel',
        'post',
        'reverse'
    ],
    'purchases': [
        'view',
        'add',
        'edit',
        'delete',
        'print',
        'export',
        'approve',
        'cancel',
        'post',
        'reverse'
    ],
    'inventory': [
        'view',
        'add',
        'edit',
        'delete',
        'print',
        'export',
        'approve',
        'cancel',
        'post',
        'reverse'
    ],
    'services': [
        'view',
        'add',
        'edit',
        'delete',
        'print',
        'export',
        'approve',
        'cancel',
        'post',
        'reverse'
    ],
    'reports': [
        'view',
        'print',
        'export'
    ]
}


def seed_catalog(apps, schema_editor):
    permission_model = apps.get_model("accounts", "AccessPermission")
    for module, actions in PERMISSION_ACTIONS.items():
        for action in actions:
            code = f"{module}.{action}"
            permission_model.objects.get_or_create(
                code=code, defaults={"name": f"{module.title()} - {action.title()}"}
            )


class Migration(migrations.Migration):
    dependencies = [("accounts", "0003_login_lockout")]
    operations = [migrations.RunPython(seed_catalog, migrations.RunPython.noop)]
