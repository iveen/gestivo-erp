"""
URL configuration for gestivo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.accounts.views import CustomTokenObtainPairView

def health_check(request):
    from django.db import connection
    from django.core.cache import cache
    try:
        connection.ensure_connection()
        db_ok = True
    except Exception:
        db_ok = False
    try:
        cache.set('health', 'ok', 10)
        cache_ok = cache.get('health') == 'ok'
    except Exception:
        cache_ok = False

    status = 200 if db_ok else 503
    return JsonResponse({
        'status':    'ok' if db_ok else 'degraded',
        'database':  'ok' if db_ok else 'error',
        'cache':     'ok' if cache_ok else 'unavailable',
    }, status=status)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/finance/', include('apps.finance.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/sales/', include('apps.sales.urls')),
    path('api/purchases/', include('apps.purchases.urls')),
    path('api/manufacturing/', include('apps.manufacturing.urls')),
    path('api/crm/', include('apps.crm.urls')),
]