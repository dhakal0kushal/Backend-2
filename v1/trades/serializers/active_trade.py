from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from rest_framework import serializers

from ..models.active_trade import ActiveTrade
from ..models.trade_post import Advertisement


class ActiveTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveTrade
        fields = ('uuid', 'amount', 'initiator_confirmed', 'owner_confirmed', 'created_at', 'updated_at', 'status')
        read_only_fields = 'created_at', 'updated_at', 'post', 'amount'

    @transaction.atomic
    def update(self, instance, validated_data):
        context = self.context['request']
        payment_windows_expires_at = instance.created_at + timedelta(minutes=instance.payment_windows)

        if self.instance.status == ActiveTrade.COMPLETED or self.instance.status == ActiveTrade.ADMIN_COMPLETED or self.instance.status == ActiveTrade.OWNER_CANCELLED or self.instance.status == ActiveTrade.INITIATOR_CANCELLED or self.instance.status == ActiveTrade.ADMIN_CANCELLED:
            error = {'error': 'You cannot undo the action'}
            raise serializers.ValidationError(error)

        if 'status' in context.data:
            if context.data['status'] == str(ActiveTrade.COMPLETED) or context.data['status'] == str(ActiveTrade.ADMIN_COMPLETED) or context.data['status'] == str(ActiveTrade.ADMIN_CANCELLED):
                error = {'error': 'You cannot set this status'}
                raise serializers.ValidationError(error)
            elif payment_windows_expires_at > timezone.now():
                if (instance.post.owner_role == Advertisement.BUYER and context.data['status'] == str(ActiveTrade.INITIATOR_CANCELLED)) or (instance.post.owner_role == Advertisement.SELLER and context.data['status'] == str(ActiveTrade.OWNER_CANCELLED)):
                    error = {'error': 'Payment window must expire before cancelling the ActiveTrade'}
                    raise serializers.ValidationError(error)

        instance = super(ActiveTradeSerializer, self).update(instance, validated_data)
        if instance.initiator_confirmed and instance.owner_confirmed:
            user = self.context['request'].user
            user.loaded += instance.amount
            user.locked -= instance.amount
            user.save()
        return instance
