from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

from .models import Wallet

globals = settings.GLOBALS

class WalletTestCase(TestCase):

    amount = 20

    @classmethod
    def setUpTestData(cls):
        cls.amount = abs(cls.amount)
        cls.user = User.objects.create_user(username='test', password='test_password')

    def setUp(self):
        self.wallet = Wallet.create(self.user)

    def test_get(self):
        self.assertEqual(self.wallet.id, Wallet.get(self.user).id)

    def test_get_not_exist(self):
        user = User.objects.create_user(username='test2', password='test_password2')
        self.assertIsNone(Wallet.get(user))

    def test_get_none_user(self):
        self.assertIsNone(Wallet.get(None))

    def test_create_none_user(self):
        self.assertIsNone(Wallet.create(None))

    def test_create_duplicate(self):
        self.assertIsNone(Wallet.create(self.user))

    def test_init_balance(self):
        self.assertEqual(self.wallet.balance, globals['min_balance'])

    def test_get_balance(self):
        self.assertEqual(self.wallet.balance, self.wallet.get_balance())

    def test_credit(self):
        init_balance = self.wallet.balance
        self.wallet.credit(self.amount)
        self.assertEqual(self.wallet.balance, init_balance + self.amount)

    def test_credit_none_amount(self):
        init_balance = self.wallet.balance
        with self.assertRaises(TypeError):
            self.wallet.credit(None)
        with self.subTest('balance_check'):
            self.assertEqual(self.wallet.balance, init_balance)

    def test_credit_invalid_amount(self):
        init_balance = self.wallet.balance
        with self.assertRaises(ValueError):
            self.wallet.credit(-self.amount)
        with self.subTest('balance_check'):
            self.assertEqual(self.wallet.balance, init_balance)

    def test_debit(self):
        self.wallet.credit(self.amount)
        init_balance = self.wallet.balance
        self.wallet.debit(self.amount)
        self.assertEqual(self.wallet.balance, init_balance - self.amount)

    def test_debit_none_amount(self):
        init_balance = self.wallet.balance
        with self.assertRaises(TypeError):
            self.wallet.debit(None)
        with self.subTest('balance_check'):
            self.assertEqual(self.wallet.balance, init_balance)

    def test_debit_invalid_amount(self):
        init_balance = self.wallet.balance
        with self.assertRaises(ValueError):
            self.wallet.debit(-self.amount)
        with self.subTest('balance_check'):
            self.assertEqual(self.wallet.balance, init_balance)

    def test_debit_insufficient_balance(self):
        while self.wallet.balance - self.amount >= globals['min_balance']:
            self.wallet.debit(self.amount)
        init_balance = self.wallet.balance
        with self.assertRaises(ValidationError):
            self.wallet.debit(self.amount)
        with self.subTest('balance_check'):
            self.assertEqual(self.wallet.balance, init_balance)
