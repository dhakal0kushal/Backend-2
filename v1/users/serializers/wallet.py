from rest_framework import serializers

from ..models.wallets import Wallet


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['asset', 'balance', 'locked']
        depth = 1
