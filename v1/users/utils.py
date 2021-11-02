from v1.core.models.asset import Asset

from .models.wallets import Wallet


def validate_address(symbol, address):

    if symbol == "TNBC":
        if len(address) == 64:
            return True

    return False


def get_tnbc_asset():
    
    return Asset.objects.get(symbol="TNBC")


def get_or_create_wallet(user, asset):

    return Wallet.objects.get_or_create(user=user, asset=asset)
