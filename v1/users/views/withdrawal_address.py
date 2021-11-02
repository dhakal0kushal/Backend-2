from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models.withdrawal_address import WithdrawalAddress
from ..serializers.withdrawal_address import WithdrawalAddressSerializer


# Create your views here.
class WithdrawalAddressViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawalAddressSerializer

    def get_queryset(self):
        return WithdrawalAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
