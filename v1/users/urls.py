from rest_framework.routers import SimpleRouter

from .views.withdrawal_address import WithdrawalAddressViewSet
from .views.withdraw import WithdrawTNBCViewSet
from .views.deposit import DepositViewSet

router = SimpleRouter(trailing_slash=False)
router.register('withdraw', WithdrawTNBCViewSet, basename='withdraw-tnbc')
router.register('withdrawal-address', WithdrawalAddressViewSet, basename='withdrawal-address')
router.register('deposit', DepositViewSet, basename='deposit')
