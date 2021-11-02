from django.contrib import admin

from .models.order import Order
from .models.advertisement import Advertisement

# Register your models here.
admin.site.register(Advertisement)
admin.site.register(Order)
