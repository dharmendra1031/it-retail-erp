from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.middleware.csrf import get_token
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .authentication import ApiSessionAuthentication
from .models import User


def _user_response(user):
    return {
        "id": user.id,
        "name": user.get_full_name() or user.email,
        "email": user.email,
        "isAdmin": user.is_superuser or user.roles.filter(name__iexact="Admin").exists(),
    }


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    return Response({"csrfToken": get_token(request)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(_user_response(request.user))


@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):
    ApiSessionAuthentication().enforce_csrf(request)
    email = str(request.data.get("email", "")).strip()
    password = str(request.data.get("password", ""))
    remember_me = request.data.get("rememberMe", False)
    if not email or not password or not isinstance(remember_me, bool):
        return Response({"detail": "Invalid request."}, status=400)

    with transaction.atomic():
        record = User.objects.select_for_update().filter(email__iexact=email).first()
        if record is None:
            return Response(status=401)

        now = timezone.now()
        if record.locked_until and record.locked_until > now:
            return Response(status=401)

        user = authenticate(request, username=record.username, password=password)
        if user is None:
            attempts = record.failed_login_attempts + 1
            record.failed_login_attempts = min(attempts, 5)
            if attempts >= 5:
                record.locked_until = now + timedelta(minutes=15)
            record.save(update_fields=["failed_login_attempts", "locked_until"])
            return Response(status=401)

        if record.failed_login_attempts or record.locked_until:
            record.failed_login_attempts = 0
            record.locked_until = None
            record.save(update_fields=["failed_login_attempts", "locked_until"])

    login(request, user)
    request.session.set_expiry(30 * 60 if remember_me else 0)
    return Response(_user_response(user))


@csrf_protect
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sign_out(request):
    ApiSessionAuthentication().enforce_csrf(request)
    logout(request)
    return Response(status=204)
