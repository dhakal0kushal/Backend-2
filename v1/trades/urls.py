from rest_framework.routers import SimpleRouter

from .views.advertisement import AdvertisementViewSet
from .views.order import OrderViewSet


router = SimpleRouter(trailing_slash=False)
router.register('advertisement', AdvertisementViewSet)
router.register('order', OrderViewSet, basename='order')
