import requests
from datetime import datetime, timedelta

from django.utils import timezone
from django.conf import settings

from ..models.scan_tracker import ScanTracker
from ..models.transactions import ThenewbostonTransaction
from ..models.asset import Asset

from v1.users.models.wallets import Wallet
from v1.users.models.transactions import UserTransaction
from v1.constants.models import TnbcrowConstant


def check_confirmation():

    waiting_confirmations_txs = ThenewbostonTransaction.objects.filter(confirmation_status=ThenewbostonTransaction.WAITING_CONFIRMATION,
                                                                       created_at__gt=timezone.now() - timedelta(hours=1))

    bank_ip = TnbcrowConstant.objects.get(title="main").bank_ip
    
    for txs in waiting_confirmations_txs:

        try:
            r = requests.get(f"http://{bank_ip}/confirmation_blocks?block={txs.block}").json()

        except requests.exceptions.RequestException:

            return False

        if 'count' in r:
            if int(r['count']) > 0:
                txs.total_confirmations = int(r['count'])
                txs.confirmation_status = ThenewbostonTransaction.CONFIRMED
                txs.save()


def scan_chain():

    scan_tracker, created = ScanTracker.objects.get_or_create(asset__symbol="TNBC")

    deposit_address = Asset.objects.get(symbol="TNBC").deposit_address

    bank_ip = TnbcrowConstant.objects.get(title="main").bank_ip

    next_url = f"http://{bank_ip}/bank_transactions?account_number={deposit_address}&block__sender=&fee=&recipient="

    transaction_fee = 0

    while next_url:

        try:
            r = requests.get(next_url).json()

        except requests.exceptions.RequestException:

            return False

        next_url = r['next']

        for transaction in r['results']:

            transaction_time = timezone.make_aware(datetime.strptime(transaction['block']['created_date'], '%Y-%m-%dT%H:%M:%S.%fZ'))
            transaction_exists = ThenewbostonTransaction.objects.filter(signature=transaction['block']['signature']).exists()

            if scan_tracker.last_scanned < transaction_time and not transaction_exists:

                amount = int(transaction['amount'])

                if transaction['recipient'] == deposit_address:
                    direction = ThenewbostonTransaction.INCOMING
                    account_number = transaction['block']['sender']
                else:
                    transaction_fee = settings.TNBC_TRANSACTION_FEE
                    direction = ThenewbostonTransaction.OUTGOING
                    account_number = transaction['recipient']

                if transaction['fee'] == "":
                    ThenewbostonTransaction.objects.create(confirmation_status=ThenewbostonTransaction.WAITING_CONFIRMATION,
                                                           direction=direction,
                                                           transaction_status=ThenewbostonTransaction.NEW,
                                                           account_number=account_number,
                                                           amount=amount,
                                                           fee=transaction_fee,
                                                           block=transaction['block']['id'],
                                                           signature=transaction['block']['signature'],
                                                           memo=transaction['memo'])

            else:
                next_url = None
                break

    scan_tracker.total_scans += 1
    scan_tracker.save()


def match_transaction():

    tnbcrow_constant = TnbcrowConstant.objects.get(title="main")

    if tnbcrow_constant.check_tnbc_confirmation:
        confirmed_txs = ThenewbostonTransaction.objects.filter(confirmation_status=ThenewbostonTransaction.CONFIRMED,
                                                               transaction_status=ThenewbostonTransaction.NEW,
                                                               direction=ThenewbostonTransaction.INCOMING)
    else:
        confirmed_txs = ThenewbostonTransaction.objects.filter(confirmation_status=ThenewbostonTransaction.WAITING_CONFIRMATION,
                                                               transaction_status=ThenewbostonTransaction.NEW,
                                                               direction=ThenewbostonTransaction.INCOMING)

    for txs in confirmed_txs:

        if Wallet.objects.filter(asset__symbol="TNBC", memo=txs.memo).exists():

            wallet = Wallet.objects.get(asset__symbol="TNBC", memo=txs.memo)
            wallet.balance += txs.amount
            wallet.save()

            UserTransaction.objects.create(user=wallet.user, amount=txs.amount, type=UserTransaction.DEPOSIT, transaction=txs)

            txs.transaction_status = ThenewbostonTransaction.IDENTIFIED
            txs.save()
        else:
            txs.transaction_status = ThenewbostonTransaction.UNIDENTIFIED
            txs.save()
