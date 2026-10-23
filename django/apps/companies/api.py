from django.core.files.storage import default_storage
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.accounts.permissions import CanManageCompanies

from .models import Company
from .serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all().order_by("name_en")
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, CanManageCompanies]
    parser_classes = [MultiPartParser, FormParser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.branches.exists():
            return Response({"detail": "Company has assigned branches."}, status=409)
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        logo_name = instance.logo.name if instance.logo else ""
        super().perform_destroy(instance)

        if logo_name:
            default_storage.delete(logo_name)
