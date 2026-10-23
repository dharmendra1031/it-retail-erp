from django.test import TestCase
from rest_framework.test import APIClient

from .models import Role, User


class RoleApiTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="TestPass123!"
        )
        self.employee = User.objects.create_user(
            username="employee", email="employee@example.com", password="TestPass123!"
        )
        self.client = APIClient()

    def authenticate_as_admin(self):
        self.client.force_authenticate(user=self.admin)

    def test_anonymous_cannot_list_roles(self):
        response = self.client.get("/api/roles")
        self.assertIn(response.status_code, (401, 403))

    def test_employee_cannot_list_roles(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.get("/api/roles")
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_update_and_delete_role(self):
        self.authenticate_as_admin()

        created = self.client.post("/api/roles", {"name": "Cashier"}, format="json")
        self.assertEqual(created.status_code, 201)
        role_id = created.data["id"]
        self.assertIsInstance(role_id, int)

        updated = self.client.put(
            f"/api/roles/{role_id}", {"name": "Senior Cashier"}, format="json"
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.data["name"], "Senior Cashier")

        listing = self.client.get("/api/roles")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.data[0]["name"], "Senior Cashier")

        deleted = self.client.delete(f"/api/roles/{role_id}")
        self.assertEqual(deleted.status_code, 204)
        self.assertFalse(Role.objects.filter(pk=role_id).exists())

    def test_duplicate_role_name_is_rejected(self):
        Role.objects.create(name="Manager")
        self.authenticate_as_admin()
        response = self.client.post("/api/roles", {"name": "manager"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_assigned_role_cannot_be_deleted(self):
        role = Role.objects.create(name="Cashier")
        self.employee.roles.add(role)
        self.authenticate_as_admin()
        response = self.client.delete(f"/api/roles/{role.id}")
        self.assertEqual(response.status_code, 409)
        self.assertTrue(Role.objects.filter(pk=role.id).exists())

    def test_admin_role_cannot_be_changed_or_deleted(self):
        role = Role.objects.create(name="Admin")
        self.authenticate_as_admin()
        self.assertEqual(
            self.client.put(f"/api/roles/{role.id}", {"name": "Other"}, format="json").status_code,
            400,
        )
        self.assertEqual(self.client.delete(f"/api/roles/{role.id}").status_code, 400)

    def test_role_name_is_required(self):
        self.authenticate_as_admin()
        response = self.client.post("/api/roles", {"name": "  "}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_role_name_max_length(self):
        self.authenticate_as_admin()
        response = self.client.post("/api/roles", {"name": "X" * 101}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_missing_role_returns_404(self):
        self.authenticate_as_admin()
        self.assertEqual(self.client.get("/api/roles/9999").status_code, 404)
