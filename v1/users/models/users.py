import uuid
import random

from django.db import models
from django.contrib.auth.models import AbstractUser


# Holds the User info.
class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)

    first_name = None
    last_name = None

    memo = models.CharField(max_length=255, unique=True, editable=False)

    balance = models.IntegerField(default=0)  # TNBC balance
    locked = models.IntegerField(default=0)  # coins locked when creating tradePost or tradeRequest

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_available_balance(self):
        return self.balance - self.locked


# generate a random memo and check if its already taken.
# If taken, generate another memo again until we find a valid memo
def generate_memo(instance):

    while True:

        memo = str(random.randint(100000, 999999))

        if not User.objects.filter(memo=memo).exists():
            return memo


def pre_save_post_receiver(sender, instance, *args, **kwargs):

    if not instance.memo:
        instance.memo = generate_memo(instance)


# save the memo before the User model is saved with the unique memo
models.signals.pre_save.connect(pre_save_post_receiver, sender=User)
