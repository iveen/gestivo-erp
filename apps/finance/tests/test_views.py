import pytest
from decimal import Decimal
from datetime import date
from rest_framework.test import APIClient
from apps.finance.models import Account, AccountType, Journal
from apps.tenants.models import Tenant
from apps.accounts.models import Company, User


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='View Tenant', slug='view-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='View Company', tenant=tenant)


@pytest.fixture
def user():
    return User.objects.create_user(
        email='view@test.com',
        password='pass123',
        first_name='View',
        last_name='User'
    )


@pytest.fixture
def api_client(user, tenant, company):
    client = APIClient()
    client.force_authenticate(user=user)
    client.tenant  = tenant
    client.company = company
    return client


@pytest.fixture
def authed_client(api_client, tenant, company, mocker):
    mocker.patch(
        'rest_framework.request.Request.tenant',
        new_callable=lambda: property(lambda self: tenant),
        create=True
    )
    mocker.patch(
        'rest_framework.request.Request.company',
        new_callable=lambda: property(lambda self: company),
        create=True
    )
    return api_client


@pytest.fixture
def account(company, tenant):
    return Account.objects.create(
        company=company, tenant=tenant,
        code='1001', name='Cash',
        account_type=AccountType.ASSET,
        currency='USD'
    )


@pytest.fixture
def journal(company, tenant):
    return Journal.objects.create(
        company=company, tenant=tenant,
        name='General Journal', code='GJ',
        journal_type='general'
    )


@pytest.mark.django_db
def test_account_list_requires_auth():
    client = APIClient()
    response = client.get('/api/finance/accounts/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_journal_entry_balance_validation(authed_client):
    pass  # placeholder - full API tests require middleware setup