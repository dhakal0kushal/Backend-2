from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .utils.scan_chain import check_confirmation, scan_chain, match_transaction


class ChainScan(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        chain_scan = scan_chain()

        if not chain_scan:
            error = {'error': 'could not scan chain'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        confirmation_check = check_confirmation()

        if not confirmation_check:
            error = {'error': 'could not check for confirmations'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        match_transaction()

        return Response({'success': 'Scan Completed'}, status=status.HTTP_200_OK)
