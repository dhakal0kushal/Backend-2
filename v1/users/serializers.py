from django.db import transaction

from rest_framework import serializers

from .models import Wallet


class WalletCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ('uuid', 'account_number', 'is_primary', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at', 'is_primary',

    @transaction.atomic
    def create(self, validated_data):
        instance = super(WalletCreateSerializer, self).create(validated_data)
        if not Wallet.objects.filter(owner=self.context['request'].user, is_primary=True).exists():
            instance.is_primary = True
            instance.save()
        return instance
    
    def validate(self, attrs):
        if not len(attrs['account_number']) == 64:
            error = {'error': 'Invalid account number!'}
            raise serializers.ValidationError(error)
        return super().validate(attrs)
 
class WalletUpdateSerializer(WalletCreateSerializer):

    class Meta:
        model = Wallet
        fields = ('uuid', 'account_number', 'is_primary', 'created_at', 'updated_at')
        read_only_fields = 'created_at', 'updated_at'

    @transaction.atomic
    def update(self, instance, validated_data):
        data = self.context['request'].data
        if 'is_primary' in data:
            if data['is_primary'] == 'True':
                primary_wallets = Wallet.objects.filter(owner=self.context['request'].user, is_primary=True)
                for wallets in primary_wallets:
                    wallets.is_primary = False
                    wallets.save()
            else:
                validated_data.pop('is_primary', [])
                error = {'error': 'You cannot unset Primary Account Number'}
                raise serializers.ValidationError(error)
        instance = super(WalletUpdateSerializer, self).update(instance, validated_data)
        return instance
    
    def validate(self, attrs):
        if not len(attrs['account_number']) == 64:
            error = {'error': 'Invalid account number!'}
            raise serializers.ValidationError(error)
        return super().validate(attrs)
