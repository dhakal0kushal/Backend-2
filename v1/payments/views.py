import requests
import os
import nacl.signing
from django.utils import timezone
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from v1.users.models import User, Wallet

from .models import ChainScanTracker, TransactionHistory
from .serializers import WithdrawTNBCSerializer
from .utils import generate_block

PV_IP = "54.219.183.128"
BANK_IP = "54.177.121.3"
ESCROW_WALLET = "0000000000000000000000000000000000000000000000000000000000000000"
TRANSACTION_URL = f"http://{BANK_IP}/bank_transactions?account_number=&block__sender=&fee=&recipient={ESCROW_WALLET}"
signing_key = nacl.signing.SigningKey(str.encode(os.environ.get('TNBCROW_SIGNING_KEY')), encoder=nacl.encoding.HexEncoder)
payment_account_number = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode('utf-8')


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

            recipient_account_number = serializer.data['account_number']
            amount = int(serializer.data['amount'])

            if not Wallet.objects.filter(owner=request.user, account_number=recipient_account_number).exists():
                error = {'error': 'Account number not associated with the user'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            elif amount < 3:
                error = {'error': 'Sorry, you cannot withdraw less than 2 tnbc'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            elif amount > request.user.loaded - request.user.locked:
                error = {'error': 'Sorry, you donot have enough balance for withdrawl'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            bank_config = requests.get(f'http://{BANK_IP}/config?format=json').json()

            balance_lock = requests.get(f"{bank_config['primary_validator']['protocol']}://{bank_config['primary_validator']['ip_address']}:{bank_config['primary_validator']['port'] or 0}/accounts/{payment_account_number}/balance_lock?format=json").json()['balance_lock']
            
            transaction_fee = int(bank_config['default_transaction_fee']) + int(bank_config['primary_validator']['default_transaction_fee'])

            withdrawl_amount = amount - transaction_fee

            txs = [
                {
                    'amount': withdrawl_amount,
                    'memo': 'tnbCrow withdrawl',
                    'recipient': recipient_account_number,
                },
                {
                    'amount': int(bank_config['default_transaction_fee']),
                    'fee': 'BANK',
                    'recipient': bank_config['account_number'],
                },
                {
                    'amount': int(bank_config['primary_validator']['default_transaction_fee']),
                    'fee': 'PRIMARY_VALIDATOR',
                    'recipient': bank_config['primary_validator']['account_number'],
                }
            ]

            data = generate_block(balance_lock, txs, signing_key)

            headers = {
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) TNBAccountManager/1.0.0-alpha.43 Chrome/83.0.4103.122 Electron/9.4.0 Safari/537.36',
                'Content-Type': 'application/json',
            }

            r = requests.request("POST", f'http://{BANK_IP}/blocks', headers=headers, data=data)

            if r:
                message = {'success': f'{withdrawl_amount} TNBC withdrawn to {recipient_account_number}'}
                request.user.loaded -= amount
                request.user.save()
            else:
                error = {'error': 'Something went wrong, Try again later!'}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            return Response(message, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
