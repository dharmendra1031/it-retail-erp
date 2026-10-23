from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.accounts.api import csrf, me, sign_in, sign_out
from apps.accounts.roles_api import RoleViewSet
from apps.accounts.permissions_api import PermissionCatalogApi
from apps.accounts.users_api import UserViewSet
from apps.companies.api import CompanyViewSet
from apps.companies.organization_api import BranchViewSet, WarehouseViewSet
from apps.partners.api import CustomerViewSet, SupplierViewSet, download_document
from apps.catalog.api import CategoryViewSet, BrandViewSet, UnitViewSet, ProductViewSet

router = SimpleRouter(trailing_slash=False)
router.register("companies", CompanyViewSet, basename="company")
router.register("roles", RoleViewSet, basename="role")
router.register("users", UserViewSet, basename="user")
router.register("branches", BranchViewSet, basename="branch")
router.register("warehouses", WarehouseViewSet, basename="warehouse")
router.register("customers", CustomerViewSet, basename="customers")
router.register("suppliers", SupplierViewSet, basename="suppliers")
router.register("categories", CategoryViewSet, basename="categories")
router.register("brands", BrandViewSet, basename="brands")
router.register("units", UnitViewSet, basename="units")
router.register("products", ProductViewSet, basename="products")

urlpatterns = [
    path("auth/csrf", csrf, name="api-csrf"),
    path("auth/me", me, name="api-me"),
    path("auth/login", sign_in, name="api-login"),
    path("auth/logout", sign_out, name="api-logout"),
    path("permissions", PermissionCatalogApi.as_view(), name="api-permissions"),
    path("<str:kind>/<int:partner_id>/documents/<int:document_id>", download_document, name="partner-document"),
    *router.urls,
]
