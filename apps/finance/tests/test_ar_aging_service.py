import pytest
from decimal import Decimal
from datetime import date
from apps.finance.models import Customer, CustomerInvoice
from apps.finance.services.ar_aging_service import generate_ar_aging
from apps.tenants.models import Tenant
from apps.accounts.models import Company


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='AR Aging Tenant', slug='ar-aging-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='AR Aging Company', tenant=tenant)


@pytest.fixture
def customer(company, tenant):
    return Customer.objects.create(
        company=company,
        tenant=tenant,
        name='Test Customer',
        currency='USD'
    )


@pytest.mark.django_db
def test_empty_ar_aging(company):
    report = generate_ar_aging(company, date(2026, 3, 1))
    assert report['grand_total'] == Decimal('0')


@pytest.mark.django_db
def test_current_invoice_goes_to_current_bucket(company, customer, tenant):
    CustomerInvoice.objects.create(
        company=company, tenant=tenant, customer=customer,
        invoice_number='INV-001',
        invoice_date=date(2026, 2, 1),
        due_date=date(2026, 3, 15),  # not yet due
        subtotal=Decimal('2000.00'),
        total=Decimal('2000.00'),
        amount_paid=Decimal('0.00'),
        status='sent'
    )
    report = generate_ar_aging(company, date(2026, 3, 1))
    assert report['buckets']['current']['total'] == Decimal('2000.00')
    assert report['grand_total'] == Decimal('2000.00')


@pytest.mark.django_db
def test_overdue_invoice_goes_to_correct_bucket(company, customer, tenant):
    CustomerInvoice.objects.create(
        company=company, tenant=tenant, customer=customer,
        invoice_number='INV-002',
        invoice_date=date(2026, 1, 1),
        due_date=date(2026, 2, 1),  # 28 days overdue as of March 1
        subtotal=Decimal('750.00'),
        total=Decimal('750.00'),
        amount_paid=Decimal('0.00'),
        status='overdue'
    )
    report = generate_ar_aging(company, date(2026, 3, 1))
    assert report['buckets']['1_30']['total'] == Decimal('750.00')


@pytest.mark.django_db
def test_paid_invoice_excluded(company, customer, tenant):
    CustomerInvoice.objects.create(
        company=company, tenant=tenant, customer=customer,
        invoice_number='INV-003',
        invoice_date=date(2026, 1, 1),
        due_date=date(2026, 2, 1),
        subtotal=Decimal('500.00'),
        total=Decimal('500.00'),
        amount_paid=Decimal('500.00'),
        status='paid'
    )
    report = generate_ar_aging(company, date(2026, 3, 1))
    assert report['grand_total'] == Decimal('0')