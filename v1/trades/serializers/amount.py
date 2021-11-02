from rest_framework import serializers

from ..models.advertisement import Advertisement


class AmountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advertisement
        fields = ('amount', )
