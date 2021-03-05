import os

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

globals = settings.GLOBALS

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField()

    @classmethod
    def create(cls, user):
        if not user:
            return None

        if wallet := cls.get(user):
            return None
        else:
            wallet = cls.objects.create(user=user, balance=globals['min_balance'])
            wallet.save()
            wallet.log(f"created with {globals['min_balance']} balance")
            return wallet

    @classmethod
    def get(cls, user):
        if not user:
            return None
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None

    def get_balance(self):
        return self.balance

    def validate_amount(self, amount):
        if type(amount) is not int:
            raise TypeError('invalid amount')
        if amount <= 0:
            raise ValueError('invalid amount')

    def debit(self, amount):
        try:
            self.validate_amount(amount)
        except Exception:
            self.log(f'debit transaction failed due to invalid amount: {amount}')
            raise

        if self.balance - amount < globals['min_balance']:
            self.log(f'debit transaction of {amount} failed due to insufficient balance')
            raise ValidationError('balance less than minimum required')
        self.balance -= amount
        self.save()
        self.log(f'debited {amount}')

    def credit(self, amount):
        try:
            self.validate_amount(amount)
        except Exception:
            self.log(f'credit transaction failed due to invalid amount: {amount}')
            raise

        self.balance += amount
        self.save()
        self.log(f'credited {amount}')

    def get_log_file(self):
        return os.path.join(settings.LOGS_DIR, f'wallet{self.id}.log')

    def log(self, message):
        with open(self.get_log_file(), 'a') as f:
            f.write(f'[{timezone.now()}]\t{message}\n')
