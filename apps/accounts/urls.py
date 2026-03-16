from rest_framework.routers import DefaultRouter
from apps.accounts.views import (
    TenantViewSet, CompanyViewSet, RoleViewSet,
    UserViewSet, UserCompanyRoleViewSet, CompanySettingsViewSet
)

router = DefaultRouter()
router.register('tenants',  TenantViewSet,      basename='tenant')
router.register('companies', CompanyViewSet,    basename='company')
router.register('roles',     RoleViewSet,       basename='role')
router.register('users',     UserViewSet,       basename='user')
router.register('assignments',      UserCompanyRoleViewSet,  basename='assignment')
router.register('company-settings', CompanySettingsViewSet,    basename='company-settings')

urlpatterns = router.urls