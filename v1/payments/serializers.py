from rest_framework import serializers

from v1.users.models import Wallet


class WithdrawTNBCSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    account_number = serializers.CharField(max_length=64)
