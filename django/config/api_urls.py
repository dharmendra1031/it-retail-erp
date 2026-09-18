from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.accounts.api import csrf, me, sign_in, sign_out
from apps.companies.api import CompanyViewSet

router = SimpleRouter(trailing_slash=False)
router.register("companies", CompanyViewSet, basename="company")

urlpatterns = [
    path("auth/csrf", csrf, name="api-csrf"),
    path("auth/me", me, name="api-me"),
    path("auth/login", sign_in, name="api-login"),
    path("auth/logout", sign_out, name="api-logout"),
    *router.urls,
]
