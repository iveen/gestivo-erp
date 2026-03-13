from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, ContactPointViewSet

router = DefaultRouter()
router.register('contacts',       ContactViewSet,      basename='contact')
router.register('contact-points', ContactPointViewSet, basename='contact-point')

urlpatterns = router.urls
