from django.test import TestCase

from ..management.commands.account_creation import Command
from ..models import User


class AccountCreationTestCase(TestCase):

    def test_spaced_name0(self):
        self._test_row([" Test Name", "test.name@example.com"],
                       "Test Name", "test.name@example.com")

    def test_spaced_name1(self):
        self._test_row(["Test Name ", "test.name@example.com"],
                       "Test Name", "test.name@example.com")

    def test_interesting_name(self):
        self._test_row(["Τεστ Ναμε", "test.name@example.com"],
                       "Τεστ Ναμε", "test.name@example.com")

    def test_spaced_email0(self):
        self._test_row(["Test Name", " test.name@example.com"],
                       "Test Name", "test.name@example.com")

    def test_spaced_email1(self):
        self._test_row(["Test Name", "test.name@example.com "],
                       "Test Name", "test.name@example.com")

    def test_capped_email0(self):
        self._test_row(["Test Name", "Test.Name@example.com"],
                       "Test Name", "test.name@example.com")

    def test_capped_email1(self):
        self._test_row(["Test Name", "TEST.NAME@EXAMPLE.COM"],
                       "Test Name", "test.name@example.com")

    def _test_row(self, row, expected_name, expected_email):
        Command()._handle_row(row)
        u = User.objects.get(pk=1)
        self.assertEqual(u.name, expected_name, row)
        self.assertEqual(u.email, expected_email, row)
