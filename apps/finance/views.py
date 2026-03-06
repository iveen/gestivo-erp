from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Account, Journal, JournalEntry
from .serializers import (
    AccountSerializer, JournalSerializer, JournalEntrySerializer
)
from apps.finance.exceptions import UnbalancedJournalEntryError


@extend_schema(tags=['Finance - Accounts'])
class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(
            company=self.request.company,
            is_active=True
        ).select_related('parent').order_by('code')

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company
        )


@extend_schema(tags=['Finance - Journals'])
class JournalViewSet(viewsets.ModelViewSet):
    serializer_class = JournalSerializer

    def get_queryset(self):
        return Journal.objects.filter(
            company=self.request.company,
            is_active=True
        ).order_by('code')

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company
        )


@extend_schema(tags=['Finance - Journal Entries'])
class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer

    def get_queryset(self):
        return JournalEntry.objects.filter(
            journal__company=self.request.company
        ).prefetch_related('lines__account')

    @action(detail=True, methods=['post'])
    def post_entry(self, request, pk=None):
        entry = self.get_object()
        try:
            entry.post()
        except UnbalancedJournalEntryError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'status': 'posted'}, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from datetime import date
from apps.finance.services.reports.balance_sheet import generate_balance_sheet
from apps.finance.services.reports.profit_loss import generate_profit_loss


@extend_schema(tags=['Finance - Reports'])
class BalanceSheetView(APIView):
    def get(self, request):
        as_of = request.query_params.get('as_of', str(date.today()))
        report = generate_balance_sheet(
            request.company,
            date.fromisoformat(as_of)
        )
        return Response(report)


@extend_schema(tags=['Finance - Reports'])
class ProfitLossView(APIView):
    def get(self, request):
        start = request.query_params.get('start')
        end   = request.query_params.get('end', str(date.today()))

        if not start:
            return Response(
                {'error': 'start date is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        report = generate_profit_loss(
            request.company,
            date.fromisoformat(start),
            date.fromisoformat(end)
        )
        return Response(report)