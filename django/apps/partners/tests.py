from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import AccessPermission, Role, User
from .models import Customer, PartnerDocument, Supplier


class PartnerApiTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="partner-admin", email="partner-admin@example.test", password="StrongPass123!"
        )
        self.employee = User.objects.create_user(
            username="partner-staff", email="partner-staff@example.test", password="StrongPass123!"
        )
        self.client = APIClient()
        self.customer = {
            "code": "c-001", "nameEn": "Al Noor", "nameAr": "النور",
            "addressAr": "مدينة الكويت", "customerType": "corporate",
            "paymentTermsDays": 30, "creditLimit": "2500.750", "civilId": "123456",
            "companyName": "Al Noor IT", "contactPerson": "Ali", "telephone": "22223333",
            "email": "sales@example.test", "taxNumber": "VAT-123",
            "openingBalance": "15.250", "remarks": "First order",
        }
        self.supplier = {
            "code": "s-001", "nameEn": "Supplier", "nameAr": "المورد",
            "paymentTermsDays": 14, "openingBalance": "135.500",
            "creditLimit": "800.500", "contactPerson": "Omar",
            "telephone": "22221111", "remarks": "Monthly terms",
        }


    def test_arabic_diacritics_round_trip(self):
        self.client.force_authenticate(user=self.admin)
        name_ar = "مُعَدّات الحاسوب — الكويت"
        address_ar = "شارع ١٢، بناية A-4"
        payload = {
            **self.customer,
            "code": "C-UNICODE-01",
            "nameAr": name_ar,
            "addressAr": address_ar,
            "creditLimit": "1234.375",
        }
        created = self.client.post("/api/customers", payload, format="json")
        self.assertEqual(created.status_code, 201, created.data)

        detail = self.client.get(f"/api/customers/{created.data['id']}")
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.data["nameAr"], name_ar)
        self.assertEqual(detail.data["addressAr"], address_ar)
        self.assertEqual(detail.data["creditLimit"], "1234.375")

    def test_customer_credit_duplicate_and_validation(self):
        self.client.force_authenticate(user=self.admin)
        created = self.client.post("/api/customers", self.customer, format="json")
        self.assertEqual(created.status_code, 201, created.data)
        item = Customer.objects.get(pk=created.data["id"])
        self.assertEqual((item.code, item.name_ar, item.credit_limit),
                         ("C-001", "النور", Decimal("2500.750")))
        self.assertEqual((item.company_name, item.opening_balance, item.tax_number),
                         ("Al Noor IT", Decimal("15.250"), "VAT-123"))
        self.assertEqual(self.client.post("/api/customers", {
            **self.customer, "code": "C-001"
        }, format="json").status_code, 400)
        for changes in ({"creditLimit": "-1.000"}, {"paymentTermsDays": 366}):
            self.assertEqual(self.client.post("/api/customers", {
                **self.customer, "code": "C-002", **changes
            }, format="json").status_code, 400)
        self.assertEqual(Customer.objects.count(), 1)
        blank_email = self.client.post("/api/customers", {
            **self.customer, "code": "C-EMPTY-EMAIL", "email": "",
        }, format="json")
        self.assertEqual(blank_email.status_code, 201, blank_email.data)
        invalid_email = self.client.post("/api/customers", {
            **self.customer, "code": "C-BAD-EMAIL", "email": "not-an-email",
        }, format="json")
        self.assertEqual(invalid_email.status_code, 400)

    def test_supplier_balance_and_duplicate(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/api/suppliers", self.supplier, format="json")
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Supplier.objects.get(pk=response.data["id"]).opening_balance,
                         Decimal("135.500"))
        self.assertEqual(response.data["creditLimit"], "800.500")
        self.assertEqual(self.client.post("/api/suppliers", self.supplier, format="json").status_code, 400)
        blank_email = self.client.post("/api/suppliers", {
            **self.supplier, "code": "S-EMPTY-EMAIL", "email": "",
        }, format="json")
        self.assertEqual(blank_email.status_code, 201, blank_email.data)
        invalid_email = self.client.post("/api/suppliers", {
            **self.supplier, "code": "S-BAD-EMAIL", "email": "not-an-email",
        }, format="json")
        self.assertEqual(invalid_email.status_code, 400)


    def test_partner_codes_use_the_same_ascii_policy_as_aspnet(self):
        self.client.force_authenticate(user=self.admin)
        for path, payload in (
            ("/api/customers", self.customer),
            ("/api/suppliers", self.supplier),
        ):
            with self.subTest(path=path):
                response = self.client.post(path, {
                    **payload,
                    "code": "رمز-١",
                    "nameAr": "المورّد",
                }, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn("code", response.data)

    def test_customer_optional_details_update_round_trip(self):
        self.client.force_authenticate(user=self.admin)
        created = self.client.post("/api/customers", self.customer, format="json")
        self.assertEqual(created.status_code, 201, created.data)
        identifier = created.data["id"]
        original = self.client.get(f"/api/customers/{identifier}")
        self.assertEqual(original.data["contactPerson"], "Ali")
        self.assertEqual(original.data["openingBalance"], "15.250")

        updated = self.client.put(f"/api/customers/{identifier}", {
            **self.customer, "companyName": "Updated IT",
            "contactPerson": "Sara", "openingBalance": "21.375",
        }, format="json")
        self.assertEqual(updated.status_code, 200, updated.data)
        self.assertEqual(updated.data["companyName"], "Updated IT")
        self.assertEqual(updated.data["openingBalance"], "21.375")
        self.assertEqual(Customer.objects.get(pk=identifier).contact_person, "Sara")

        invalid = self.client.put(f"/api/customers/{identifier}", {
            **self.customer, "email": "not an email",
        }, format="json")
        self.assertEqual(invalid.status_code, 400)
        self.assertEqual(self.client.get(f"/api/customers/{identifier}").data["companyName"], "Updated IT")

    def test_supplier_optional_details_update_round_trip(self):
        self.client.force_authenticate(user=self.admin)
        created = self.client.post("/api/suppliers", self.supplier, format="json")
        self.assertEqual(created.status_code, 201, created.data)
        identifier = created.data["id"]
        self.assertEqual(created.data["creditLimit"], "800.500")

        updated = self.client.put(f"/api/suppliers/{identifier}", {
            **self.supplier, "creditLimit": "950.125",
            "contactPerson": "Fatima", "remarks": "Revised terms",
        }, format="json")
        self.assertEqual(updated.status_code, 200, updated.data)
        self.assertEqual(updated.data["creditLimit"], "950.125")
        self.assertEqual(Supplier.objects.get(pk=identifier).contact_person, "Fatima")

        invalid = self.client.put(f"/api/suppliers/{identifier}", {
            **self.supplier, "creditLimit": "-1.000",
        }, format="json")
        self.assertEqual(invalid.status_code, 400)
        self.assertEqual(self.client.get(f"/api/suppliers/{identifier}").data["creditLimit"], "950.125")

    def test_civil_id_hidden_from_nonadmin(self):
        self.client.force_authenticate(user=self.admin)
        self.client.post("/api/customers", self.customer, format="json")
        role = Role.objects.create(name="Customer Reader")
        role.permissions.add(AccessPermission.objects.get(code="customers.view"))
        self.employee.roles.add(role)
        self.client.force_authenticate(user=self.employee)
        result = self.client.get("/api/customers")
        self.assertEqual(result.status_code, 200)
        self.assertNotIn("civilId", result.data[0])
        self.assertEqual(self.client.post("/api/customers", self.customer, format="json").status_code, 403)
        self.assertEqual(self.client.get("/api/customers/1/documents").status_code, 403)

    def test_secure_upload_download_and_corrupt_rejection(self):
        self.client.force_authenticate(user=self.admin)
        created = self.client.post("/api/customers", self.customer, format="json")
        url = f"/api/customers/{created.data['id']}/documents"
        bad = self.client.post(url, {"file": SimpleUploadedFile(
            "bad.pdf", b"garbage", content_type="application/pdf"
        )}, format="multipart")
        self.assertEqual(bad.status_code, 400)
        good = self.client.post(url, {"file": SimpleUploadedFile(
            "civil.pdf", b"%PDF-1.4\nsecret", content_type="application/pdf"
        )}, format="multipart")
        self.assertEqual(good.status_code, 201, good.data)
        document_id = good.data["id"]
        self.assertEqual(PartnerDocument.objects.count(), 1)
        self.assertEqual(self.client.get(f"{url}/{document_id}").content, b"%PDF-1.4\nsecret")
        self.client.force_authenticate(user=self.employee)
        self.assertEqual(self.client.get(f"{url}/{document_id}").status_code, 403)
