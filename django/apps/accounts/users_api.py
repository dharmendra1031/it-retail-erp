from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import Role, User
from .roles_api import IsAdminUser


def user_response(user):
    return {
        "id": user.pk,
        "username": user.username,
        "fullName": user.first_name,
        "email": user.email,
        "mobile": user.mobile,
        "isActive": user.is_active,
        "roleIds": sorted(user.roles.values_list("id", flat=True)),
    }


class UserViewSet(ViewSet):
    permission_classes = [IsAdminUser]

    def list(self, request):
        return Response([
            user_response(user)
            for user in User.objects.prefetch_related("roles").order_by("username")
        ])

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except (User.DoesNotExist, ValueError):
            return Response(status=404)
        return Response(user_response(user))

    def _validate(self, data, *, existing=None):
        username = data.get("username")
        email = data.get("email")
        name = data.get("fullName")
        mobile = data.get("mobile", "")
        role_ids = data.get("roleIds", [])
        active = data.get("isActive", True)
        password = data.get("password")
        if (not isinstance(username, str) or not 1 <= len(username.strip()) <= 150
            or not isinstance(email, str) or "@" not in email or len(email) > 254
            or not isinstance(name, str) or len(name.strip()) > 150
            or not isinstance(mobile, str) or len(mobile) > 30
            or not isinstance(role_ids, list) or not all(
                isinstance(role_id, int) and not isinstance(role_id, bool) and role_id > 0
                for role_id in role_ids
            )
            or not isinstance(active, bool)
            or (existing is None and not isinstance(password, str))):
            return None
        role_ids = set(role_ids)
        if Role.objects.filter(pk__in=role_ids).count() != len(role_ids):
            return None
        if existing is None:
            try:
                validate_password(password)
            except ValidationError:
                return None
        return username.strip(), email.strip().lower(), name.strip(), mobile.strip(), active, role_ids, password

    def create(self, request):
        values = self._validate(request.data)
        if values is None:
            return Response({"detail": "Invalid request."}, status=400)
        username, email, name, mobile, active, role_ids, password = values
        if User.objects.filter(username__iexact=username).exists() or User.objects.filter(email__iexact=email).exists():
            return Response({"detail": "User already exists."}, status=400)

        with transaction.atomic():
            user = User.objects.create_user(
                username=username, email=email, password=password,
                first_name=name, mobile=mobile, is_active=active,
            )
            user.roles.set(role_ids)
        return Response(user_response(user), status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except (User.DoesNotExist, ValueError):
            return Response(status=404)
        values = self._validate(request.data, existing=user)
        if values is None:
            return Response({"detail": "Invalid request."}, status=400)
        username, email, name, mobile, active, role_ids, _ = values
        if (User.objects.exclude(pk=pk).filter(username__iexact=username).exists()
            or User.objects.exclude(pk=pk).filter(email__iexact=email).exists()):
            return Response({"detail": "User already exists."}, status=400)
        if user.pk == request.user.pk and (not active or not role_ids.intersection(
            Role.objects.filter(name__iexact="Admin").values_list("id", flat=True)
        )):
            return Response({"detail": "Cannot remove your own administrator access."}, status=400)

        with transaction.atomic():
            user.username, user.email, user.first_name = username, email, name
            user.mobile, user.is_active = mobile, active
            user.save(update_fields=["username", "email", "first_name", "mobile", "is_active"])
            user.roles.set(role_ids)
        return Response(user_response(user))

    @action(detail=True, methods=["put"], url_path="password")
    def password(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except (User.DoesNotExist, ValueError):
            return Response(status=404)
        password = request.data.get("password")
        if not isinstance(password, str):
            return Response({"detail": "Invalid request."}, status=400)
        try:
            validate_password(password, user)
        except ValidationError:
            return Response({"detail": "Invalid request."}, status=400)
        user.set_password(password)
        user.save(update_fields=["password"])
        return Response(status=204)
