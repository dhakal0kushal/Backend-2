from uuid import uuid4

from django.db import models

from v1.users.models.users import User


class UserTransaction(models.Model):

    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"

    TYPE_CHOICES = [
        (WITHDRAW, 'Withdraw'),
        (DEPOSIT, 'Deposit')
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
