from uuid import uuid4

from django.db import models

from v1.users.models import User


class ChainScanTracker(models.Model):
    total_scans = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.total_scans} at {self.updated_at}'


class TransactionHistory(models.Model):

    WITHDRAW = PENDING = 0
    DEPOSIT = COMPELTED = 1

    TYPE_CHOICES = [
        (WITHDRAW, 'Withdraw'),
        (DEPOSIT, 'Deposit')
    ]

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPELTED, 'Completed')
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.IntegerField(choices=TYPE_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
