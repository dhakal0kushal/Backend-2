from rest_framework.routers import SimpleRouter

from .views import ChainScanViewSet


router = SimpleRouter(trailing_slash=False)
router.register('scan-tnbc-chain', ChainScanViewSet, basename='scan-tnbc-chain')
