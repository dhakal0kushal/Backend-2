from django.contrib import admin

from .models.scan_tracker import ScanTracker
from .models.transactions import ThenewbostonTransaction
from .models.asset import Asset


admin.site.register(ScanTracker)
admin.site.register(ThenewbostonTransaction)
admin.site.register(Asset)
