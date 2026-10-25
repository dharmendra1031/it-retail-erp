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
        duplicate = self.client.post("/api/categories", {
            "code": "laptops", "nameEn": "Duplicate", "parentId": root.data["id"],
        }, format="json")
        self.assertEqual(duplicate.status_code, 400)
        self.assertEqual(duplicate.data, {"detail": "Category code already exists."})
        cycle = self.client.put(f"/api/categories/{root.data['id']}", {
            "code": "COMPUTERS", "nameEn": "Computers", "parentId": child.data["id"],
        }, format="json")
        self.assertEqual(cycle.status_code, 400)
        self.assertEqual(self.client.delete(f"/api/categories/{root.data['id']}").status_code, 409)

    def test_category_search_by_code_and_bilingual_name(self):
        root = self.client.post("/api/categories", {
            "code": "COMP", "nameEn": "Computers", "nameAr": "الحواسيب",
        }, format="json")
        self.assertEqual(root.status_code, 201, root.data)
        child = self.client.post("/api/categories", {
            "code": "LAP", "nameEn": "Laptops", "nameAr": "الحواسيب المحمولة",
            "parentId": root.data["id"],
        }, format="json")
        self.assertEqual(child.status_code, 201, child.data)
        self.client.post("/api/categories", {
            "code": "PRN", "nameEn": "Printers", "nameAr": "الطابعات",
        }, format="json")

        for query, expected in [
            ("?search=comp", {"COMP"}),
            ("?search=Laptop", {"LAP"}),
            ("?search=الحواسيب", {"COMP", "LAP"}),
        ]:
            response = self.client.get("/api/categories" + query)
            self.assertEqual(response.status_code, 200, response.data)
            self.assertEqual({row["code"] for row in response.data}, expected)

        self.assertEqual(self.client.get(
            f"/api/categories/{child.data['id']}"
        ).data["parentId"], root.data["id"])

    def test_reparenting_does_not_create_a_deep_category_cycle(self):
        root = Category.objects.create(code="ROOT", name_en="Root")
        child = Category.objects.create(code="CHILD", name_en="Child", parent=root)
        grandchild = Category.objects.create(code="LEAF", name_en="Leaf", parent=child)

        update = self.client.put(f"/api/categories/{root.pk}", {
            "code": "ROOT", "nameEn": "Root", "parentId": grandchild.pk,
        }, format="json")
        self.assertEqual(update.status_code, 400)
        root.refresh_from_db()
        self.assertIsNone(root.parent_id)
        self.assertEqual(Category.objects.count(), 3)

    def test_category_with_subcategory_and_product_cannot_be_deleted(self):
        from decimal import Decimal

        root = Category.objects.create(code="HARDWARE", name_en="Hardware", name_ar="أجهزة")
        child = Category.objects.create(code="SSD", name_en="SSD", parent=root)
        unit = Unit.objects.create(code="PCS", name_en="Pieces")
        Product.objects.create(
            sku="SSD-001", name_en="SSD 1TB", name_ar="قرص",
            category=child, unit=unit,
            cost_price=Decimal("10.500"), base_price=Decimal("15.750"),
        )

        for category in (child, root):
            response = self.client.delete(f"/api/categories/{category.pk}")
            self.assertEqual(response.status_code, 409)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 2)

    def test_brand_and_unit_uniqueness_and_precision(self):
        brand = {"code": "dell", "nameEn": "Dell", "nameAr": "ديل"}
        self.assertEqual(self.client.post("/api/brands", brand, format="json").status_code, 201)
        duplicate_brand = self.client.post("/api/brands", brand, format="json")
        self.assertEqual(duplicate_brand.status_code, 400)
        self.assertEqual(duplicate_brand.data, {"detail": "Brand code already exists."})
        unit = {"code": "PCS", "nameEn": "Pieces", "decimalPlaces": 0}
        self.assertEqual(self.client.post("/api/units", unit, format="json").status_code, 201)
        duplicate_unit = self.client.post("/api/units", unit, format="json")
        self.assertEqual(duplicate_unit.status_code, 400)
        self.assertEqual(duplicate_unit.data, {"detail": "Unit code already exists."})
        self.assertEqual(self.client.post("/api/units", {
            **unit, "code": "BAD", "decimalPlaces": 7
        }, format="json").status_code, 400)
        self.assertEqual((Brand.objects.count(), Unit.objects.count()), (1, 1))


    def test_category_sibling_uniqueness_and_invalid_reparent(self):
        root = self.client.post("/api/categories", {
            "code": "ROOT-A", "nameEn": "Root A", "nameAr": "الفئة الأولى",
        }, format="json")
        second = self.client.post("/api/categories", {
            "code": "ROOT-B", "nameEn": "Root B",
        }, format="json")
        self.assertEqual((root.status_code, second.status_code), (201, 201))
        common = {"code": "SSD", "nameEn": "SSD"}
        one = self.client.post("/api/categories", {
            **common, "parentId": root.data["id"],
        }, format="json")
        two = self.client.post("/api/categories", {
            **common, "parentId": second.data["id"],
        }, format="json")
        self.assertEqual((one.status_code, two.status_code), (201, 201))
        duplicate = self.client.post("/api/categories", {
            **common, "code": "ssd", "parentId": root.data["id"],
        }, format="json")
        self.assertEqual(duplicate.status_code, 400)
        collision = self.client.put(f"/api/categories/{one.data['id']}", {
            **common, "parentId": second.data["id"],
        }, format="json")
        self.assertEqual(collision.status_code, 400)
        still = self.client.get(f"/api/categories/{one.data['id']}")
        self.assertEqual(still.data["parentId"], root.data["id"])

    def test_brand_and_unit_updates_preserve_codes_and_unicode(self):
        brand = self.client.post("/api/brands", {
            "code": "HP", "nameEn": "HP", "nameAr": "إتش بي",
        }, format="json")
        duplicate = self.client.post("/api/brands", {
            "code": "hp", "nameEn": "Duplicate",
        }, format="json")
        self.assertEqual((brand.status_code, duplicate.status_code), (201, 400))
        updated = self.client.put(f"/api/brands/{brand.data['id']}", {
            "code": "HP", "nameEn": "Hewlett Packard", "nameAr": "هيوليت باكارد",
        }, format="json")
        self.assertEqual(updated.status_code, 200, updated.data)
        self.assertEqual(self.client.get(f"/api/brands/{brand.data['id']}").data["nameAr"], "هيوليت باكارد")

        unit = self.client.post("/api/units", {
            "code": "BOX", "nameEn": "Box", "nameAr": "صندوق", "decimalPlaces": 2,
        }, format="json")
        self.assertEqual(unit.status_code, 201, unit.data)
        for invalid in (7, -1):
            rejection = self.client.put(f"/api/units/{unit.data['id']}", {
                "code": "BOX", "nameEn": "Box", "decimalPlaces": invalid,
            }, format="json")
            self.assertEqual(rejection.status_code, 400)
        self.assertEqual(self.client.get(f"/api/units/{unit.data['id']}").data["decimalPlaces"], 2)

    def test_unit_precision_database_constraint(self):
        from django.db import IntegrityError, transaction

        unit = Unit.objects.create(code="KG", name_en="Kilogram", decimal_places=3)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Unit.objects.filter(pk=unit.pk).update(decimal_places=7)
        unit.refresh_from_db()
        self.assertEqual(unit.decimal_places, 3)

    def test_brand_unit_product_references_are_protected(self):
        from decimal import Decimal

        category = Category.objects.create(code="LAPTOP", name_en="Laptops")
        brand = Brand.objects.create(code="LENOVO", name_en="Lenovo", name_ar="لينوفو")
        unit = Unit.objects.create(code="PCS", name_en="Pieces", name_ar="قطعة")
        Product.objects.create(
            sku="LAPTOP-100", name_en="Laptop", name_ar="حاسوب محمول",
            category=category, brand=brand, unit=unit,
            cost_price=Decimal("250.000"), base_price=Decimal("350.000"),
        )

        for kind, pk in (("brands", brand.pk), ("units", unit.pk)):
            response = self.client.delete(f"/api/{kind}/{pk}")
            self.assertEqual(response.status_code, 409)
        self.assertEqual(Product.objects.count(), 1)

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
