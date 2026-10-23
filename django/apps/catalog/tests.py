from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User
from .models import Brand, Category, Unit, Product


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


class ProductApiTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="product-admin", email="product-admin@example.test", password="StrongPass123!"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.category = Category.objects.create(code="COMPUTERS", name_en="Computers")
        self.brand = Brand.objects.create(code="DELL", name_en="Dell")
        self.unit = Unit.objects.create(code="PCS", name_en="Pieces")
        self.data = {
            "sku": "laptop-01", "barcode": "123456789012", "nameEn": "Laptop",
            "nameAr": "حاسوب محمول", "categoryId": self.category.pk,
            "brandId": self.brand.pk, "unitId": self.unit.pk,
            "productType": "stock", "serialTracked": True,
            "costPrice": "250.000", "basePrice": "320.500",
            "minPrice": "300.000", "reorderLevel": "5.000000",
        }

    def test_stock_product_bilingual_unique_and_references(self):
        response = self.client.post("/api/products", self.data, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data["sku"], "LAPTOP-01")
        self.assertEqual(response.data["nameAr"], "حاسوب محمول")
        self.assertEqual(self.client.post("/api/products", {
            **self.data, "barcode": "987654321000"
        }, format="json").status_code, 400)
        self.assertEqual(self.client.post("/api/products", {
            **self.data, "sku": "LAPTOP-02"
        }, format="json").status_code, 400)
        self.assertEqual(self.client.delete(f"/api/categories/{self.category.pk}").status_code, 409)
        self.assertEqual(self.client.delete(f"/api/brands/{self.brand.pk}").status_code, 409)
        self.assertEqual(self.client.delete(f"/api/units/{self.unit.pk}").status_code, 409)

    def test_product_price_category_and_type_rules(self):
        for change in [
            {"sku": "A", "costPrice": "-1.000"},
            {"sku": "B", "categoryId": 999999},
            {"sku": "C", "minPrice": "400.000"},
            {"sku": "D", "productType": "nonstock", "serialTracked": True},
            {"sku": "E", "productType": "digital", "reorderLevel": "1.000000"},
        ]:
            self.assertEqual(self.client.post("/api/products", {
                **self.data, **change
            }, format="json").status_code, 400)
        self.assertFalse(Product.objects.exists())

    def test_nonstock_no_quantity_settings(self):
        response = self.client.post("/api/products", {
            **self.data, "sku": "SERVICE-01", "barcode": "", "productType": "nonstock",
            "serialTracked": False, "reorderLevel": "0.000000",
        }, format="json")
        self.assertEqual(response.status_code, 201, response.data)
