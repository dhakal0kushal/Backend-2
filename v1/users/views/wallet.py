from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from ..models.wallets import Wallet
from ..serializers.wallet import WalletSerializer


# Create your views here.
class WalletViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)
