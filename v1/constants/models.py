import uuid

from django.db import models


class Exchange(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}: {self.price}'


class TransactionType(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ['type', 'name']

    def __str__(self):
        return f'{self.type.name}: {self.name}'


class Currency(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f'{self.name}'


class TnbcrowConstant(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    title = models.CharField(max_length=255, unique=True)
    escrow_fee = models.IntegerField()  # 100 here = 1%
    minimum_escrow_amount = models.IntegerField()
    maximum_escrow_amount = models.IntegerField()
    bank_ip = models.CharField(max_length=255)
    check_tnbc_confirmation = models.BooleanField()

    def __str__(self):
        return f'Fee: {self.escrow_fee/100}; Minimum: {self.minimum_escrow_amount}; Maximum: {self.maximum_escrow_amount}'


class Country(models.Model):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    name = models.CharField(max_length=255, unique=True)
    alpha_two_code = models.CharField(max_length=2)
    alpha_three_code = models.CharField(max_length=3)
    phone_code = models.CharField(max_length=6)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f'{self.alpha_two_code}: {self.name}'
