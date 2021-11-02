from uuid import uuid4
from django.db import models

from v1.users.models.users import User
from v1.constants.models import PaymentMethod


class Order(models.Model):

    OPEN = 'OPEN'
    COMPLETED = 'COMPLETED'
    ADMIN_COMPLETED = 'ADMIN_COMPLETED'

    BUYER_CANCELLED = 'BUYER_CANCELLED'
    SELLER_CANCELLED = 'SELLER_CANCELLED'
    ADMIN_CANCELLED = 'ADMIN_CANCELLED'

    STATUS = [
        (OPEN, 'Open'),
        (COMPLETED, 'Completed'),
        (ADMIN_COMPLETED, 'Admin Completed'),
        (SELLER_CANCELLED, 'Seller Cancelled'),
        (BUYER_CANCELLED, 'Buyer Cancelled'),
        (ADMIN_CANCELLED, 'Admin Cancelled')
    ]

    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")

    amount = models.IntegerField()
    rate = models.PositiveIntegerField()
    fee = models.IntegerField()

    payment_windows = models.PositiveIntegerField()
    terms_of_trade = models.TextField()
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    status = models.CharField(max_length=255, choices=STATUS, default='OPEN')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post}'
