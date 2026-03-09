from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer


@extend_schema(tags=['Purchases - Orders'])
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        return PurchaseOrder.objects.filter(
            company=self.request.company
        ).select_related('vendor', 'approved_by').prefetch_related('lines')

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company
        )

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        po = self.get_object()
        try:
            po.submit_for_approval()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'pending'})

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        po = self.get_object()
        try:
            po.approve(request.user)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'approved'})
