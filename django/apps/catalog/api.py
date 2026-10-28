import re
import unicodedata
from decimal import Decimal

from django.db import IntegrityError, transaction
from django.db.models import ProtectedError, Q
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.permissions import has_permission
from .license_crypto import decrypt as decrypt_license_key
from .license_crypto import encrypt as encrypt_license_key
from .license_crypto import fingerprint as license_fingerprint
from .models import Brand, Category, Unit, Product, ProductLicense


class CatalogPermission(BasePermission):
    ACTIONS = {"create": "add", "update": "edit", "destroy": "delete"}

    def has_permission(self, request, view):
        return has_permission(request.user, f"{view.basename}.{self.ACTIONS.get(view.action, 'view')}")


class NamedSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=30)
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
        validators = []  # Sibling/root uniqueness is checked against the resolved parent.

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


PRODUCT_DUPLICATE_ERROR = "SKU or barcode already exists."


class CatalogViewSet(ModelViewSet):
    def integrity_detail(self, error):
        message = str(error)
        if self.basename == "products" and (
            "UNIQUE constraint failed" in message
            or re.search(r"\((?:2601|2627)\)", message)
        ):
            return PRODUCT_DUPLICATE_ERROR
        return "Invalid request."

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().create(request, *args, **kwargs)
        except IntegrityError as error:
            return Response({"detail": self.integrity_detail(error)}, status=400)

    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().update(request, *args, **kwargs)
        except IntegrityError as error:
            return Response({"detail": self.integrity_detail(error)}, status=400)

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

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) | Q(name_en__icontains=search) | Q(name_ar__icontains=search)
            )
        return queryset


class BrandViewSet(CatalogViewSet):
    serializer_class = BrandSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) | Q(name_en__icontains=search) |
                Q(name_ar__icontains=search)
            )
        return queryset


class UnitViewSet(CatalogViewSet):
    serializer_class = UnitSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) | Q(name_en__icontains=search) |
                Q(name_ar__icontains=search)
            )
        return queryset


class ProductSerializer(serializers.ModelSerializer):
    nameEn = serializers.CharField(source="name_en", max_length=200)
    nameAr = serializers.CharField(source="name_ar", max_length=200, required=False, allow_blank=True)
    descriptionEn = serializers.CharField(source="description_en", max_length=1000, required=False, allow_blank=True)
    descriptionAr = serializers.CharField(source="description_ar", max_length=1000, required=False, allow_blank=True)
    categoryId = serializers.PrimaryKeyRelatedField(source="category", queryset=Category.objects.filter(is_active=True))
    brandId = serializers.PrimaryKeyRelatedField(source="brand", queryset=Brand.objects.filter(is_active=True),
                                                 required=False, allow_null=True)
    unitId = serializers.PrimaryKeyRelatedField(source="unit", queryset=Unit.objects.filter(is_active=True))
    productType = serializers.ChoiceField(source="product_type", choices=[value for value, _ in Product.TYPES])
    serialTracked = serializers.BooleanField(source="serial_tracked", required=False)
    costPrice = serializers.DecimalField(source="cost_price", max_digits=18, decimal_places=3, min_value=0)
    basePrice = serializers.DecimalField(source="base_price", max_digits=18, decimal_places=3, min_value=0)
    minPrice = serializers.DecimalField(source="min_price", max_digits=18, decimal_places=3, min_value=0,
                                        required=False)
    reorderLevel = serializers.DecimalField(source="reorder_level", max_digits=18, decimal_places=6,
                                             min_value=0, required=False)
    isActive = serializers.BooleanField(source="is_active", required=False)

    class Meta:
        model = Product
        fields = ("id", "sku", "barcode", "nameEn", "nameAr", "descriptionEn", "descriptionAr",
                  "categoryId", "brandId", "unitId", "productType", "serialTracked",
                  "costPrice", "basePrice", "minPrice", "reorderLevel", "isActive")
        read_only_fields = ("id",)
        extra_kwargs = {"barcode": {"required": False, "allow_blank": True, "allow_null": True, "validators": []},
                        "sku": {"validators": []}}

    def validate_sku(self, value):
        sku = value.strip().upper()
        if not re.fullmatch(r"[A-Z0-9_-]{1,40}", sku):
            raise serializers.ValidationError("Invalid SKU.")
        if Product.objects.filter(sku__iexact=sku).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError(PRODUCT_DUPLICATE_ERROR)
        return sku

    def validate_barcode(self, value):
        value = value.strip().upper() if value else None
        if value and not re.fullmatch(r"[A-Z0-9_-]{3,64}", value):
            raise serializers.ValidationError("Invalid barcode.")
        if value and Product.objects.filter(barcode__iexact=value).exclude(
            pk=self.instance.pk if self.instance else None
        ).exists():
            raise serializers.ValidationError(PRODUCT_DUPLICATE_ERROR)
        return value

    def validate_nameEn(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value.strip()

    def validate(self, values):
        product = self.instance
        kind = values.get("product_type", product.product_type if product else "stock")
        serial = values.get("serial_tracked", product.serial_tracked if product else False)
        reorder = values.get("reorder_level", product.reorder_level if product else Decimal("0"))
        base = values.get("base_price", product.base_price if product else None)
        minimum = values.get("min_price", product.min_price if product else Decimal("0"))
        if kind != "stock" and (serial or reorder):
            raise serializers.ValidationError("Non-stock or digital products cannot hold stock settings.")
        if base is not None and minimum > base:
            raise serializers.ValidationError("Minimum price exceeds selling price.")
        if product and product.product_type == "digital" and kind != "digital" and product.licenses.exists():
            raise serializers.ValidationError("Product with licenses must remain digital.")
        return values


class ProductViewSet(CatalogViewSet):
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        if "page" not in request.query_params and "pageSize" not in request.query_params:
            return super().list(request, *args, **kwargs)
        try:
            page = int(request.query_params.get("page", "1"))
            size = int(request.query_params.get("pageSize", "25"))
        except ValueError:
            return Response({"detail": "Invalid request."}, status=400)
        if page < 1 or not 1 <= size <= 100 or (page - 1) * size > 2147483647:
            return Response({"detail": "Invalid request."}, status=400)

        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.count()
        products = queryset[(page - 1) * size:page * size]
        return Response({
            "items": self.get_serializer(products, many=True).data,
            "total": total, "page": page, "pageSize": size,
        })

    def get_queryset(self):
        queryset = Product.objects.select_related("category", "brand", "unit").order_by("sku")
        search = self.request.query_params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(sku__icontains=search) | Q(barcode__icontains=search) |
                Q(name_en__icontains=search) | Q(name_ar__icontains=search)
            )
        return queryset


