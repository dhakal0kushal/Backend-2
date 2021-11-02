from rest_framework import viewsets, mixins, status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from v1.third_party.tnbCrow.permissions import IsOwner
from v1.constants.models import TnbcrowConstant
from v1.users.utils import get_tnbc_asset, get_or_create_wallet

from ..models.advertisement import Advertisement

from ..serializers.advertisement import AdvertisementSerializer
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

        serializer = AmountSerializer(data=request.data)

        if serializer.is_valid():

            amount = int(request.data['amount'])

            if obj.role == Advertisement.SELLER:

                asset = get_tnbc_asset()

                wallet, created = get_or_create_wallet(request.user, asset)
    
                if wallet.get_available_balance() >= amount:

                    wallet.locked += amount
                    wallet.save()

                    fee_percentage = TnbcrowConstant.objects.get(title="main").escrow_fee / 100
                    final_amount = amount * (100 - fee_percentage) / 100

                    obj.amount += final_amount
                    obj.save()
                    
                else:
                    error = {'error': f'You only have {wallet.get_available_balance()} TNBC available.'}
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

        serializer = AmountSerializer(data=request.data)

        if serializer.is_valid():

            amount = int(request.data['amount'])

            if obj.amount >= amount:

                if obj.role == Advertisement.SELLER:

                    asset = get_tnbc_asset()
                    wallet, created = get_or_create_wallet(request.user, asset)

                    fee_percentage = TnbcrowConstant.objects.get(title="main").escrow_fee / 100
                    final_amount = amount * (100 + fee_percentage) / 100

                    wallet.locked -= final_amount
                    wallet.save()

                    obj.amount -= amount
                    obj.save()

                else:
                    obj.amount -= amount
                    obj.save()

            else:
                error = {'error': 'Advertisement do not have enough coins to withdraw!!'}
                raise serializers.ValidationError(error)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
