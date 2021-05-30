from django.contrib import admin
from .models import ChainScanTracker, TransactionHistory

# Register your models here.
admin.site.register(ChainScanTracker)
admin.site.register(TransactionHistory)
