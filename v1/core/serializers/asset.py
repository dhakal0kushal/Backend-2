from rest_framework import serializers

from ..models.asset import Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['uuid', 'title', 'symbol']
