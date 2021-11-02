from uuid import uuid4

from django.db import models

from v1.users.models.users import User
from v1.constants.models import Currency, PaymentMethod


class Advertisement(models.Model):
    BUYER = 'BUYER'
    SELLER = 'SELLER'

    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller')
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()

    amount = models.PositiveIntegerField()
    payment_windows = models.PositiveIntegerField()

    terms_of_trade = models.TextField()
    min_reputation = models.IntegerField()

    broadcast_trade = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.uuid}: {self.is_active}'
