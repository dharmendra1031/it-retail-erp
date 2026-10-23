from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import AccessPermission, Role
from .permissions import catalog
from .serializers import RoleSerializer


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and (
            request.user.is_superuser or request.user.roles.filter(name__iexact="Admin").exists()
        ))


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all().order_by("name")
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "post", "put", "delete", "head", "options"]

    @action(detail=True, methods=["get", "put"], url_path="permissions")
    def role_permissions(self, request, pk=None):
        role = self.get_object()
        if request.method == "GET":
            return Response({"permissions": list(
                role.permissions.order_by("code").values_list("code", flat=True)
            )})

        if role.name.casefold() == "admin":
            return Response({"detail": "Admin role cannot be changed."}, status=400)

        codes = request.data.get("permissions")
        if not isinstance(codes, list) or any(not isinstance(code, str) for code in codes):
            return Response({"detail": "Invalid request."}, status=400)

        requested = set(codes)
        known = {entry["code"] for entry in catalog()}
        if not requested.issubset(known):
            return Response({"detail": "Invalid request."}, status=400)

        with transaction.atomic():
            permissions = list(AccessPermission.objects.filter(code__in=requested))
            if len(permissions) != len(requested):
                return Response({"detail": "Invalid request."}, status=400)
            role.permissions.set(permissions)
        return Response({"permissions": sorted(requested)})

    def update(self, request, *args, **kwargs):
        if self.get_object().name.casefold() == "admin":
            return Response({"detail": "Admin role cannot be changed."}, status=400)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        role = self.get_object()
        if role.name.casefold() == "admin":
            return Response({"detail": "Admin role cannot be deleted."}, status=400)
        if role.users.exists():
            return Response({"detail": "Role is assigned to users."}, status=status.HTTP_409_CONFLICT)
        return super().destroy(request, *args, **kwargs)