class ProductLicensePermission(BasePermission):
    ACTIONS = {"create": "add", "destroy": "revoke", "reveal": "reveal"}

    def has_permission(self, request, view):
        return has_permission(request.user, f"product-licenses.{self.ACTIONS.get(view.action, 'view')}")


class ProductLicenseSerializer(serializers.ModelSerializer):
    productId = serializers.PrimaryKeyRelatedField(
        source="product", queryset=Product.objects.filter(product_type="digital", is_active=True)
    )
    licenseNumber = serializers.CharField(source="license_number", max_length=100,
                                          required=False, allow_blank=True)
    licenseKey = serializers.CharField(write_only=True, max_length=512,
                                       required=False, allow_blank=True)
    hasKey = serializers.SerializerMethodField()
    activationDate = serializers.DateField(source="activation_date", required=False, allow_null=True)
    expiryDate = serializers.DateField(source="expiry_date", required=False, allow_null=True)
    isActive = serializers.BooleanField(source="is_active", read_only=True)

    class Meta:
        model = ProductLicense
        fields = ("id", "productId", "licenseNumber", "licenseKey", "hasKey",
                  "activationDate", "expiryDate", "isActive")
        read_only_fields = ("id", "hasKey", "isActive")

    def get_hasKey(self, obj):
        return obj.encrypted_key is not None

    def validate_licenseKey(self, value):
        value = value.strip()
        if any(unicodedata.category(char) == "Cc" for char in value):
            raise serializers.ValidationError("Invalid license key.")
        return value

    def validate(self, values):
        key = values.get("licenseKey", "")
        number = values.get("license_number", "").strip()
        if not key and not number:
            raise serializers.ValidationError("License key or number is required.")
        activation = values.get("activation_date")
        expiry = values.get("expiry_date")
        if activation and expiry and expiry < activation:
            raise serializers.ValidationError("Expiry date cannot precede activation date.")
        values["license_number"] = number
        return values

    def create(self, validated_data):
        key = validated_data.pop("licenseKey", "")
        if key:
            validated_data["encrypted_key"] = encrypt_license_key(key)
            validated_data["key_fingerprint"] = license_fingerprint(key)
        return ProductLicense.objects.create(**validated_data)


class ProductLicenseViewSet(ModelViewSet):
    serializer_class = ProductLicenseSerializer
    queryset = ProductLicense.objects.order_by("-id")
    permission_classes = [IsAuthenticated, ProductLicensePermission]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def list(self, request, *args, **kwargs):
        try:
            product_id = int(request.query_params.get("productId", ""))
        except ValueError:
            return Response({"detail": "Invalid request."}, status=400)
        if product_id <= 0:
            return Response({"detail": "Invalid request."}, status=400)
        rows = self.get_queryset().filter(product_id=product_id)
        return Response(self.get_serializer(rows, many=True).data)

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return super().create(request, *args, **kwargs)
        except IntegrityError as error:
            message = str(error)
            if "UNIQUE constraint failed" in message or re.search(r"\((?:2601|2627)\)", message):
                return Response({"detail": "Active license key already exists."}, status=400)
            return Response({"detail": "Invalid request."}, status=400)

    def destroy(self, request, *args, **kwargs):
        license = self.get_object()
        if license.is_active:
            license.is_active = False
            license.save(update_fields=["is_active", "updated_at"])
        return Response(self.get_serializer(license).data)

    @action(detail=True, methods=["get"])
    def reveal(self, request, pk=None):
        license = self.get_object()
        response = Response({"licenseKey": decrypt_license_key(license.encrypted_key)
                             if license.encrypted_key is not None else None})
        response["Cache-Control"] = "no-store"
        return response
