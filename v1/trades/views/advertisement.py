from rest_framework import viewsets, mixins, status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from v1.third_party.tnbCrow.permissions import IsOwner
from v1.constants.models import TnbcrowConstant
from v1.users.utils import get_tnbc_asset, get_or_create_wallet

from ..models.advertisement import Advertisement
from ..models.order import Order

from ..serializers.advertisement import AdvertisementSerializer
from ..serializers.amount import AmountSerializer
from ..serializers.order import OrderSerializer


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

            fee_percentage = TnbcrowConstant.objects.get(title="main").escrow_fee
            fee = amount * fee_percentage / 100

            if obj.role == Advertisement.SELLER:

                asset = get_tnbc_asset()

                wallet, created = get_or_create_wallet(request.user, asset)

                if wallet.get_available_balance() >= amount:

                    wallet.locked += amount
                    wallet.save()

                    obj.amount += amount
                    obj.fee += fee
                    obj.save()

                else:
                    error = {'error': f'You only have {wallet.get_available_balance()} TNBC available.'}
                    raise serializers.ValidationError(error)

            else:
                obj.amount += amount
                obj.fee += fee
                obj.save()

            advertisement_serializer = AdvertisementSerializer(obj)
            return Response(advertisement_serializer.data, status=status.HTTP_201_CREATED)
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

                    wallet.locked -= amount
                    wallet.save()

                fee_percentage = TnbcrowConstant.objects.get(title="main").escrow_fee
                fee = amount * fee_percentage / 100

                obj.amount -= amount
                obj.fee -= fee
                obj.save()

            else:
                error = {'error': 'Advertisement do not have enough coins to withdraw!!'}
                raise serializers.ValidationError(error)

            advertisement_serializer = AdvertisementSerializer(obj)
            return Response(advertisement_serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def order(self, request, **kwargs):

        obj = self.get_object()
        serializer = AmountSerializer(data=request.data)

        if serializer.is_valid():

            amount = int(request.data['amount'])

            if obj.role == Advertisement.SELLER:

                advertisement_amount_without_fee = obj.amount - obj.fee

                if amount <= advertisement_amount_without_fee:

                    fee = amount / advertisement_amount_without_fee * obj.fee

                    obj.amount -= amount / advertisement_amount_without_fee * obj.amount
                    obj.fee -= fee
                    obj.save()

                    order = Order.objects.create(buyer=request.user,
                                                 seller=obj.owner,
                                                 fee=fee,
                                                 amount=amount,
                                                 rate=obj.rate,
                                                 payment_windows=obj.payment_windows,
                                                 terms_of_trade=obj.terms_of_trade,
                                                 payment_method=obj.payment_method)

                else:
                    error = {'error': f'There\'s only {advertisement_amount_without_fee} TNBC available on advertisement.'}
                    raise serializers.ValidationError(error)

            else:
                if amount <= obj.amount:

                    fee_percentage = TnbcrowConstant.objects.get(title="main").escrow_fee

                    fee = amount * fee_percentage / 100

                    obj.amount -= amount
                    obj.fee -= fee
                    obj.save()

                    order = Order.objects.create(buyer=obj.owner,
                                                 seller=request.user,
                                                 fee=fee,
                                                 amount=amount,
                                                 rate=obj.rate,
                                                 payment_windows=obj.payment_windows,
                                                 terms_of_trade=obj.terms_of_trade,
                                                 payment_method=obj.payment_method)

            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
