from v1.core.models.asset import Asset

from rest_framework import serializers


class DepositSerializer(serializers.Serializer):

    symbol = serializers.CharField(max_length=255)
