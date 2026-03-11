from rest_framework.routers import DefaultRouter
from apps.accounts.views import (
    TenantViewSet, CompanyViewSet, RoleViewSet,
    UserViewSet, UserCompanyRoleViewSet
)

router = DefaultRouter()
router.register('tenants',  TenantViewSet,      basename='tenant')
router.register('companies', CompanyViewSet,    basename='company')
router.register('roles',     RoleViewSet,       basename='role')
router.register('users',     UserViewSet,       basename='user')
router.register('assignments', UserCompanyRoleViewSet, basename='assignment')

urlpatterns = router.urls