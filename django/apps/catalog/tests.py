from concurrent.futures import ThreadPoolExecutor
import base64
import os
from threading import Barrier
from unittest import skipUnless
from unittest.mock import patch

from django.db import close_old_connections, connection
from django.test import TestCase, TransactionTestCase
from rest_framework.test import APIClient

from apps.accounts.models import AccessPermission, Role, User
from .models import Brand, Category, Unit, Product, ProductLicense


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

    def test_brand_unit_search_normalization_and_referenced_deletion(self):
        from decimal import Decimal

        brand = self.client.post("/api/brands", {
            "code": "  acer  ", "nameEn": "Acer", "nameAr": "ايسر",
        }, format="json")
        unit = self.client.post("/api/units", {
            "code": " kg ", "nameEn": "Kilogram", "nameAr": "كيلوغرام",
            "decimalPlaces": 3,
        }, format="json")
        self.assertEqual((brand.status_code, unit.status_code), (201, 201))
        self.assertEqual((brand.data["code"], unit.data["code"]), ("ACER", "KG"))
        for kind, term, expected in (
            ("brands", "ايسر", "ACER"), ("brands", "ace", "ACER"),
            ("units", "كيلوغرام", "KG"), ("units", "kilogram", "KG"),
        ):
            result = self.client.get(f"/api/{kind}?search={term}")
            self.assertEqual(result.status_code, 200)
            self.assertEqual([row["code"] for row in result.data], [expected])
        self.assertEqual(self.client.post("/api/brands", {
            "code": "ACER", "nameEn": "Duplicate",
        }, format="json").status_code, 400)
        self.assertEqual(self.client.post("/api/units", {
            "code": "KG", "nameEn": "Duplicate", "decimalPlaces": 0,
        }, format="json").status_code, 400)

        category = Category.objects.create(code="LAPTOPS", name_en="Laptops")
        Product.objects.create(
            sku="ACER-01", name_en="Acer Laptop", category=category,
            brand_id=brand.data["id"], unit_id=unit.data["id"],
            cost_price=Decimal("100.000"), base_price=Decimal("120.000"),
        )
        for kind, pk in (("brands", brand.data["id"]), ("units", unit.data["id"])):
            self.assertEqual(self.client.delete(f"/api/{kind}/{pk}").status_code, 409)

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
        self.assertEqual(self.client.get("/api/units").status_code, 403)
        self.assertEqual(self.client.post("/api/brands", {
            "code": "NO", "nameEn": "No Access"
        }, format="json").status_code, 403)
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

    def test_product_search_finds_english_arabic_name_and_barcode(self):
        product = {**self.data, "nameEn": "Portable Notebook"}
        response = self.client.post("/api/products", product, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        product_id = response.data["id"]

        for term in ("Notebook", product["nameAr"], product["barcode"]):
            with self.subTest(term=term):
                result = self.client.get("/api/products", {"search": term})
                self.assertEqual(result.status_code, 200, result.data)
                self.assertEqual([row["id"] for row in result.data], [product_id])

    def test_product_page_filters_and_validation(self):
        for sku, barcode in (("LAPTOP-01", "111222333444"), ("LAPTOP-02", "222333444555")):
            response = self.client.post(
                "/api/products", {**self.data, "sku": sku, "barcode": barcode},
                format="json",
            )
            self.assertEqual(response.status_code, 201, response.data)

        first = self.client.get("/api/products", {"page": 1, "pageSize": 1})
        second = self.client.get("/api/products", {"page": 2, "pageSize": 1})
        self.assertEqual(first.status_code, 200, first.data)
        self.assertEqual(first.data["total"], 2)
        self.assertEqual(first.data["pageSize"], 1)
        self.assertEqual([row["sku"] for row in first.data["items"]], ["LAPTOP-01"])
        self.assertEqual([row["sku"] for row in second.data["items"]], ["LAPTOP-02"])
        self.assertEqual(self.client.get("/api/products", {"page": 0}).status_code, 400)
        self.assertEqual(self.client.get("/api/products", {"pageSize": 101}).status_code, 400)

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

    def test_duplicate_sku_barcode_details_and_multiple_blank_barcodes(self):
        created = self.client.post("/api/products", self.data, format="json")
        self.assertEqual(created.status_code, 201, created.data)

        for fields in (
            {"barcode": "111222333444"},
            {"sku": "LAPTOP-02"},
        ):
            duplicate = self.client.post(
                "/api/products", {**self.data, **fields}, format="json"
            )
            self.assertEqual(duplicate.status_code, 400, duplicate.data)
            self.assertEqual(duplicate.data, {"detail": "SKU or barcode already exists."})

        for sku in ("BARCODELESS-1", "BARCODELESS-2"):
            response = self.client.post(
                "/api/products", {**self.data, "sku": sku, "barcode": ""},
                format="json",
            )
            self.assertEqual(response.status_code, 201, response.data)
            self.assertIsNone(response.data["barcode"])

    def test_rejected_product_mutations_preserve_existing_row(self):
        seeded = self.client.post(
            "/api/products", {**self.data, "barcode": "ABC-12345"}, format="json"
        )
        self.assertEqual(seeded.status_code, 201, seeded.data)
        product_id = seeded.data["id"]
        before = Product.objects.values().get(pk=product_id)
        inactive = Category.objects.create(code="INACTIVE", name_en="Inactive", is_active=False)

        cases = (
            ("duplicate sku", {"sku": " laptop-01 ", "barcode": "NEW-12345"},
             "SKU or barcode already exists."),
            ("duplicate barcode", {"sku": "NEW-01", "barcode": " abc-12345 "},
             "SKU or barcode already exists."),
            ("missing category", {"sku": "NEW-02", "barcode": "NEW-12345", "categoryId": None},
             "Invalid request."),
            ("zero category", {"sku": "NEW-08", "barcode": "NEW-12345", "categoryId": 0},
             "Invalid request."),
            ("inactive category", {"sku": "NEW-03", "barcode": "NEW-12345", "categoryId": inactive.pk},
             "Invalid request."),
            ("negative cost", {"sku": "NEW-04", "barcode": "NEW-12345", "costPrice": "-0.001"},
             "Invalid request."),
            ("negative base", {"sku": "NEW-05", "barcode": "NEW-12345", "basePrice": "-0.001"},
             "Invalid request."),
            ("negative minimum", {"sku": "NEW-06", "barcode": "NEW-12345", "minPrice": "-0.001"},
             "Invalid request."),
            ("excess price precision", {"sku": "NEW-07", "barcode": "NEW-12345", "basePrice": "320.5001"},
             "Invalid request."),
        )
        for label, change, detail in cases:
            with self.subTest(case=label):
                rejected = self.client.post(
                    "/api/products", {**self.data, **change}, format="json"
                )
                self.assertEqual(rejected.status_code, 400, rejected.data)
                self.assertEqual(rejected.data, {"detail": detail})
                self.assertEqual(Product.objects.count(), 1)
                self.assertEqual(Product.objects.values().get(pk=product_id), before)

        omitted_category = {**self.data, "sku": "NEW-09", "barcode": "NEW-12345"}
        del omitted_category["categoryId"]
        rejected = self.client.post("/api/products", omitted_category, format="json")
        self.assertEqual(rejected.status_code, 400, rejected.data)
        self.assertEqual(rejected.data, {"detail": "Invalid request."})
        self.assertEqual(Product.objects.values().get(pk=product_id), before)
        self.assertEqual(Product.objects.count(), 1)

        for label, change in (
            ("bad price", {"costPrice": "-0.001"}),
            ("missing category", {"categoryId": None}),
            ("inactive category", {"categoryId": inactive.pk}),
        ):
            with self.subTest(update=label):
                rejected = self.client.put(
                    f"/api/products/{product_id}",
                    {**self.data, "barcode": "ABC-12345", **change}, format="json",
                )
                self.assertEqual(rejected.status_code, 400, rejected.data)
                self.assertEqual(Product.objects.values().get(pk=product_id), before)

    def test_product_read_only_grant_denies_mutations(self):
        created = self.client.post("/api/products", self.data, format="json")
        self.assertEqual(created.status_code, 201, created.data)
        product_id = created.data["id"]

        employee = User.objects.create_user(
            username="product-reader", email="reader@example.test", password="StrongPass123!"
        )
        self.client.force_authenticate(user=employee)
        for path in ("/api/products", f"/api/products/{product_id}"):
            self.assertEqual(self.client.get(path).status_code, 403)

        role = Role.objects.create(name="Product Reader")
        permission, _ = AccessPermission.objects.get_or_create(
            code="products.view", defaults={"name": "Products View"}
        )
        role.permissions.add(permission)
        employee.roles.add(role)

        listing = self.client.get("/api/products")
        detail = self.client.get(f"/api/products/{product_id}")
        self.assertEqual(listing.status_code, 200, listing.data)
        self.assertEqual(detail.status_code, 200, detail.data)
        self.assertEqual(detail.data["id"], product_id)

        for method, path, payload in (
            ("post", "/api/products", {**self.data, "sku": "DENIED-NEW", "barcode": ""}),
            ("put", f"/api/products/{product_id}", {**self.data, "nameEn": "Unauthorized"}),
            ("delete", f"/api/products/{product_id}", None),
        ):
            response = getattr(self.client, method)(path, payload, format="json")
            self.assertEqual(response.status_code, 403, response.data)

        self.client.force_authenticate(user=self.admin)
        reloaded = self.client.get(f"/api/products/{product_id}")
        self.assertEqual(reloaded.data["nameEn"], self.data["nameEn"])
        self.assertEqual(Product.objects.count(), 1)

    def test_product_write_requires_csrf_cookie_session(self):
        session_client = APIClient(enforce_csrf_checks=True)
        session_client.force_login(self.admin)
        response = session_client.post("/api/products", self.data, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Product.objects.exists())

    def test_product_arabic_unicode_and_decimal_round_trip(self):
        data = {
            **self.data,
            "nameAr": "حاسوب مُتنقّل", "descriptionAr": "حاسوب تجريبي بذاكرة كبيرة",
            "costPrice": "123.456", "basePrice": "150.500",
            "minPrice": "120.125", "reorderLevel": "4.123456",
        }
        created = self.client.post("/api/products", data, format="json")
        self.assertEqual(created.status_code, 201, created.data)
        self.assertEqual(created.data["nameAr"], data["nameAr"])
        self.assertEqual(created.data["descriptionAr"], data["descriptionAr"])
        self.assertEqual(created.data["costPrice"], "123.456")
        self.assertEqual(created.data["basePrice"], "150.500")
        self.assertEqual(created.data["minPrice"], "120.125")
        self.assertEqual(created.data["reorderLevel"], "4.123456")

        updated = self.client.put(
            f"/api/products/{created.data['id']}",
            {**data, "descriptionAr": "تفاصيل مُحدّثة"},
            format="json",
        )
        self.assertEqual(updated.status_code, 200, updated.data)
        reloaded = self.client.get(f"/api/products/{created.data['id']}")
        self.assertEqual(reloaded.data["descriptionAr"], "تفاصيل مُحدّثة")
        self.assertEqual(reloaded.data["costPrice"], "123.456")
        self.assertEqual(reloaded.data["reorderLevel"], "4.123456")

    def test_nonstock_no_quantity_settings(self):
        for product_type, sku in (("nonstock", "SERVICE-01"), ("digital", "LICENSE-01")):
            with self.subTest(product_type=product_type):
                response = self.client.post("/api/products", {
                    **self.data, "sku": sku, "barcode": "", "productType": product_type,
                    "serialTracked": False, "reorderLevel": "0.000000",
                }, format="json")
                self.assertEqual(response.status_code, 201, response.data)
                self.assertFalse(response.data["serialTracked"])
                self.assertEqual(response.data["reorderLevel"], "0.000000")
                saved = Product.objects.get(pk=response.data["id"])
                self.assertEqual(saved.product_type, product_type)
                self.assertFalse(saved.serial_tracked)
                self.assertEqual(saved.reorder_level, 0)

    def test_database_rejects_nonstock_reorder_setting(self):
        from decimal import Decimal
        from django.db import IntegrityError, transaction

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Product.objects.create(
                    sku="INVALID-SERVICE", name_en="Invalid Service",
                    category=self.category, unit=self.unit, product_type="nonstock",
                    cost_price=Decimal("0.000"), base_price=Decimal("0.000"),
                    reorder_level=Decimal("1.000000"),
                )
        self.assertFalse(Product.objects.filter(sku="INVALID-SERVICE").exists())


@skipUnless(connection.vendor == "microsoft", "SQL Server concurrency test")
class ProductConcurrentApiTests(TransactionTestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="product-race-admin", email="product-race@example.test", password="StrongPass123!"
        )
        self.category = Category.objects.create(code="RACECAT", name_en="Race Category")
        self.unit = Unit.objects.create(code="RACEUNIT", name_en="Piece")

    def test_simultaneous_duplicate_sku_and_barcode(self):
        for duplicate_sku in (True, False):
            with self.subTest(duplicate_sku=duplicate_sku):
                barrier = Barrier(2)

                def create(attempt):
                    close_old_connections()
                    try:
                        client = APIClient()
                        client.force_authenticate(user=self.admin)
                        payload = {
                            "sku": "RACE-SKU" if duplicate_sku else f"RACE-SKU-{attempt}",
                            "barcode": f"RACE-BAR-{attempt}" if duplicate_sku else "RACE-BAR",
                            "nameEn": "Concurrent Product",
                            "categoryId": self.category.pk, "unitId": self.unit.pk,
                            "productType": "stock", "costPrice": "1.000", "basePrice": "2.000",
                        }
                        barrier.wait(timeout=10)
                        response = client.post("/api/products", payload, format="json")
                        return response.status_code, response.data
                    finally:
                        close_old_connections()

                with ThreadPoolExecutor(max_workers=2) as pool:
                    results = list(pool.map(create, (1, 2)))

                self.assertEqual(sorted(status for status, _ in results), [201, 400], results)
                self.assertEqual(
                    next(data for status, data in results if status == 400),
                    {"detail": "SKU or barcode already exists."},
                )
                matching = (Product.objects.filter(sku="RACE-SKU") if duplicate_sku
                            else Product.objects.filter(barcode="RACE-BAR"))
                self.assertEqual(matching.count(), 1)
                Product.objects.all().delete()


class ProductLicenseApiTests(TestCase):
    def setUp(self):
        secret = base64.b64encode(os.urandom(32)).decode("ascii")
        environment = patch.dict(os.environ, {"PRODUCT_LICENSE_SECRET": secret})
        environment.start()
        self.addCleanup(environment.stop)
        self.admin = User.objects.create_superuser(
            username="license-admin", email="license-admin@example.test", password="StrongPass123!"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        category = Category.objects.create(code="SOFTWARE", name_en="Software")
        unit = Unit.objects.create(code="LICENSE", name_en="License")
        self.product = Product.objects.create(
            sku="DIGITAL-01", name_en="Software License", category=category, unit=unit,
            product_type="digital", cost_price=0, base_price=1,
        )
        self.payload = {
            "productId": self.product.pk, "licenseKey": "AbC-123-key",
            "licenseNumber": "LIC-001", "activationDate": "2026-10-01",
            "expiryDate": "2027-10-01",
        }

    def test_key_is_encrypted_masked_unique_and_revocable(self):
        created = self.client.post("/api/product-licenses", self.payload, format="json")
        self.assertEqual(created.status_code, 201, created.data)
        license_id = created.data["id"]
        self.assertTrue(created.data["hasKey"])
        self.assertNotIn("licenseKey", created.data)
        self.assertEqual(created.data["expiryDate"], "2027-10-01")

        saved = ProductLicense.objects.get(pk=license_id)
        self.assertNotIn(self.payload["licenseKey"].encode(), bytes(saved.encrypted_key))
        self.assertEqual(len(bytes(saved.key_fingerprint)), 32)
        listed = self.client.get("/api/product-licenses", {"productId": self.product.pk})
        self.assertEqual(listed.status_code, 200, listed.data)
        self.assertEqual(len(listed.data), 1)
        self.assertNotIn("licenseKey", listed.data[0])

        type_change = self.client.put(f"/api/products/{self.product.pk}", {
            "sku": self.product.sku, "nameEn": self.product.name_en,
            "categoryId": self.product.category_id, "unitId": self.product.unit_id,
            "productType": "nonstock", "costPrice": "0.000", "basePrice": "1.000",
        }, format="json")
        self.assertEqual(type_change.status_code, 400, type_change.data)
        self.product.refresh_from_db()
        self.assertEqual(self.product.product_type, "digital")
        self.assertEqual(self.client.delete(
            f"/api/products/{self.product.pk}").status_code, 409)

        duplicate = self.client.post("/api/product-licenses", {
            **self.payload, "licenseKey": " ABC-123-KEY ", "licenseNumber": "LIC-002",
        }, format="json")
        self.assertEqual(duplicate.status_code, 400, duplicate.data)
        self.assertEqual(duplicate.data, {"detail": "Active license key already exists."})
        self.assertEqual(ProductLicense.objects.count(), 1)

        revealed = self.client.get(f"/api/product-licenses/{license_id}/reveal")
        self.assertEqual(revealed.status_code, 200, revealed.data)
        self.assertEqual(revealed.data, {"licenseKey": self.payload["licenseKey"]})
        self.assertEqual(revealed["Cache-Control"], "no-store")

        revoked = self.client.delete(f"/api/product-licenses/{license_id}")
        self.assertEqual(revoked.status_code, 200, revoked.data)
        self.assertFalse(revoked.data["isActive"])
        reissued = self.client.post("/api/product-licenses", self.payload, format="json")
        self.assertEqual(reissued.status_code, 201, reissued.data)
        number_only = self.client.post("/api/product-licenses", {
            "productId": self.product.pk, "licenseNumber": "NUMBER-ONLY",
        }, format="json")
        self.assertEqual(number_only.status_code, 201, number_only.data)
        self.assertFalse(number_only.data["hasKey"])
        self.assertEqual(ProductLicense.objects.count(), 3)

    def test_invalid_product_dates_and_missing_identity_are_rejected(self):
        stock = Product.objects.create(
            sku="STOCK-01", name_en="Hardware", category=self.product.category,
            unit=self.product.unit, product_type="stock", cost_price=0, base_price=1,
        )
        for change in (
            {"productId": stock.pk},
            {"activationDate": "2027-10-01", "expiryDate": "2026-10-01"},
            {"licenseKey": "", "licenseNumber": ""},
        ):
            with self.subTest(change=change):
                rejected = self.client.post("/api/product-licenses", {
                    **self.payload, **change,
                }, format="json")
                self.assertEqual(rejected.status_code, 400, rejected.data)
                self.assertEqual(ProductLicense.objects.count(), 0)

    def test_read_only_grant_cannot_reveal_or_write_key(self):
        created = self.client.post("/api/product-licenses", self.payload, format="json")
        self.assertEqual(created.status_code, 201, created.data)
        license_id = created.data["id"]
        reader = User.objects.create_user(
            username="license-reader", email="license-reader@example.test", password="StrongPass123!"
        )
        role = Role.objects.create(name="License Reader")
        permission, _ = AccessPermission.objects.get_or_create(
            code="product-licenses.view", defaults={"name": "Licenses View"}
        )
        role.permissions.add(permission)
        reader.roles.add(role)
        self.client.force_authenticate(user=reader)

        listed = self.client.get("/api/product-licenses", {"productId": self.product.pk})
        self.assertEqual(listed.status_code, 200, listed.data)
        self.assertNotIn("licenseKey", listed.data[0])
        self.assertEqual(self.client.get(
            f"/api/product-licenses/{license_id}/reveal").status_code, 403)
        self.assertEqual(self.client.post(
            "/api/product-licenses", self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(
            f"/api/product-licenses/{license_id}").status_code, 403)
        self.assertEqual(ProductLicense.objects.count(), 1)

    def test_session_create_requires_csrf(self):
        session_client = APIClient(enforce_csrf_checks=True)
        session_client.force_login(self.admin)
        response = session_client.post("/api/product-licenses", self.payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertFalse(ProductLicense.objects.exists())
