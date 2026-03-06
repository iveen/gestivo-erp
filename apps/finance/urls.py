from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    AccountViewSet, JournalViewSet, JournalEntryViewSet,
    BalanceSheetView, ProfitLossView,
    VendorViewSet, VendorBillViewSet, APAgingView,
    CustomerViewSet, CustomerInvoiceViewSet, ARAgingView
)

router = DefaultRouter()
router.register('accounts', AccountViewSet, basename='account')
router.register('journals', JournalViewSet, basename='journal')
router.register('journal-entries', JournalEntryViewSet, basename='journal-entry')
router.register('vendors', VendorViewSet, basename='vendor')
router.register('vendor-bills', VendorBillViewSet, basename='vendor-bill')
router.register('customers', CustomerViewSet, basename='customer')
router.register('customer-invoices', CustomerInvoiceViewSet, basename='customer-invoice')

urlpatterns = router.urls + [
    path('reports/balance_sheet/', BalanceSheetView.as_view(), name='balance_sheet'),
    path('reports/profit_loss/', ProfitLossView.as_view(), name='profit_loss'),
    path('reports/ap_aging/', APAgingView.as_view(), name='ap-aging'),
    path('reports/ar_aging/', ARAgingView.as_view(), name='ar-aging'),
]