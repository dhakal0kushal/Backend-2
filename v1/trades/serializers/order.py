from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from rest_framework import serializers

from ..models.order import Order
from ..models.advertisement import Advertisement


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('uuid', 'taker', 'maker', 'amount', 'rate', 'fee', 'advertisement',
                  'payment_windows', 'terms_of_trade', 'payment_method', 'status',
                  'created_at', 'updated_at')
        read_only_fields = 'taker', 'maker', 'amount', 'rate', 'fee', 'advertisement', 'payment_windows', 'terms_of_trade', 'payment_method', 'status', 'created_at', 'updated_at'
