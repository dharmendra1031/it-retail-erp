import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.conf import settings
from django.db import connection, connections
from django.test import TransactionTestCase, TestCase

from .models import DocumentSequence
from .numbering import next_number


@unittest.skipUnless(settings.DATABASES["default"]["ENGINE"] == "mssql", "SQL Server only")
class DocumentSequenceSchemaTests(TestCase):
    def test_numeric_id_and_unique_key(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
                "WHERE TABLE_NAME = 'core_documentsequence' AND COLUMN_NAME = 'id'"
            )
            self.assertEqual(cursor.fetchone()[0].lower(), "bigint")
        self.assertEqual(next_number("INV", 2026), 1)


@unittest.skipUnless(settings.DATABASES["default"]["ENGINE"] == "mssql", "SQL Server only")
class DocumentSequenceConcurrencyTests(TransactionTestCase):
    def test_same_series_allocates_unique_monotonic_values(self):
        barrier = Barrier(5)

        def reserve(_):
            connections["default"].close()
            try:
                barrier.wait(timeout=15)
                return next_number("SALE", 2026, branch_id=1)
            finally:
                connections["default"].close()

        with ThreadPoolExecutor(max_workers=5) as executor:
            numbers = list(executor.map(reserve, range(5)))

        self.assertEqual(sorted(numbers), [1, 2, 3, 4, 5])
        self.assertEqual(DocumentSequence.objects.get(
            series="SALE", fiscal_year=2026, branch_id=1
        ).last_number, 5)
