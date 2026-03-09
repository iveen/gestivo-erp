from rest_framework.routers import DefaultRouter
from .views import SalesQuotationViewSet, SalesOrderViewSet

router = DefaultRouter()
router.register('quotations', SalesQuotationViewSet, basename='quotation')
router.register('orders', SalesOrderViewSet, basename='order')

urlpatterns = router.urls
