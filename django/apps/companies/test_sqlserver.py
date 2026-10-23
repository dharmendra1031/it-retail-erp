import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.conf import settings
from django.db import IntegrityError, connection, connections, transaction
from django.test import TestCase, TransactionTestCase

from apps.accounts.models import Role, User
from .models import Company


@unittest.skipUnless(settings.DATABASES["default"]["ENGINE"] == "mssql", "SQL Server integration only")
class SqlServerSchemaTests(TestCase):
    def test_business_ids_are_bigint_identity(self):
        tables = ("companies_company", "accounts_user", "accounts_role")
        with connection.cursor() as cursor:
            for table in tables:
                with self.subTest(table=table):
                    cursor.execute(
                        "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                        "WHERE TABLE_NAME = %s AND COLUMN_NAME = 'id'", [table]
                    )
                    self.assertEqual(cursor.fetchone()[0].lower(), "bigint")
                    cursor.execute(
                        f"SELECT COLUMNPROPERTY(OBJECT_ID('{table}'), 'id', 'IsIdentity')"
                    )
                    self.assertEqual(cursor.fetchone()[0], 1)

    def test_english_and_arabic_columns_use_unicode(self):
        with connection.cursor() as cursor:
            for column in ("name_en", "name_ar", "address_en", "address_ar"):
                with self.subTest(column=column):
                    cursor.execute(
                        "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                        "WHERE TABLE_NAME='companies_company' AND COLUMN_NAME=%s", [column]
                    )
                    self.assertEqual(cursor.fetchone()[0].lower(), "nvarchar")

    def test_orphan_user_role_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.roles.through.objects.create(user_id=999999999, role_id=999999999)

    def test_arabic_company_values_round_trip(self):
        company = Company.objects.create(
            name_en="Store", name_ar="شركة التجزئة",
            address_ar="شارع المدينة", tax_number="TAX123"
        )
        company.refresh_from_db()
        self.assertEqual(company.name_ar, "شركة التجزئة")
        self.assertEqual(company.address_ar, "شارع المدينة")


@unittest.skipUnless(settings.DATABASES["default"]["ENGINE"] == "mssql", "SQL Server integration only")
class SqlServerRoleConcurrencyTests(TransactionTestCase):
    def test_simultaneous_role_insert_preserves_unique_name(self):
        barrier = Barrier(2)

        def create_role():
            connections["default"].close()
            try:
                barrier.wait(timeout=10)
                try:
                    Role.objects.create(name="ConcurrentCashier")
                    return True
                except IntegrityError:
                    return False
            finally:
                connections["default"].close()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: create_role(), range(2)))

        self.assertEqual(results.count(True), 1)
        self.assertEqual(Role.objects.filter(name="ConcurrentCashier").count(), 1)
