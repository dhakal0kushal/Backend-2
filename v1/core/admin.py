from django.contrib import admin

from .models.scan_tracker import ScanTracker
from .models.transactions import Transaction


admin.site.register(ScanTracker)
admin.site.register(Transaction)
