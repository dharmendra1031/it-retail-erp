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

    def test_user_with_admin_role_can_manage_roles(self):
        admin_role, _ = Role.objects.get_or_create(name="Admin")
        self.employee.roles.add(admin_role)
        self.client.force_authenticate(user=self.employee)
        response = self.client.post("/api/roles", {"name": "Warehouse"}, format="json")
        self.assertEqual(response.status_code, 201)

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
        self.assertIn("Senior Cashier", [role["name"] for role in listing.data])

        deleted = self.client.delete(f"/api/roles/{role_id}")
        self.assertEqual(deleted.status_code, 204)
        self.assertFalse(Role.objects.filter(pk=role_id).exists())

    def test_duplicate_role_name_is_rejected(self):
        Role.objects.create(name="Manager")
        self.authenticate_as_admin()
        response = self.client.post("/api/roles", {"name": "manager"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "Role name already exists."})

    def test_assigned_role_cannot_be_deleted(self):
        role = Role.objects.create(name="Cashier")
        self.employee.roles.add(role)
        self.authenticate_as_admin()
        response = self.client.delete(f"/api/roles/{role.id}")
        self.assertEqual(response.status_code, 409)
        self.assertTrue(Role.objects.filter(pk=role.id).exists())

    def test_admin_role_cannot_be_changed_or_deleted(self):
        role, _ = Role.objects.get_or_create(name="Admin")
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


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cashier", email="cashier@example.com", password="TestPass123!"
        )
        self.client = APIClient()

    def test_invalid_password_locks_account_after_five_attempts(self):
        for _ in range(5):
            response = self.client.post(
                "/api/auth/login",
                {"email": "cashier@example.com", "password": "incorrect"},
                format="json",
            )
            self.assertEqual(response.status_code, 401)

        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 5)
        self.assertIsNotNone(self.user.locked_until)
        self.assertEqual(
            self.client.post("/api/auth/login", {
                "email": self.user.email, "password": "TestPass123!"
            }, format="json").status_code, 401
        )

    def test_expired_lock_resets_on_success(self):
        from datetime import timedelta
        from django.utils import timezone

        self.user.failed_login_attempts = 5
        self.user.locked_until = timezone.now() - timedelta(minutes=1)
        self.user.save(update_fields=["failed_login_attempts", "locked_until"])
        response = self.client.post("/api/auth/login", {
            "email": self.user.email, "password": "TestPass123!"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.failed_login_attempts, 0)
        self.assertIsNone(self.user.locked_until)

    def test_anonymous_and_expired_session_cannot_access_company(self):
        self.assertEqual(self.client.get("/api/companies").status_code, 401)
        self.client.force_login(self.user)
        self.assertEqual(self.client.get("/api/companies").status_code, 200)
        self.client.logout()
        self.assertEqual(self.client.get("/api/companies").status_code, 401)

    def test_csrf_is_required_for_login_and_logout(self):
        client = APIClient(enforce_csrf_checks=True)
        payload = {"email": self.user.email, "password": "TestPass123!"}
        self.assertEqual(client.post("/api/auth/login", payload, format="json").status_code, 403)

        token_response = client.get("/api/auth/csrf")
        token = token_response.data["csrfToken"]
        self.assertEqual(client.post(
            "/api/auth/login", payload, format="json", HTTP_X_CSRF_TOKEN=token
        ).status_code, 200)
        self.assertEqual(client.post("/api/auth/logout").status_code, 403)
        fresh_token = client.get("/api/auth/csrf").data["csrfToken"]
        self.assertEqual(client.post(
            "/api/auth/logout", HTTP_X_CSRF_TOKEN=fresh_token
        ).status_code, 204)

    def test_remember_me_sets_session_expiry(self):
        response = self.client.post("/api/auth/login", {
            "email": self.user.email, "password": "TestPass123!", "rememberMe": True
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(self.client.session.get_expiry_age(), 1800, delta=5)

    def test_missing_or_invalid_login_details_are_rejected(self):
        self.assertEqual(self.client.post("/api/auth/login", {
            "email": self.user.email, "password": ""
        }, format="json").status_code, 400)
        self.assertEqual(self.client.post("/api/auth/login", {
            "email": self.user.email, "password": "TestPass123!", "rememberMe": "false"
        }, format="json").status_code, 400)


class EmailIntegrityTests(TestCase):
    def test_user_email_unique_at_database_level(self):
        from django.db import IntegrityError, transaction

        User.objects.create_user(username="unique1", email="unique@example.com", password="TestPass123!")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(username="unique2", email="unique@example.com", password="TestPass123!")


class AdminBootstrapTests(TestCase):
    def test_seed_admin_is_idempotent(self):
        from io import StringIO
        from unittest.mock import patch
        from django.core.management import call_command

        with patch.dict("os.environ", {
            "ERP_ADMIN_EMAIL": "bootstrap@example.com",
            "ERP_ADMIN_PASSWORD": "TestPass123!",
        }):
            call_command("seed_admin", stdout=StringIO())
            call_command("seed_admin", stdout=StringIO())

        admin = User.objects.get(email="bootstrap@example.com")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.roles.filter(name="Admin").exists())
        self.assertEqual(User.objects.filter(email="bootstrap@example.com").count(), 1)

    def test_seed_admin_rejects_missing_credentials(self):
        from io import StringIO
        from unittest.mock import patch
        from django.core.management import call_command
        from django.core.management.base import CommandError

        with patch.dict("os.environ", {
            "ERP_ADMIN_EMAIL": "",
            "ERP_ADMIN_PASSWORD": "",
        }):
            with self.assertRaises(CommandError):
                call_command("seed_admin", stdout=StringIO())


class AccountSchemaTests(TestCase):
    def test_role_assignment_requires_real_role(self):
        from django.db import IntegrityError, transaction

        user = User.objects.create_user(
            username="orphan-check", email="orphan@example.com", password="TestPass123!"
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.roles.through.objects.create(user_id=user.id, role_id=999999999)

    def test_admin_seed_is_idempotent(self):
        from django.core.management import call_command
        from unittest.mock import patch

        with patch.dict("os.environ", {
            "ERP_ADMIN_EMAIL": "bootstrap@example.com",
            "ERP_ADMIN_PASSWORD": "StrongTestPassword123!",
        }):
            call_command("seed_admin")
            call_command("seed_admin")

        admin = User.objects.get(email="bootstrap@example.com")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.roles.filter(name="Admin").exists())
        self.assertTrue(admin.check_password("StrongTestPassword123!"))
        self.assertEqual(User.objects.filter(email=admin.email).count(), 1)
