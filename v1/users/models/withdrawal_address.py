from uuid import uuid4

from django.db import models

from v1.third_party.tnbCrow.constants import VERIFY_KEY_LENGTH
from v1.third_party.tnbCrow.models import CreatedModified

from .users import User

from v1.core.models.asset import Asset


class WithdrawalAddress(CreatedModified):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    memo = models.CharField(max_length=255)
    address = models.CharField(max_length=VERIFY_KEY_LENGTH)

    def __str__(self):
        return f"{self.user.username}: {self.address}"
