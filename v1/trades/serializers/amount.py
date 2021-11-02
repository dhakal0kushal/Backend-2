from rest_framework import serializers

from ..models.trade_post import Advertisement


class AmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('amount', )
