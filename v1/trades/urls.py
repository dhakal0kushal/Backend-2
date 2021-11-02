from rest_framework.routers import SimpleRouter

from .views.trade_post import AdvertisementViewSet
from .views.active_trade import ActiveTradeViewSet


router = SimpleRouter(trailing_slash=False)
router.register('advertisement', AdvertisementViewSet)
router.register('active-trade', ActiveTradeViewSet, basename='activetrade')
