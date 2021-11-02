from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from rest_framework import serializers

from ..models.order import Order
from ..models.advertisement import Advertisement


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('uuid', 'amount', 'created_at', 'updated_at', 'status', 'fee')
        read_only_fields = 'created_at', 'updated_at', 'post', 'amount'

    @transaction.atomic
    def update(self, instance, validated_data):
        context = self.context['request']
        payment_windows_expires_at = instance.created_at + timedelta(minutes=instance.payment_windows)

        if self.instance.status == Order.COMPLETED or self.instance.status == Order.ADMIN_COMPLETED or self.instance.status == Order.OWNER_CANCELLED or self.instance.status == Order.INITIATOR_CANCELLED or self.instance.status == Order.ADMIN_CANCELLED:
            error = {'error': 'You cannot undo the action'}
            raise serializers.ValidationError(error)

        if 'status' in context.data:
            if context.data['status'] == str(Order.COMPLETED) or context.data['status'] == str(Order.ADMIN_COMPLETED) or context.data['status'] == str(Order.ADMIN_CANCELLED):
                error = {'error': 'You cannot set this status'}
                raise serializers.ValidationError(error)
            elif payment_windows_expires_at > timezone.now():
                if (instance.post.owner_role == Advertisement.BUYER and context.data['status'] == str(Order.INITIATOR_CANCELLED)) or (instance.post.owner_role == Advertisement.SELLER and context.data['status'] == str(Order.OWNER_CANCELLED)):
                    error = {'error': 'Payment window must expire before cancelling the Order'}
                    raise serializers.ValidationError(error)

        instance = super(OrderSerializer, self).update(instance, validated_data)
        if instance.initiator_confirmed and instance.owner_confirmed:
            user = self.context['request'].user
            user.loaded += instance.amount
            user.locked -= instance.amount
            user.save()
        return instance
