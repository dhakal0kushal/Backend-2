from django.contrib import admin
from .models import Exchange, TransactionType, PaymentMethod, Currency, Country, TnbcrowConstant

# Register your models here.
admin.site.register(Exchange)
admin.site.register(TransactionType)
admin.site.register(Currency)
admin.site.register(TnbcrowConstant)
admin.site.register(PaymentMethod)
admin.site.register(Country)
