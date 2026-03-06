from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import SalesQuotation, SalesOrder
from .serializers import SalesQuotationSerializer, SalesOrderSerializer


@extend_schema(tags=['Sales - Quotations'])
class SalesQuotationViewSet(viewsets.ModelViewSet):
    serializer_class = SalesQuotationSerializer

    def get_queryset(self):
        return SalesQuotation.objects.filter(
            company=self.request.company
        ).select_related('customer', 'salesperson').prefetch_related('lines')

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company
        )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        quotation = self.get_object()
        try:
            order = quotation.confirm()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(SalesOrderSerializer(order).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Sales - Orders'])
class SalesOrderViewSet(viewsets.ModelViewSet):
    serializer_class = SalesOrderSerializer

    def get_queryset(self):
        return SalesOrder.objects.filter(
            company=self.request.company
        ).select_related('customer', 'quotation')

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company
        )