import pytest
from rest_framework.test import APIClient
from apps.tenants.models import Tenant
from apps.accounts.models import Company, User


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='Conftest Tenant', slug='conftest-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='Conftest Company', tenant=tenant)


@pytest.fixture
def user():
    return User.objects.create_user(
        email='conftest@test.com',
        password='pass123',
        first_name='Conftest',
        last_name='User'
    )


@pytest.fixture
def tenant_client(user, tenant, company, settings):
    settings.MIDDLEWARE = [
        m for m in settings.MIDDLEWARE
        if m not in (
            'apps.tenants.middleware.TenantMiddleware',
            'apps.accounts.middleware.CompanyMiddleware',
        )
    ]

    class FakeRequest:
        pass

    from unittest.mock import patch, PropertyMock
    client = APIClient()
    client.force_authenticate(user=user)
    client._tenant  = tenant
    client._company = company
    return client, tenant, company