from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User
from .models import Brand, Category, Unit


class CatalogApiTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="catalog-admin", email="catalog-admin@example.test", password="StrongPass123!"
        )
        self.employee = User.objects.create_user(
            username="catalog-employee", email="catalog-employee@example.test", password="StrongPass123!"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)

    def test_category_root_child_unicode_duplicate_and_cycle(self):
        root = self.client.post("/api/categories", {
            "code": "computers", "nameEn": "Computers", "nameAr": "حواسيب",
        }, format="json")
        self.assertEqual(root.status_code, 201, root.data)
        child = self.client.post("/api/categories", {
            "code": "laptops", "nameEn": "Laptops", "nameAr": "حاسوب محمول",
            "parentId": root.data["id"],
        }, format="json")
        self.assertEqual(child.status_code, 201, child.data)
        self.assertEqual(root.data["code"], "COMPUTERS")
        self.assertEqual(self.client.post("/api/categories", {
            "code": "laptops", "nameEn": "Duplicate", "parentId": root.data["id"],
        }, format="json").status_code, 400)
        cycle = self.client.put(f"/api/categories/{root.data['id']}", {
            "code": "COMPUTERS", "nameEn": "Computers", "parentId": child.data["id"],
        }, format="json")
        self.assertEqual(cycle.status_code, 400)
        self.assertEqual(self.client.delete(f"/api/categories/{root.data['id']}").status_code, 409)

    def test_brand_and_unit_uniqueness_and_precision(self):
        brand = {"code": "dell", "nameEn": "Dell", "nameAr": "ديل"}
        self.assertEqual(self.client.post("/api/brands", brand, format="json").status_code, 201)
        self.assertEqual(self.client.post("/api/brands", brand, format="json").status_code, 400)
        unit = {"code": "PCS", "nameEn": "Pieces", "decimalPlaces": 0}
        self.assertEqual(self.client.post("/api/units", unit, format="json").status_code, 201)
        self.assertEqual(self.client.post("/api/units", {
            **unit, "code": "BAD", "decimalPlaces": 7
        }, format="json").status_code, 400)
        self.assertEqual((Brand.objects.count(), Unit.objects.count()), (1, 1))

    def test_employee_without_grants_cannot_read_or_modify(self):
        self.client.force_authenticate(user=self.employee)
        self.assertEqual(self.client.get("/api/brands").status_code, 403)
        self.assertEqual(self.client.post("/api/categories", {
            "code": "NO", "nameEn": "No Access"
        }, format="json").status_code, 403)
