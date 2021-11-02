from django.db import models


# Exchange model will hold the value of TNBC in different exchanges
# that will be avaiable in future
class Exchange(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}: {self.price}'


# This model will contain the type of transaction that the user will use
# Eg: Cryptocurrency, Fiat Exchange, Online Purchases
class TransactionType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# This model consists the payment method that will be avaialble for
# the TransactionType. Eg: For Crypto, it will have bitcoin, litecoin and
# for Fiat, we will have USD, EUR and so on
class PaymentMethod(models.Model):
    type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ['type', 'name']

    def __str__(self):
        return f'{self.type.name}: {self.name}'


# The type of currency that the user is using to send or recieve the payment
class Currency(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f'{self.name}'


# We will hold the fee in this model instead of hardcoding it.
class TnbcrowConstant(models.Model):
    title = models.CharField(max_length=255, unique=True)
    transaction_fee = models.IntegerField()  # 100 here = 1%
    minimum_escrow_amount = models.IntegerField()
    maximum_escrow_amount = models.IntegerField()
    bank_ip = models.CharField(max_length=255)
    check_tnbc_confirmation = models.BooleanField()

    def __str__(self):
        return f'Fee: {self.transaction_fee/100}; Minimum: {self.minimum_escrow_amount}; Maximum: {self.maximum_escrow_amount}'


# This model will list all the countries in the world with the alpha and phone codes
class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    alpha_two_code = models.CharField(max_length=2)
    alpha_three_code = models.CharField(max_length=3)
    phone_code = models.CharField(max_length=6)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f'{self.alpha_two_code}: {self.name}'
