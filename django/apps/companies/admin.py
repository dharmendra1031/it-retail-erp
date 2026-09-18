from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name_en", "telephone", "mobile", "tax_number", "is_active")
    search_fields = ("name_en", "name_ar", "tax_number", "commercial_registration_number")
    list_filter = ("is_active",)
