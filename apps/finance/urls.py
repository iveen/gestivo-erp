from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    AccountViewSet, JournalViewSet, JournalEntryViewSet,
    BalanceSheetView, ProfitLossView
)

router = DefaultRouter()
router.register('accounts', AccountViewSet, basename='account')
router.register('journals', JournalViewSet, basename='journal')
router.register('journal-entries', JournalEntryViewSet, basename='journal-entry')

urlpatterns = router.urls + [
    path('reports/balance_sheet/', BalanceSheetView.as_view(), name='balance_sheet'),
    path('reports/profit_loss/', ProfitLossView.as_view(), name='profit_loss'),
]