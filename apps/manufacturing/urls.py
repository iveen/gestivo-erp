from rest_framework.routers import DefaultRouter
from .views import BillOfMaterialsViewSet, WorkCenterViewSet, ManufacturingOrderViewSet

router = DefaultRouter()
router.register('boms', BillOfMaterialsViewSet, basename='bom')
router.register('work-centers', WorkCenterViewSet, basename='work-center')
router.register('orders', ManufacturingOrderViewSet, basename='manufacturing-order')

urlpatterns = router.urls
