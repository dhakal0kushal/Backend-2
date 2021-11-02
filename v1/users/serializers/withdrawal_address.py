from rest_framework import serializers

from ..models.withdrawal_address import WithdrawalAddress

from ..utils import validate_address


class WithdrawalAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = WithdrawalAddress
        fields = ('uuid', 'asset', 'title', 'memo', 'address', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at'

    def validate(self, attrs):

        if not validate_address(attrs['asset'].symbol, attrs['address']):
            error = {'error': 'Invalid withdrawal address.'}
            raise serializers.ValidationError(error)

        if WithdrawalAddress.objects.filter(asset=attrs['asset'], user=self.context['request'].user, address=attrs['address']).exists():
            error = {'error': 'You have added the address already.'}
            raise serializers.ValidationError(error)

        return super().validate(attrs)
