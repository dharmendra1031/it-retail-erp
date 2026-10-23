from pathlib import Path

from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.accounts.permissions import has_permission
from apps.accounts.roles_api import IsAdminUser
from .models import Customer, PartnerDocument, Supplier


class PartnerPermission(BasePermission):
    ACTIONS = {"create": "add", "update": "edit", "destroy": "delete"}

    def has_permission(self, request, view):
        operation = self.ACTIONS.get(view.action, "view")
        return has_permission(request.user, f"{view.basename}.{operation}")


class PartnerSerializer(serializers.ModelSerializer):
    nameEn = serializers.CharField(source="name_en", max_length=200)
    nameAr = serializers.CharField(source="name_ar", max_length=200, required=False, allow_blank=True)
    addressEn = serializers.CharField(source="address_en", max_length=500, required=False, allow_blank=True)
    addressAr = serializers.CharField(source="address_ar", max_length=500, required=False, allow_blank=True)
    paymentTermsDays = serializers.IntegerField(source="payment_terms_days", min_value=0, max_value=365)
    isActive = serializers.BooleanField(source="is_active", required=False)
    contactPerson = serializers.CharField(source="contact_person", max_length=150, required=False, allow_blank=True)
    telephone = serializers.CharField(source="telephone", max_length=30, required=False, allow_blank=True)
    remarks = serializers.CharField(source="remarks", max_length=1000, required=False, allow_blank=True)

    def validate_code(self, value):
        code = value.strip().upper()
        if not code or not code.replace("_", "").replace("-", "").isalnum():
            raise serializers.ValidationError("Invalid code.")
        if self.Meta.model.objects.filter(code__iexact=code).exclude(
            pk=getattr(self.instance, "pk", None)
        ).exists():
            raise serializers.ValidationError("Code already exists.")
        return code

    def validate_nameEn(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name required.")
        return value.strip()


class CustomerSerializer(PartnerSerializer):
    civilId = serializers.CharField(source="civil_id", max_length=30, required=False, allow_blank=True)
    companyName = serializers.CharField(source="company_name", max_length=200, required=False, allow_blank=True)
    email = serializers.EmailField(source="email", max_length=200, required=False, allow_blank=True)
    taxNumber = serializers.CharField(source="tax_number", max_length=100, required=False, allow_blank=True)
    openingBalance = serializers.DecimalField(source="opening_balance", max_digits=18, decimal_places=3, min_value=0, required=False)
    customerType = serializers.ChoiceField(source="customer_type", choices=[
        key for key, _ in Customer.TYPES
    ])
    creditLimit = serializers.DecimalField(source="credit_limit", max_digits=18, decimal_places=3, min_value=0)

    class Meta:
        model = Customer
        fields = ("id", "code", "nameEn", "nameAr", "addressEn", "addressAr",
                  "mobile", "civilId", "customerType", "paymentTermsDays", "creditLimit", "isActive",
                  "contactPerson", "telephone", "remarks", "companyName", "email",
                  "taxNumber", "openingBalance")
        read_only_fields = ("id",)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        request = self.context.get("request")
        if request is not None and not IsAdminUser().has_permission(request, None):
            result.pop("civilId", None)
        return result


class SupplierSerializer(PartnerSerializer):
    taxNumber = serializers.CharField(source="tax_number", max_length=100, required=False, allow_blank=True)
    openingBalance = serializers.DecimalField(
        source="opening_balance", max_digits=18, decimal_places=3, min_value=0
    )
    creditLimit = serializers.DecimalField(
        source="credit_limit", max_digits=18, decimal_places=3, min_value=0, required=False
    )

    class Meta:
        model = Supplier
        fields = ("id", "code", "nameEn", "nameAr", "addressEn", "addressAr",
                  "mobile", "email", "taxNumber", "paymentTermsDays", "openingBalance", "isActive",
                  "contactPerson", "telephone", "remarks", "creditLimit")
        read_only_fields = ("id",)


class PartnerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, PartnerPermission]
    http_method_names = ["get", "post", "put", "delete", "head", "options"]

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.order_by("code")

    def destroy(self, request, *args, **kwargs):
        if self.get_object().documents.exists():
            return Response({"detail": "Protected documents exist."}, status=409)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get", "post"])
    def documents(self, request, pk=None):
        if not IsAdminUser().has_permission(request, self):
            return Response(status=403)
        partner = self.get_object()
        docs = PartnerDocument.objects.filter(**{self.document_fk: partner})
        if request.method == "GET":
            return Response([self.document_data(doc) for doc in docs.order_by("id")])

        file = request.FILES.get("file")
        if file is None or not 0 < file.size <= 5 * 1024 * 1024:
            return Response({"detail": "Invalid document."}, status=400)
        sig = file.read(12)
        mime = file.content_type
        if not (
            mime == "application/pdf" and sig.startswith(b"%PDF-")
            or mime == "image/png" and sig.startswith(b"\x89PNG\r\n\x1a\n")
            or mime == "image/jpeg" and sig.startswith(b"\xff\xd8\xff")
        ):
            return Response({"detail": "Invalid document."}, status=400)
        file.seek(0)
        document = PartnerDocument.objects.create(
            **{self.document_fk: partner},
            file_name=Path(file.name).name[:200],
            content_type=mime,
            content=file.read(),
        )
        return Response(self.document_data(document), status=201)

    @staticmethod
    def document_data(doc):
        return {"id": doc.pk, "fileName": doc.file_name,
                "contentType": doc.content_type, "size": len(doc.content)}


class CustomerViewSet(PartnerViewSet):
    serializer_class = CustomerSerializer
    document_fk = "customer"


class SupplierViewSet(PartnerViewSet):
    serializer_class = SupplierSerializer
    document_fk = "supplier"


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_document(request, kind, partner_id, document_id):
    if not request.user.is_authenticated or not IsAdminUser().has_permission(request, None):
        return HttpResponse(status=403)
    if kind not in ("customers", "suppliers"):
        return HttpResponse(status=404)
    owner = "customer_id" if kind == "customers" else "supplier_id"
    document = PartnerDocument.objects.filter(pk=document_id, **{owner: partner_id}).first()
    if document is None:
        return HttpResponse(status=404)
    response = HttpResponse(bytes(document.content), content_type=document.content_type)
    response["Content-Disposition"] = 'attachment; filename="document"'
    response["X-Content-Type-Options"] = "nosniff"
    return response
