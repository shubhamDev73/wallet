from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

MIN_BALANCE = 100

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField()

    @classmethod
    def create(cls, user):
        wallet = cls.objects.create(user=user, balance=MIN_BALANCE)
        wallet.save()
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
            raise ValidationError('balance less than minimum required')
        self.balance -= amount
        self.save()

    def credit(self, amount):
        self.balance += amount
        self.save()
