from django.test import TestCase

from .models import DocumentSequence
from .numbering import next_number


class DocumentSequenceTests(TestCase):
    def test_increments_without_repeating(self):
        self.assertEqual(next_number("INV", 2026), 1)
        self.assertEqual(next_number("INV", 2026), 2)
        self.assertEqual(DocumentSequence.objects.count(), 1)

    def test_scopes_are_independent(self):
        self.assertEqual(next_number("INV", 2026, branch_id=1), 1)
        self.assertEqual(next_number("INV", 2026, branch_id=2), 1)
        self.assertEqual(next_number("INV", 2027, branch_id=1), 1)
        self.assertEqual(next_number("PO", 2026, branch_id=1), 1)

    def test_series_is_validated(self):
        with self.assertRaises(ValueError):
            next_number("bad key!", 2026)
        with self.assertRaises(ValueError):
            next_number("INV", 2026, -1)
        with self.assertRaises(ValueError):
            next_number("INV", 1999)
        self.assertFalse(DocumentSequence.objects.exists())
