from pathlib import Path
from secrets import token_hex
from PIL import Image, UnidentifiedImageError
from django.db import transaction

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

        allowed = {
            ".jpg": ("image/jpeg", "JPEG"),
            ".jpeg": ("image/jpeg", "JPEG"),
            ".png": ("image/png", "PNG"),
            ".webp": ("image/webp", "WEBP"),
        }
        expected_type, expected_format = allowed[extension]
        if logo.content_type != expected_type:
            raise serializers.ValidationError("Invalid logo file type.")
        try:
            with Image.open(logo) as image:
                if image.format != expected_format:
                    raise serializers.ValidationError("Invalid logo file type.")
                image.verify()
        except (UnidentifiedImageError, OSError):
            raise serializers.ValidationError("Invalid logo file type.")
        finally:
            logo.seek(0)
        return logo

    def create(self, validated_data):
        logo = validated_data.pop("logo", None)
        new_logo = ""
        try:
            with transaction.atomic():
                company = super().create(validated_data)
                if logo:
                    new_logo = self._save_logo(company.id, logo)
                    company.logo.name = new_logo
                    company.save(update_fields=["logo"])
            return company
        except Exception:
            if new_logo:
                default_storage.delete(new_logo)
            raise

    def update(self, instance, validated_data):
        logo = validated_data.pop("logo", None)
        previous_logo = instance.logo.name if instance.logo else ""
        new_logo = ""
        try:
            with transaction.atomic():
                company = super().update(instance, validated_data)
                if logo:
                    new_logo = self._save_logo(company.id, logo)
                    company.logo.name = new_logo
                    company.save(update_fields=["logo"])
        except Exception:
            if new_logo:
                default_storage.delete(new_logo)
            raise

        if new_logo and previous_logo and previous_logo != new_logo:
            default_storage.delete(previous_logo)
        return company

    def get_logoUrl(self, obj):
        return obj.logo.url if obj.logo else ""

    @staticmethod
    def _save_logo(company_id, file):
        extension = Path(file.name).suffix.lower()
        path = f"company/company-{company_id}-{token_hex(12)}{extension}"
        return default_storage.save(path, file)
