from rest_framework.routers import DefaultRouter
from .views import PurchaseOrderViewSet

router = DefaultRouter()
router.register('orders', PurchaseOrderViewSet, basename='purchase-order')

urlpatterns = router.urls
