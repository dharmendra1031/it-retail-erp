from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Role
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
