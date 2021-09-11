from . import views
from rest_framework.routers import SimpleRouter

from .views.wallets import WalletViewSet
from .views.withdraw import WithdrawTNBCViewSet

router = SimpleRouter(trailing_slash=False)
router.register('withdraw-tnbc', WithdrawTNBCViewSet, basename='withdraw-tnbc')
router.register('wallets', WalletViewSet, basename='wallet')
