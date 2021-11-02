from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, mixins

from v1.core.utils.send_tnbc import send_tnbc, estimate_fee
from v1.core.models.transactions import ThenewbostonTransaction
from v1.core.models.asset import Asset

from ..serializers.withdraw import WithdrawTNBCSerializer
from ..models.transactions import UserTransaction
from ..models.wallets import Wallet

from ..utils import validate_address


class WithdrawTNBCViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawTNBCSerializer

    def create(self, request, format=None):

        serializer = WithdrawTNBCSerializer(data=request.data)

        if serializer.is_valid():

            if Asset.objects.filter(symbol=serializer.data['symbol']).exists():
                asset = Asset.objects.get(symbol=serializer.data['symbol'])

            else:
                error = {'error': 'tnbCrow does not support withdrawal of that particular symbol.'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            wallet, created = Wallet.objects.get_or_create(user=request.user, asset=asset)

            address = serializer.data['address']
            amount = int(serializer.data['amount'])

            response, fee = estimate_fee()

            if not validate_address(asset.symbol, address):
                error = {'error': 'Invalid TNBC account number.'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            elif amount < 1:
                error = {'error': 'Sorry, you cannot withdraw less than 1 tnbc'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            elif amount + fee > wallet.get_available_balance():
                error = {'error': f'Sorry, you only have {wallet.get_available_balance() - fee} withdrawable TNBC (network fees included) available.'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            block_response, fee = send_tnbc(address, amount, wallet.memo)

            if block_response:
                if block_response.status_code == 201:
                    txs = ThenewbostonTransaction.objects.create(confirmation_status=ThenewbostonTransaction.WAITING_CONFIRMATION,
                                                                 transaction_status=ThenewbostonTransaction.IDENTIFIED,
                                                                 direction=ThenewbostonTransaction.OUTGOING,
                                                                 account_number=address,
                                                                 amount=amount,
                                                                 fee=fee,
                                                                 signature=block_response.json()['signature'],
                                                                 block=block_response.json()['id'],
                                                                 memo=wallet.memo)
                    wallet.balance -= amount + fee
                    wallet.save()
                    UserTransaction.objects.create(user=request.user, amount=amount + fee, type=UserTransaction.WITHDRAW, transaction=txs)
                    message = {'success': f'{amount} TNBC withdrawn to {address}'}
                    return Response(message, status=status.HTTP_200_OK)
                else:
                    error = {'error': 'Something went wrong, Try again later!'}
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            else:
                error = {'error': 'Something went wrong, Try again later!'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            return Response(message, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
