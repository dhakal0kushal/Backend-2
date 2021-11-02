from django.contrib import admin

from .models.active_trade import ActiveTrade
from .models.advertisement import Advertisement

# Register your models here.
admin.site.register(Advertisement)
admin.site.register(ActiveTrade)
