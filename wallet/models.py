import os

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

MIN_BALANCE = 100

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField()

    @classmethod
    def create(cls, user):
        wallet = cls.objects.create(user=user, balance=MIN_BALANCE)
        wallet.save()
        wallet.log(f'created with {MIN_BALANCE} balance')
        return wallet

    @classmethod
    def get(cls, user):
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return None

    def get_balance(self):
        return self.balance

    def debit(self, amount):
        if self.balance - amount < MIN_BALANCE:
            self.log(f'debit transaction failed. balance less than minimum required')
            raise ValidationError('balance less than minimum required')
        self.balance -= amount
        self.save()
        self.log(f'debited {amount}')

    def credit(self, amount):
        self.balance += amount
        self.save()
        self.log(f'credited {amount}')

    def get_log_file(self):
        return os.path.join(settings.LOGS_DIR, f'wallet{self.id}.log')

    def log(self, message):
        with open(self.get_log_file(), 'a') as f:
            f.write(f'[{timezone.now()}]\t{message}\n')
