from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User


def _user_response(user):
    return {
        "id": user.id,
        "name": user.get_full_name() or user.email,
        "email": user.email,
    }


@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    return Response({"csrfToken": get_token(request)})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(_user_response(request.user))


@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):
    email = str(request.data.get("email", "")).strip()
    password = str(request.data.get("password", ""))
    remember_me = bool(request.data.get("rememberMe", False))

    user_record = User.objects.filter(email__iexact=email).only("username").first()
    if user_record is None:
        return Response(status=401)

    user = authenticate(request, username=user_record.username, password=password)
    if user is None:
        return Response(status=401)

    login(request, user)

    if not remember_me:
        request.session.set_expiry(0)

    return Response(_user_response(user))


@csrf_protect
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sign_out(request):
    logout(request)
    return Response(status=204)
