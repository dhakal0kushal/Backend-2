from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from ..serializers.order import OrderSerializer

from ..models.order import Order

from ..permissions import OrderBuyer, OrderSeller


class OrderViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    def get_queryset(self):
        return Order.objects.filter(Q(initiator=self.request.user) | Q(post__owner=self.request.user))

    serializer_class = OrderSerializer

    def get_permissions(self):
        data = self.request.data
        if 'status' in data:
            if data['status'] == str(Order.SELLER_CANCELLED):
                return [OrderSeller(), ]
            elif data['status'] == str(Order.BUYER_CANCELLED):
                return [OrderBuyer(), ]
        if 'initiator_confirmed' in data and 'owner_confirmed' not in data:
            return [OrderBuyer(), ]
        elif 'owner_confirmed' in data and 'initiator_confirmed' not in data:
            return [OrderSeller(), ]
        else:
            return [IsAuthenticated(), ]
