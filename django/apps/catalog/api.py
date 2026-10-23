import re

from django.db.models import ProtectedError
from rest_framework import serializers
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.permissions import has_permission
from .models import Brand, Category, Unit


class CatalogPermission(BasePermission):
    ACTIONS = {"create": "add", "update": "edit", "destroy": "delete"}

    def has_permission(self, request, view):
        return has_permission(request.user, f"{view.basename}.{self.ACTIONS.get(view.action, 'view')}")


class NamedSerializer(serializers.ModelSerializer):
    nameEn = serializers.CharField(source="name_en", max_length=200)
    nameAr = serializers.CharField(source="name_ar", max_length=200, required=False, allow_blank=True)
    isActive = serializers.BooleanField(source="is_active", required=False)

    def validate_code(self, code):
        code = code.strip().upper()
        if not re.fullmatch(r"[A-Z0-9_-]{1,30}", code):
            raise serializers.ValidationError("Invalid code.")
        return code

    def validate_nameEn(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value.strip()


class CategorySerializer(NamedSerializer):
    parentId = serializers.PrimaryKeyRelatedField(
        source="parent", queryset=Category.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Category
        fields = ("id", "code", "nameEn", "nameAr", "parentId", "isActive")
        read_only_fields = ("id",)

    def validate(self, values):
        category = self.instance
        parent = values.get("parent", category.parent if category else None)
        code = values.get("code", category.code if category else None)
        if Category.objects.filter(parent=parent, code__iexact=code).exclude(
            pk=category.pk if category else None
        ).exists():
            raise serializers.ValidationError("Category code already exists.")
        node = parent
        while node is not None:
            if category and node.pk == category.pk:
                raise serializers.ValidationError("Category hierarchy cycle.")
            node = node.parent
        return values


class BrandSerializer(NamedSerializer):
    class Meta:
        model = Brand
        fields = ("id", "code", "nameEn", "nameAr", "isActive")
        read_only_fields = ("id",)

    def validate_code(self, code):
        code = super().validate_code(code)
        if Brand.objects.filter(code__iexact=code).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError("Brand code already exists.")
        return code


class UnitSerializer(NamedSerializer):
    decimalPlaces = serializers.IntegerField(
        source="decimal_places", min_value=0, max_value=6, required=False
    )

    class Meta:
        model = Unit
        fields = ("id", "code", "nameEn", "nameAr", "decimalPlaces", "isActive")
        read_only_fields = ("id",)

    def validate_code(self, code):
        code = super().validate_code(code)
        if Unit.objects.filter(code__iexact=code).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError("Unit code already exists.")
        return code


class CatalogViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, CatalogPermission]
    http_method_names = ["get", "post", "put", "delete", "head", "options"]

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.order_by("code")

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response({"detail": "Record is in use."}, status=409)


class CategoryViewSet(CatalogViewSet):
    serializer_class = CategorySerializer


class BrandViewSet(CatalogViewSet):
    serializer_class = BrandSerializer


class UnitViewSet(CatalogViewSet):
    serializer_class = UnitSerializer
