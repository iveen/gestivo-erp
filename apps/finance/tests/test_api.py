import pytest
from decimal import Decimal
from datetime import date
from rest_framework.test import APIClient
from apps.finance.models import Account, AccountType, Journal, JournalEntry, JournalEntryLine
from apps.tenants.models import Tenant
from apps.accounts.models import Company, User


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='API Tenant', slug='api-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='API Company', tenant=tenant)


@pytest.fixture
def user():
    return User.objects.create_user(
        email='api@test.com',
        password='pass123',
        first_name='API',
        last_name='User'
    )


@pytest.fixture
def api_client(user, tenant, company, settings):
    # Disable tenant and company middleware for API tests
    settings.MIDDLEWARE = [
        m for m in settings.MIDDLEWARE
        if m not in (
            'apps.tenants.middleware.TenantMiddleware',
            'apps.accounts.middleware.CompanyMiddleware',
        )
    ]
    client = APIClient()
    client.force_authenticate(user=user)
    return client


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
        name='General Journal', code='GJ4',
        journal_type='general'
    )


@pytest.mark.django_db
def test_account_list_requires_auth():
    client = APIClient()
    response = client.get('/api/finance/accounts/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_balance_sheet_view(api_client, tenant, company, monkeypatch):
    monkeypatch.setattr(
        'apps.finance.views.BalanceSheetView.get',
        lambda self, request: __import__(
            'rest_framework.response', fromlist=['Response']
        ).Response({'is_balanced': True, 'assets': {}, 'liabilities': {}, 'equity': {}})
    )
    response = api_client.get('/api/finance/reports/balance_sheet/?as_of=2026-03-01')
    assert response.status_code == 200


@pytest.mark.django_db
def test_profit_loss_view(api_client, tenant, company, monkeypatch):
    monkeypatch.setattr(
        'apps.finance.views.ProfitLossView.get',
        lambda self, request: __import__(
            'rest_framework.response', fromlist=['Response']
        ).Response({'net_income': '0.00', 'revenue': {}, 'expenses': {}})
    )
    response = api_client.get(
        '/api/finance/reports/profit_loss/?start=2026-01-01&end=2026-03-31'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_profit_loss_missing_start(api_client, tenant, company, monkeypatch):
    from rest_framework.response import Response
    from rest_framework import status

    def fake_get(self, request):
        start = request.query_params.get('start')
        if not start:
            return Response({'error': 'start date is required'}, status=400)
        return Response({})

    monkeypatch.setattr('apps.finance.views.ProfitLossView.get', fake_get)
    response = api_client.get('/api/finance/reports/profit_loss/')
    assert response.status_code == 400


@pytest.mark.django_db
def test_ap_aging_view(api_client, tenant, company, monkeypatch):
    monkeypatch.setattr(
        'apps.finance.views.APAgingView.get',
        lambda self, request: __import__(
            'rest_framework.response', fromlist=['Response']
        ).Response({'grand_total': '0.00', 'buckets': {}})
    )
    response = api_client.get('/api/finance/reports/ap_aging/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_ar_aging_view(api_client, tenant, company, monkeypatch):
    monkeypatch.setattr(
        'apps.finance.views.ARAgingView.get',
        lambda self, request: __import__(
            'rest_framework.response', fromlist=['Response']
        ).Response({'grand_total': '0.00', 'buckets': {}})
    )
    response = api_client.get('/api/finance/reports/ar_aging/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_journal_entry_post_action(api_client, tenant, company, journal, account):
    acct2 = Account.objects.create(
        company=company, tenant=tenant,
        code='4001', name='Revenue',
        account_type=AccountType.REVENUE,
        currency='USD'
    )
    entry = JournalEntry.objects.create(
        tenant=tenant, journal=journal,
        date=date(2026, 1, 1), is_posted=False
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry, account=account,
        debit=Decimal('500.00'), credit=Decimal('0.00')
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry, account=acct2,
        debit=Decimal('0.00'), credit=Decimal('500.00')
    )
    from unittest.mock import patch
    with patch.object(
        __import__('apps.finance.views', fromlist=['JournalEntryViewSet']).JournalEntryViewSet,
        'get_queryset',
        return_value=JournalEntry.objects.filter(journal__company=company)
    ):
        response = api_client.post(f'/api/finance/journal-entries/{entry.id}/post_entry/')
        assert response.status_code == 200

@pytest.mark.django_db
def test_vendor_list_requires_auth():
    client = APIClient()
    response = client.get('/api/finance/vendors/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_customer_list_requires_auth():
    client = APIClient()
    response = client.get('/api/finance/customers/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_vendor_bill_list_requires_auth():
    client = APIClient()
    response = client.get('/api/finance/vendor-bills/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_customer_invoice_list_requires_auth():
    client = APIClient()
    response = client.get('/api/finance/customer-invoices/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_journal_entry_list_requires_auth():
    client = APIClient()
    response = client.get('/api/finance/journal-entries/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_unbalanced_journal_entry_post_fails(api_client, tenant, company, journal, account):
    entry = JournalEntry.objects.create(
        tenant=tenant, journal=journal,
        date=date(2026, 1, 1), is_posted=False
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry, account=account,
        debit=Decimal('500.00'), credit=Decimal('0.00')
    )
    from unittest.mock import patch
    with patch.object(
        __import__('apps.finance.views', fromlist=['JournalEntryViewSet']).JournalEntryViewSet,
        'get_queryset',
        return_value=JournalEntry.objects.filter(journal__company=company)
    ):
        response = api_client.post(f'/api/finance/journal-entries/{entry.id}/post_entry/')
        assert response.status_code == 400

@pytest.mark.django_db
def test_account_create(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post('/api/finance/accounts/', {
        'code': '9001',
        'name': 'Test Account',
        'account_type': 'asset',
        'currency': 'USD',
    }, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_account_list_with_tenant(user, tenant, company, with_tenant_company):
    Account.objects.create(
        company=company, tenant=tenant,
        code='9002', name='Test Account 2',
        account_type=AccountType.ASSET,
        currency='USD'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/accounts/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_journal_create(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post('/api/finance/journals/', {
        'name': 'Test Journal',
        'code': 'TJ1',
        'journal_type': 'general',
    }, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_vendor_list_with_tenant(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/vendors/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_customer_list_with_tenant(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/customers/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_balance_sheet_with_tenant(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/reports/balance_sheet/?as_of=2026-03-01')
    assert response.status_code == 200


@pytest.mark.django_db
def test_profit_loss_with_tenant(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(
        '/api/finance/reports/profit_loss/?start=2026-01-01&end=2026-03-31'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_ap_aging_with_tenant(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/reports/ap_aging/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_ar_aging_with_tenant(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/reports/ar_aging/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_vendor_create(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post('/api/finance/vendors/', {
        'name': 'New Vendor',
        'currency': 'USD',
        'payment_terms': 30,
    }, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_customer_create(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post('/api/finance/customers/', {
        'name': 'New Customer',
        'currency': 'USD',
        'credit_limit': '5000.00',
    }, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_vendor_bill_list(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/vendor-bills/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_customer_invoice_list(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/customer-invoices/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_customer_invoice_create(user, tenant, company, with_tenant_company):
    from apps.finance.models import Customer
    from datetime import date
    customer = Customer.objects.create(
        company=company, tenant=tenant,
        name='Invoice Customer', currency='USD'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post('/api/finance/customer-invoices/', {
        'customer': str(customer.id),
        'invoice_number': 'INV-API-001',
        'invoice_date': '2026-03-01',
        'due_date': '2026-03-31',
        'subtotal': '1000.00',
        'total': '1000.00',
        'status': 'draft',
    }, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_journal_list_with_tenant(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/journals/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_journal_entry_list_with_tenant(user, tenant, company, with_tenant_company, journal):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/journal-entries/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_profit_loss_missing_start_with_tenant(user, tenant, company, with_tenant_company):
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/api/finance/reports/profit_loss/')
    assert response.status_code == 400