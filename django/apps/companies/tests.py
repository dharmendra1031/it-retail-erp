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

    def test_invalid_payload_uses_shared_error_response(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/api/companies", {"nameEn": ""}, format="multipart"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "Invalid request."})

    def test_missing_company_has_no_error_payload(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get("/api/companies/999999")
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(response.data)


class BranchWarehouseApiTests(TestCase):
    def setUp(self):
        from apps.accounts.models import User
        from .models import Company, Branch, Warehouse

        self.admin = User.objects.create_superuser(
            username="orgadmin", email="orgadmin@example.test", password="StrongPass123!"
        )
        self.company = Company.objects.create(name_en="Test Company")
        self.branch = Branch.objects.create(company=self.company, code="H1", name_en="HQ")
        self.second_branch = Branch.objects.create(company=self.company, code="H2", name_en="Shop Two")
        self.warehouse = Warehouse.objects.create(branch=self.branch, code="MAIN", name_en="Main")
        self.second_warehouse = Warehouse.objects.create(branch=self.second_branch, code="MAIN", name_en="Other")
        self.employee = User.objects.create_user(
            username="branchstaff", email="branchstaff@example.test",
            password="StrongPass123!", branch=self.branch
        )
        self.client = APIClient()

    def test_non_admin_is_scoped_to_assigned_branch_and_warehouses(self):
        self.client.force_authenticate(user=self.employee)
        branches = self.client.get("/api/branches")
        self.assertEqual(branches.status_code, 200)
        self.assertEqual([item["id"] for item in branches.data], [self.branch.id])
        self.assertEqual(self.client.get(f"/api/branches/{self.second_branch.id}").status_code, 404)
        warehouses = self.client.get("/api/warehouses")
        self.assertEqual([item["id"] for item in warehouses.data], [self.warehouse.id])
        self.assertEqual(self.client.get(f"/api/warehouses/{self.second_warehouse.id}").status_code, 404)
        self.assertEqual(self.client.post("/api/branches", {
            "companyId": self.company.id, "code": "H3", "nameEn": "Another"
        }, format="json").status_code, 403)

    def test_duplicate_code_and_orphan_fk_are_rejected(self):
        self.client.force_authenticate(user=self.admin)
        duplicate = self.client.post("/api/branches", {
            "companyId": self.company.id, "code": "h1", "nameEn": "Duplicate"
        }, format="json")
        self.assertEqual(duplicate.status_code, 400)
        orphan = self.client.post("/api/warehouses", {
            "branchId": 999999999, "code": "A", "nameEn": "Orphan"
        }, format="json")
        self.assertEqual(orphan.status_code, 400)
        self.assertEqual(self.client.delete(f"/api/branches/{self.branch.id}").status_code, 409)
        self.assertEqual(self.client.delete(f"/api/companies/{self.company.id}").status_code, 409)


class CompanyLogoLifecycleTests(TestCase):
    def setUp(self):
        import tempfile
        from django.test import override_settings
        from apps.accounts.models import User

        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        settings_override = override_settings(MEDIA_ROOT=self.folder.name)
        settings_override.enable()
        self.addCleanup(settings_override.disable)
        self.admin = User.objects.create_superuser(
            username="logoadmin", email="logoadmin@example.test", password="StrongPass123!"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def _logo(self, name="logo.png", mime="image/png"):
        from io import BytesIO
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile

        output = BytesIO()
        Image.new("RGB", (2, 2), color="white").save(output, format="PNG")
        return SimpleUploadedFile(name, output.getvalue(), content_type=mime)

    def test_valid_image_is_saved_and_replaced_without_orphan(self):
        import os
        from .models import Company

        created = self.client.post("/api/companies", {
            "nameEn": "Logo Shop", "logo": self._logo()
        }, format="multipart")
        self.assertEqual(created.status_code, 201)
        company = Company.objects.get(pk=created.data["id"])
        old_name = company.logo.name
        self.assertTrue(os.path.exists(company.logo.path))

        updated = self.client.put(f"/api/companies/{company.pk}", {
            "nameEn": "Logo Shop", "logo": self._logo("replacement.png")
        }, format="multipart")
        self.assertEqual(updated.status_code, 200)
        company.refresh_from_db()
        self.assertNotEqual(company.logo.name, old_name)
        self.assertTrue(os.path.exists(company.logo.path))
        self.assertFalse(os.path.exists(os.path.join(self.folder.name, old_name)))

    def test_invalid_mime_and_corrupt_image_rejected(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        from .models import Company

        mime = self.client.post("/api/companies", {
            "nameEn": "Mime Test", "logo": self._logo(mime="text/plain")
        }, format="multipart")
        self.assertEqual(mime.status_code, 400)
        invalid = self.client.post("/api/companies", {
            "nameEn": "Corrupt Test",
            "logo": SimpleUploadedFile("logo.png", b"not an image", content_type="image/png")
        }, format="multipart")
        self.assertEqual(invalid.status_code, 400)
        self.assertFalse(Company.objects.filter(name_en__in=["Mime Test", "Corrupt Test"]).exists())
