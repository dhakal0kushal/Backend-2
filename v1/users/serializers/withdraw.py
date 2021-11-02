from rest_framework import serializers

from ..models.withdrawal_address import WithdrawalAddress


class WithdrawTNBCSerializer(serializers.ModelSerializer):

    amount = serializers.IntegerField()
    symbol = serializers.CharField(source='asset.symbol')

    class Meta:
        model = WithdrawalAddress
        fields = ['symbol', 'address', 'amount']
