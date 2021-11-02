from rest_framework.permissions import IsAuthenticated
from rest_framework import status, mixins
from rest_framework import viewsets
from rest_framework.response import Response

from ..serializers.deposit import DepositSerializer

from v1.core.models.asset import Asset

from ..models.wallets import Wallet


class DepositViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = DepositSerializer

    def create(self, request, format=None):

        serializer = DepositSerializer(data=request.data)

        if serializer.is_valid():

            if Asset.objects.filter(symbol=serializer.data['symbol']).exists():

                asset = Asset.objects.get(symbol=serializer.data['symbol'])

                deposit_address = asset.deposit_address

                wallet, created = Wallet.objects.get_or_create(user=request.user,
                                                               asset=asset,
                                                               deposit_address=deposit_address)

                message = {
                    'address': wallet.deposit_address,
                    'memo': wallet.memo
                }

            else:
                error = {'error': 'No deposit address found for that particular symbol.'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(message, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
