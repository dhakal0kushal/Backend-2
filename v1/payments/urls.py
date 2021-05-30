from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from .views import ChainScan, WithdrawTNBC

urlpatterns = [
    path('chain-scan/', ChainScan.as_view()),
    path('withdraw/', WithdrawTNBC.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
