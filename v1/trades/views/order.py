from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Q

from ..serializers.order import OrderSerializer

from ..models.order import Order
from ..models.advertisement import Advertisement

from ..permissions import IsOrderMaker, IsOrderTaker, OrderIsOpen

from v1.users.utils import get_tnbc_asset, get_or_create_wallet


class OrderViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    def get_queryset(self):
        return Order.objects.filter(Q(taker=self.request.user) | Q(maker=self.request.user))

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    @action(methods=['post'], detail=True, permission_classes=[IsOrderTaker, OrderIsOpen])
    def cancel(self, request, **kwargs):

        obj = self.get_object()

        obj.status = Order.TAKER_CANCELLED
        obj.save()

        order_amount = obj.amount + obj.fee
        obj.advertisement.amount += order_amount
        obj.advertisement.fee = obj.fee
        obj.advertisement.save()

        serialized_order = OrderSerializer(obj)

        return Response(serialized_order.data, status=status.HTTP_201_CREATED)
    
    
    @action(methods=['post'], detail=True, permission_classes=[IsOrderMaker, OrderIsOpen])
    def release(self, request, **kwargs):

        obj = self.get_object()

        obj.status = Order.COMPLETED
        obj.save()

        asset = get_tnbc_asset()

        taker_wallet, created =  get_or_create_wallet(obj.taker, asset)
        taker_wallet.balance += obj.amount
        taker_wallet.save()

        maker_wallet, created = get_or_create_wallet(obj.maker, asset)
        maker_wallet.balance -= obj.amount + obj.fee
        maker_wallet.locked -= obj.amount + obj.fee
        maker_wallet.save()
        
        serialized_order = OrderSerializer(obj)
        
        return Response(serialized_order.data, status=status.HTTP_201_CREATED)
