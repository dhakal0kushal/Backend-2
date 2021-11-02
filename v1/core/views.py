from rest_framework import status, mixins, viewsets
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from v1.constants.models import TnbcrowConstant

from .utils.scan_chain import check_confirmation, scan_chain, match_transaction


class ChainScanViewSet(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def create(self, request, format=None):

        tnbcrow_constant = TnbcrowConstant.objects.get(title="main")

        scan_chain()

        if tnbcrow_constant.check_tnbc_confirmation:

            check_confirmation()

        match_transaction()

        return Response({'success': 'Scan Completed!'}, status=status.HTTP_200_OK)
