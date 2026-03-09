from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import BillOfMaterials, WorkCenter, ManufacturingOrder
from .serializers import (
    BillOfMaterialsSerializer, WorkCenterSerializer, ManufacturingOrderSerializer
)


@extend_schema(tags=['Manufacturing - BOMs'])
class BillOfMaterialsViewSet(viewsets.ModelViewSet):
    serializer_class = BillOfMaterialsSerializer

    def get_queryset(self):
        return BillOfMaterials.objects.filter(
            company=self.request.company, is_active=True
        ).select_related('product').prefetch_related('lines__component')

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company
        )


@extend_schema(tags=['Manufacturing - Work Centers'])
class WorkCenterViewSet(viewsets.ModelViewSet):
    serializer_class = WorkCenterSerializer

    def get_queryset(self):
        return WorkCenter.objects.filter(
            company=self.request.company, is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company
        )


@extend_schema(tags=['Manufacturing - Orders'])
class ManufacturingOrderViewSet(viewsets.ModelViewSet):
    serializer_class = ManufacturingOrderSerializer

    def get_queryset(self):
        return ManufacturingOrder.objects.filter(
            company=self.request.company
        ).select_related('product', 'bom').prefetch_related('work_orders')

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.tenant,
            company=self.request.company
        )

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        mo = self.get_object()
        try:
            mo.confirm()
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'confirmed'})
