from rest_framework.permissions import BasePermission

from .models import AccessPermission


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


def catalog():
    return [
        {"code": f"{module}.{action}", "name": f"{module.title()} - {action.title()}"}
        for module, actions in PERMISSION_ACTIONS.items()
        for action in actions
    ]


def has_permission(user, code):
    if not user.is_authenticated or not user.is_active:
        return False
    return (
        user.is_superuser
        or user.roles.filter(name__iexact="Admin").exists()
        or user.roles.filter(permissions__code=code).exists()
    )


class CanManageCompanies(BasePermission):
    ACTIONS = {"create": "add", "update": "edit", "partial_update": "edit", "destroy": "delete"}

    def has_permission(self, request, view):
        action = self.ACTIONS.get(view.action)
        return action is None or has_permission(request.user, f"companies.{action}")
