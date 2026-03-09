from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Lead
from .serializers import LeadSerializer


@extend_schema(tags=['CRM - Leads'])
class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer

    def get_queryset(self):
        return Lead.objects.filter(
            company=self.request.company, is_active=True
        ).select_related('salesperson', 'sales_order')

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company,
            salesperson=self.request.user
        )

    @action(detail=True, methods=['post'])
    def won(self, request, pk=None):
        lead = self.get_object()
        try:
            lead.mark_won()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'won'})

    @action(detail=True, methods=['post'])
    def lost(self, request, pk=None):
        lead = self.get_object()
        try:
            lead.mark_lost()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'lost'})
