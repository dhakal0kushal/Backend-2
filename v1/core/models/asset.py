import uuid

from django.db import models


class Asset(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    title = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255, unique=True)
    deposit_address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.symbol}"
