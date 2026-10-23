from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIClient

from apps.accounts.models import Role, User
from .models import Company
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

    def test_name_over_max_length_is_rejected(self):
        serializer = CompanySerializer(data={"nameEn": "A" * 201})
        self.assertFalse(serializer.is_valid())
        self.assertIn("nameEn", serializer.errors)

    def test_invalid_website_is_rejected(self):
        serializer = CompanySerializer(data={"nameEn": "Retail", "website": "not-a-url"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("website", serializer.errors)

    def test_invalid_email_is_rejected(self):
        serializer = CompanySerializer(data={"nameEn": "Retail", "email": "invalid"})
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)


class ApiRouteTests(SimpleTestCase):
    def test_company_route(self):
        match = resolve("/api/companies")
        self.assertEqual(match.url_name, "company-list")

    def test_company_detail_route(self):
        match = resolve("/api/companies/123")
        self.assertEqual(match.url_name, "company-detail")
        self.assertEqual(match.kwargs["pk"], "123")

    def test_auth_csrf_route(self):
        match = resolve("/api/auth/csrf")
        self.assertEqual(match.url_name, "api-csrf")

    def test_auth_login_route(self):
        match = resolve("/api/auth/login")
        self.assertEqual(match.url_name, "api-login")


class CompanyAuthorizationTests(TestCase):
    def setUp(self):
        self.employee = User.objects.create_user(
            username="employee", email="employee@example.com", password="TestPass123!"
        )
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="TestPass123!"
        )
        self.client = APIClient()

    def test_employee_can_read_but_cannot_create_company(self):
        Company.objects.create(name_en="Existing Company")
        self.client.force_authenticate(user=self.employee)
        self.assertEqual(self.client.get("/api/companies").status_code, 200)
        self.assertEqual(
            self.client.post("/api/companies", {"nameEn": "New Company"}, format="multipart").status_code,
            403,
        )
        self.assertEqual(Company.objects.count(), 1)

    def test_employee_cannot_change_or_delete_company(self):
        company = Company.objects.create(name_en="Existing Company")
        self.client.force_authenticate(user=self.employee)
        self.assertEqual(
            self.client.put(
                f"/api/companies/{company.id}", {"nameEn": "Changed"}, format="multipart"
            ).status_code,
            403,
        )
        self.assertEqual(self.client.delete(f"/api/companies/{company.id}").status_code, 403)
        company.refresh_from_db()
        self.assertEqual(company.name_en, "Existing Company")

    def test_admin_role_can_create_company(self):
        self.employee.roles.add(Role.objects.get(name="Admin"))
        self.client.force_authenticate(user=self.employee)
        response = self.client.post(
            "/api/companies", {"nameEn": "Authorized Company"}, format="multipart"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Company.objects.filter(name_en="Authorized Company").exists())
