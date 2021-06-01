from rest_framework import serializers


class WithdrawTNBCSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    account_number = serializers.CharField(max_length=64)
