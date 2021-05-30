import requests
from django.utils import timezone
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from v1.users.models import User, Wallet

from .models import ChainScanTracker, TransactionHistory
from .serializers import WithdrawTNBCSerializer


PV_IP = "54.219.183.128"
BANK_IP = "54.177.121.3"
ESCROW_WALLET = "0000000000000000000000000000000000000000000000000000000000000000"
TRANSACTION_URL = f"http://{BANK_IP}/bank_transactions?account_number=&block__sender=&fee=&recipient={ESCROW_WALLET}"


class ChainScan(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        scan_tracker = ChainScanTracker.objects.first()
        next_url = TRANSACTION_URL

        while next_url:
            r = requests.get(TRANSACTION_URL).json()
            next_url = r['next']
            for transaction in r['results']:
                transaction_time = timezone.make_aware(datetime.strptime(transaction['block']['modified_date'], '%Y-%m-%dT%H:%M:%S.%fZ'))
                if scan_tracker.updated_at < transaction_time:
                    amount = int(transaction['amount'])
                    user_memo = User.objects.filter(memo=transaction['memo']).first()
                    if user_memo:
                        user_memo.loaded += amount
                        user_memo.save()
                        TransactionHistory.objects.create(user=request.user, amount=amount, type=TransactionHistory.DEPOSIT, status=TransactionHistory.COMPELTED)
                else:
                    next_url = None
                    break
        scan_tracker.updated_at = timezone.now()
        scan_tracker.save()
        return Response(status=status.HTTP_201_CREATED)


class WithdrawTNBC(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = WithdrawTNBCSerializer(data=request.data)

        if serializer.is_valid():
            if not Wallet.objects.filter(owner=request.user, account_number=serializer.data['account_number']).exists():
                error = {'error': 'Account number not associated with the user'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
