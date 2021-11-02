import uuid
import random

from django.db import models

from .users import User

from v1.core.models.asset import Asset


class Wallet(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    balance = models.BigIntegerField(default=0)
    locked = models.BigIntegerField(default=0)

    memo = models.CharField(max_length=255, null=True, blank=True)

    deposit_address = models.CharField(max_length=255, null=True, blank=True)

    def get_available_balance(self):
        return self.balance - self.locked

    def __str__(self):
        return f"{self.user}; {self.asset} - {self.get_available_balance()}"


def generate_memo(instance):

    while True:

        memo = str(random.randint(100000, 999999))

        if not Wallet.objects.filter(memo=memo).exists():
            return memo


def pre_save_post_receiver(sender, instance, *args, **kwargs):

    if not instance.memo:
        instance.memo = generate_memo(instance)


models.signals.pre_save.connect(pre_save_post_receiver, sender=Wallet)
