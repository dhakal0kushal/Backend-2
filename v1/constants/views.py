from rest_framework import viewsets

from .models import Country, TransactionType, Exchange, Currency, PaymentMethod
from .serializers import CountrySerializer, TransactionTypeSerializer, ExchangeSerializer, CurrencySerializer, PaymentMethodSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class TransactionTypeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer


class ExchangeViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
