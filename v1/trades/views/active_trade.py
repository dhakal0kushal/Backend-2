from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from ..serializers.active_trade import ActiveTradeSerializer

from ..models.active_trade import ActiveTrade

from ..permissions import OrderBuyer, OrderSeller


class ActiveTradeViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):

    def get_queryset(self):
        return ActiveTrade.objects.filter(Q(initiator=self.request.user) | Q(post__owner=self.request.user))

    serializer_class = ActiveTradeSerializer

    def get_permissions(self):
        data = self.request.data
        if 'status' in data:
            if data['status'] == str(ActiveTrade.SELLER_CANCELLED):
                return [OrderSeller(), ]
            elif data['status'] == str(ActiveTrade.BUYER_CANCELLED):
                return [OrderBuyer(), ]
        if 'initiator_confirmed' in data and 'owner_confirmed' not in data:
            return [OrderBuyer(), ]
        elif 'owner_confirmed' in data and 'initiator_confirmed' not in data:
            return [OrderSeller(), ]
        else:
            return [IsAuthenticated(), ]
