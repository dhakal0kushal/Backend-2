from uuid import uuid4

from django.db import models

from v1.third_party.tnbCrow.constants import VERIFY_KEY_LENGTH
from v1.third_party.tnbCrow.models import CreatedModified
from .users import User


# Assigns the users with their respective wallets.
# M-T-O with User model
class Wallet(CreatedModified):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    account_number = models.CharField(max_length=VERIFY_KEY_LENGTH)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.username}: {self.account_number}: {self.is_primary}"
