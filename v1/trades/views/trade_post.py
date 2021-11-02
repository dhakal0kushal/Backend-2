from rest_framework import viewsets, mixins, status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from v1.third_party.tnbCrow.permissions import IsOwner
from v1.constants.models import TnbcrowConstant

from ..models.trade_post import Advertisement

from ..serializers.trade_post import AdvertisementSerializer
from ..serializers.amount import AmountSerializer


class AdvertisementViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny(), ]
        elif self.action == 'create':
            return [IsAuthenticated(), ]
        else:
            return [IsOwner(), ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['post'], detail=True)
    def load(self, request, **kwargs):

        obj = self.get_object()

        # self.serializer_class = AmountSerializer
        serializer = AmountSerializer(data=request.data)

        if serializer.is_valid():
            amount = int(request.data['amount'])
            if obj.owner_role == Advertisement.SELLER:
                if request.user.get_user_balance() > amount:
                    request.user.locked += amount
                    fee_percentage = TnbcrowConstant.objects.get(title="main").fee / 100
                    transaction_fee = int(amount * fee_percentage / 100)
                    final_amount = amount - transaction_fee
                    obj.amount += final_amount
                    obj.save()
                    request.user.save()
                else:
                    error = {'error': 'You donot have enough balance to load!!'}
                    raise serializers.ValidationError(error)
            else:
                obj.amount += amount
                obj.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def withdraw(self, request, **kwargs):

        obj = self.get_object()

        # self.serializer_class = AmountSerializer
        serializer = AmountSerializer(data=request.data)

        if serializer.is_valid():
            amount = int(request.data['amount'])
            if obj.amount >= amount:
                if obj.owner_role == Advertisement.SELLER:
                    fee_percentage = TnbcrowConstant.objects.get(title="main").fee / 100
                    final_amount = (amount * 100) / (100 - fee_percentage)
                    request.user.locked -= final_amount
                    obj.amount -= amount
                    obj.save()
                    request.user.save()
                else:
                    obj.amount -= amount
                    obj.save()
            else:
                error = {'error': 'Trade Post donot have enough coins to withdraw!!'}
                raise serializers.ValidationError(error)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
