from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import (
    ProductCategory, UnitOfMeasure, Product,
    Warehouse, StockLocation, StockMove, StockQuant
)
from .serializers import (
    ProductCategorySerializer, UnitOfMeasureSerializer, ProductSerializer,
    WarehouseSerializer, StockLocationSerializer, StockMoveSerializer,
    StockQuantSerializer
)
from .services.stock_service import process_stock_move, get_stock_on_hand
from .services.alert_service import get_low_stock_products


@extend_schema(tags=['Inventory - Products'])
class ProductCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        return ProductCategory.objects.filter(
            company=self.request.company, is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant, company=self.request.company)


@extend_schema(tags=['Inventory - Products'])
class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    serializer_class = UnitOfMeasureSerializer

    def get_queryset(self):
        return UnitOfMeasure.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)


@extend_schema(tags=['Inventory - Products'])
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(
            company=self.request.company, is_active=True
        ).select_related('category', 'uom')

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant, company=self.request.company)


@extend_schema(tags=['Inventory - Warehouses'])
class WarehouseViewSet(viewsets.ModelViewSet):
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        return Warehouse.objects.filter(
            company=self.request.company, is_active=True
        )

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant, company=self.request.company)


@extend_schema(tags=['Inventory - Warehouses'])
class StockLocationViewSet(viewsets.ModelViewSet):
    serializer_class = StockLocationSerializer

    def get_queryset(self):
        return StockLocation.objects.filter(
            warehouse__company=self.request.company, is_active=True
        ).select_related('warehouse')


@extend_schema(tags=['Inventory - Stock'])
class StockMoveViewSet(viewsets.ModelViewSet):
    serializer_class = StockMoveSerializer

    def get_queryset(self):
        return StockMove.objects.filter(
            product__company=self.request.company
        ).select_related('product', 'source', 'destination')

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.tenant)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        move = self.get_object()
        try:
            process_stock_move(move)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'done'})


@extend_schema(tags=['Inventory - Stock'])
class StockQuantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StockQuantSerializer

    def get_queryset(self):
        return StockQuant.objects.filter(
            product__company=self.request.company
        ).select_related('product', 'location')


@extend_schema(tags=['Inventory - Reports'])
class LowStockView(viewsets.ViewSet):
    def list(self, request):
        alerts = get_low_stock_products(request.company)
        return Response(alerts)
