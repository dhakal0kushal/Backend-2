from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, mixins

from v1.core.utils.send_tnbc import send_tnbc, estimate_fee
from v1.core.models.transactions import Transaction

from ..serializers.withdraw import WithdrawTNBCSerializer
from ..models.wallets import Wallet
from ..models.transactions import UserTransaction


class WithdrawTNBCViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawTNBCSerializer

    def create(self, request, format=None):
        serializer = WithdrawTNBCSerializer(data=request.data)

        if serializer.is_valid():

            recipient_account_number = serializer.data['account_number']
            amount = int(serializer.data['amount'])

            fee = estimate_fee()

            if not Wallet.objects.filter(owner=request.user, account_number=recipient_account_number).exists():
                error = {'error': 'Account number not associated with the user'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            elif amount < 3:
                error = {'error': 'Sorry, you cannot withdraw less than 2 tnbc'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            elif amount + fee > request.user.get_available_balance():
                error = {'error': f'Sorry, you only have {request.user.get_available_balance()} balance eligible to withdraw.'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            block_response, fee = send_tnbc(recipient_account_number, amount, request.user.memo)

            if block_response:
                if block_response.status_code == 201:
                    txs = Transaction.objects.create(confirmation_status=Transaction.WAITING_CONFIRMATION,
                                                     transaction_status=Transaction.IDENTIFIED,
                                                     direction=Transaction.OUTGOING,
                                                     account_number=request.user.withdrawal_address,
                                                     amount=amount,
                                                     fee=fee,
                                                     signature=block_response.json()['signature'],
                                                     block=block_response.json()['id'],
                                                     memo=request.user.memo)
                    request.user.balance -= amount + fee
                    request.user.save()
                    UserTransaction.objects.create(user=request.user, amount=amount + fee, type=UserTransaction.WITHDRAW, transaction=txs)
                    message = {'success': f'{amount} TNBC withdrawn to {recipient_account_number}'}
                    return Response(message, status=status.HTTP_200_OK)
                else:
                    error = {'error': 'Something went wrong, Try again later!'}
                    return Response(error, status=status.HTTP_400_BAD_REQUEST)
            else:
                error = {'error': 'Something went wrong, Try again later!'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            return Response(message, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
