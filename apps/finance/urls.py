from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, JournalViewSet, JournalEntryViewSet

router = DefaultRouter()
router.register('accounts', AccountViewSet, basename='account')
router.register('journals', JournalViewSet, basename='journal')
router.register('journal-entries', JournalEntryViewSet, basename='journal-entry')

urlpatterns = router.urls