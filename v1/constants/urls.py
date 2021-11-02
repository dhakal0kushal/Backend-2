from rest_framework.routers import SimpleRouter

from .views import CountryViewSet, TransactionTypeViewSet, ExchangeViewSet, CurrencyViewSet, PaymentMethodViewSet


router = SimpleRouter(trailing_slash=False)
router.register('countries', CountryViewSet)
router.register('transaction-type', TransactionTypeViewSet)
router.register('exchange', ExchangeViewSet)
router.register('currency', CurrencyViewSet)
router.register('payment-method', PaymentMethodViewSet)
