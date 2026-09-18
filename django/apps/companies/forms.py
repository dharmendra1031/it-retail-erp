from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name_en",
            "name_ar",
            "address_en",
            "address_ar",
            "telephone",
            "mobile",
            "email",
            "website",
            "tax_number",
            "commercial_registration_number",
            "logo",
            "bank_details",
            "invoice_header",
            "invoice_footer",
            "terms_and_conditions",
            "social_media",
            "is_active",
        ]
        labels = {
            "name_en": "Company Name (English)",
            "name_ar": "اسم الشركة (العربية)",
            "address_en": "Address (English)",
            "address_ar": "العنوان (العربية)",
            "tax_number": "VAT / Tax Number",
            "commercial_registration_number": "Commercial Registration Number",
        }
        widgets = {
            "address_en": forms.Textarea(attrs={"rows": 3}),
            "address_ar": forms.Textarea(attrs={"rows": 3, "dir": "rtl"}),
            "name_ar": forms.TextInput(attrs={"dir": "rtl"}),
            "bank_details": forms.Textarea(attrs={"rows": 3}),
            "invoice_header": forms.Textarea(attrs={"rows": 3}),
            "invoice_footer": forms.Textarea(attrs={"rows": 3}),
            "terms_and_conditions": forms.Textarea(attrs={"rows": 4}),
            "social_media": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == "is_active":
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

        self.fields["logo"].widget.attrs["accept"] = ".jpg,.jpeg,.png,.webp"

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if not logo:
            return logo

        content_type = getattr(logo, "content_type", None)
        if not content_type:
            return logo

        if logo.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Logo must be smaller than 2 MB.")

        if content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise forms.ValidationError("Logo must be JPG, PNG or WebP.")

        return logo
