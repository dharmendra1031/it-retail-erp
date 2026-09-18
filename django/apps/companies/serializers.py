from pathlib import Path

from django.core.files.storage import default_storage
from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    nameEn = serializers.CharField(source="name_en", max_length=200)
    nameAr = serializers.CharField(source="name_ar", max_length=200, allow_blank=True, required=False)
    addressEn = serializers.CharField(source="address_en", max_length=500, allow_blank=True, required=False)
    addressAr = serializers.CharField(source="address_ar", max_length=500, allow_blank=True, required=False)
    taxNumber = serializers.CharField(source="tax_number", max_length=100, allow_blank=True, required=False)
    commercialRegistrationNumber = serializers.CharField(
        source="commercial_registration_number",
        max_length=100,
        allow_blank=True,
        required=False,
    )
    bankDetails = serializers.CharField(source="bank_details", allow_blank=True, required=False)
    invoiceHeader = serializers.CharField(source="invoice_header", allow_blank=True, required=False)
    invoiceFooter = serializers.CharField(source="invoice_footer", allow_blank=True, required=False)
    termsAndConditions = serializers.CharField(
        source="terms_and_conditions",
        allow_blank=True,
        required=False,
    )
    socialMedia = serializers.CharField(source="social_media", allow_blank=True, required=False)
    isActive = serializers.BooleanField(source="is_active", required=False)
    logo = serializers.ImageField(write_only=True, required=False)
    logoUrl = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "id",
            "nameEn",
            "nameAr",
            "addressEn",
            "addressAr",
            "telephone",
            "mobile",
            "email",
            "website",
            "taxNumber",
            "commercialRegistrationNumber",
            "logo",
            "logoUrl",
            "bankDetails",
            "invoiceHeader",
            "invoiceFooter",
            "termsAndConditions",
            "socialMedia",
            "isActive",
        ]
        read_only_fields = ["id", "logoUrl"]

    def validate_logo(self, logo):
        if logo.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Logo must be smaller than 2 MB.")

        extension = Path(logo.name).suffix.lower()
        if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
            raise serializers.ValidationError("Logo must be JPG, PNG or WebP.")

        return logo

    def create(self, validated_data):
        logo = validated_data.pop("logo", None)
        company = super().create(validated_data)

        if logo:
            company.logo.name = self._save_logo(company.id, logo)
            company.save(update_fields=["logo"])

        return company

    def update(self, instance, validated_data):
        logo = validated_data.pop("logo", None)
        previous_logo = instance.logo.name if instance.logo else ""

        company = super().update(instance, validated_data)

        if logo:
            company.logo.name = self._save_logo(company.id, logo)
            company.save(update_fields=["logo"])

            if previous_logo and previous_logo != company.logo.name:
                default_storage.delete(previous_logo)

        return company

    def get_logoUrl(self, obj):
        return obj.logo.url if obj.logo else ""

    @staticmethod
    def _save_logo(company_id, file):
        extension = Path(file.name).suffix.lower()
        path = f"company/company-{company_id}{extension}"

        if default_storage.exists(path):
            default_storage.delete(path)

        return default_storage.save(path, file)
