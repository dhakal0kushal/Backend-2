from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Q

from ..serializers.order import OrderSerializer

from ..models.order import Order
from ..models.advertisement import Advertisement

from ..permissions import IsOrderMaker, IsOrderTaker, OrderIsOpen


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
