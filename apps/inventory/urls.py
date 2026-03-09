from rest_framework.routers import DefaultRouter
from .views import (
    ProductCategoryViewSet, UnitOfMeasureViewSet, ProductViewSet,
    WarehouseViewSet, StockLocationViewSet, StockMoveViewSet,
    StockQuantViewSet, LowStockView
)

router = DefaultRouter()
router.register('categories', ProductCategoryViewSet, basename='category')
router.register('uom', UnitOfMeasureViewSet, basename='uom')
router.register('products', ProductViewSet, basename='product')
router.register('warehouses', WarehouseViewSet, basename='warehouse')
router.register('locations', StockLocationViewSet, basename='location')
router.register('stock-moves', StockMoveViewSet, basename='stock-move')
router.register('stock-quants', StockQuantViewSet, basename='stock-quant')
router.register('low-stock', LowStockView, basename='low-stock')

urlpatterns = router.urls
