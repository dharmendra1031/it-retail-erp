from django.test import SimpleTestCase
from django.urls import resolve

from apps.companies.serializers import CompanySerializer


class CompanySerializerTests(SimpleTestCase):
    def test_name_is_required(self):
        serializer = CompanySerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("nameEn", serializer.errors)

    def test_bilingual_fields_are_accepted(self):
        serializer = CompanySerializer(data={"nameEn": "Retail", "nameAr": "تجارة"})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["name_ar"], "تجارة")

    def test_invalid_email_is_rejected(self):
        serializer = CompanySerializer(data={"nameEn": "Retail", "email": "invalid"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


class ApiRouteTests(SimpleTestCase):
    def test_company_route(self):
        match = resolve("/api/companies")
        self.assertEqual(match.url_name, "company-list")

    def test_auth_login_route(self):
        match = resolve("/api/auth/login")
        self.assertEqual(match.url_name, "api-login")
