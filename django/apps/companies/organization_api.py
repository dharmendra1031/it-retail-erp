from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers

from apps.accounts.roles_api import IsAdminUser
from .models import Branch, Company, Warehouse


class AdminWritePermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in ("GET", "HEAD", "OPTIONS") or IsAdminUser().has_permission(request, view)


class BranchSerializer(serializers.ModelSerializer):
    companyId = serializers.PrimaryKeyRelatedField(
        source="company", queryset=Company.objects.all()
    )
    nameEn = serializers.CharField(source="name_en", max_length=200)
    nameAr = serializers.CharField(source="name_ar", max_length=200, allow_blank=True, required=False)
    isActive = serializers.BooleanField(source="is_active", required=False)

    class Meta:
        model = Branch
        fields = ("id", "companyId", "code", "nameEn", "nameAr", "isActive")
        read_only_fields = ("id",)

    def validate_code(self, value):
        value = value.strip().upper()
        if not value or len(value) > 30:
            raise serializers.ValidationError("Invalid branch code.")
        return value

    def validate(self, values):
        company = values.get("company", getattr(self.instance, "company", None))
        code = values.get("code", getattr(self.instance, "code", None))
        if Branch.objects.filter(company=company, code__iexact=code).exclude(
            pk=getattr(self.instance, "pk", None)
        ).exists():
            raise serializers.ValidationError("Branch code already exists.")
        return values


class WarehouseSerializer(serializers.ModelSerializer):
    branchId = serializers.PrimaryKeyRelatedField(source="branch", queryset=Branch.objects.all())
    nameEn = serializers.CharField(source="name_en", max_length=200)
    nameAr = serializers.CharField(source="name_ar", max_length=200, allow_blank=True, required=False)
    isActive = serializers.BooleanField(source="is_active", required=False)

    class Meta:
        model = Warehouse
        fields = ("id", "branchId", "code", "nameEn", "nameAr", "isActive")
        read_only_fields = ("id",)

    def validate_code(self, value):
        value = value.strip().upper()
        if not value or len(value) > 30:
            raise serializers.ValidationError("Invalid warehouse code.")
        return value

    def validate(self, values):
        branch = values.get("branch", getattr(self.instance, "branch", None))
        code = values.get("code", getattr(self.instance, "code", None))
        if Warehouse.objects.filter(branch=branch, code__iexact=code).exclude(
            pk=getattr(self.instance, "pk", None)
        ).exists():
            raise serializers.ValidationError("Warehouse code already exists.")
        return values


class BranchViewSet(ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, AdminWritePermission]
    http_method_names = ["get", "post", "put", "delete", "head", "options"]

    def get_queryset(self):
        queryset = Branch.objects.all().order_by("code")
        if IsAdminUser().has_permission(self.request, self):
            return queryset
        return queryset.filter(id=self.request.user.branch_id)

    def destroy(self, request, *args, **kwargs):
        branch = self.get_object()
        if branch.warehouses.exists() or branch.user_set.exists():
            return Response({"detail": "Branch is in use."}, status=409)
        return super().destroy(request, *args, **kwargs)


class WarehouseViewSet(ModelViewSet):
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, AdminWritePermission]
    http_method_names = ["get", "post", "put", "delete", "head", "options"]

    def get_queryset(self):
        queryset = Warehouse.objects.all().order_by("code")
        if IsAdminUser().has_permission(self.request, self):
            return queryset
        return queryset.filter(branch_id=self.request.user.branch_id)
