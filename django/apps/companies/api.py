from django.core.files.storage import default_storage
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from apps.accounts.roles_api import IsAdminUser

from .models import Company
from .serializers import CompanySerializer


class CanManageCompanies(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or IsAdminUser().has_permission(request, view)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all().order_by("name_en")
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, CanManageCompanies]
    parser_classes = [MultiPartParser, FormParser]

    def perform_destroy(self, instance):
        logo_name = instance.logo.name if instance.logo else ""
        super().perform_destroy(instance)

        if logo_name:
            default_storage.delete(logo_name)
