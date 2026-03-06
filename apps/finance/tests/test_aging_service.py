import pytest
from decimal import Decimal
from datetime import date
from apps.finance.models import Vendor, VendorBill, Account, AccountType
from apps.finance.services.aging_service import generate_ap_aging
from apps.tenants.models import Tenant
from apps.accounts.models import Company


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='AP Tenant', slug='ap-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='AP Company', tenant=tenant)


@pytest.fixture
def vendor(company, tenant):
    return Vendor.objects.create(
        company=company,
        tenant=tenant,
        name='Test Vendor',
        currency='USD'
    )


@pytest.mark.django_db
def test_empty_aging_report(company):
    report = generate_ap_aging(company, date(2026, 3, 1))
    assert report['grand_total'] == Decimal('0')


@pytest.mark.django_db
def test_current_bill_goes_to_current_bucket(company, vendor, tenant):
    VendorBill.objects.create(
        company=company, tenant=tenant, vendor=vendor,
        bill_number='BILL-001',
        bill_date=date(2026, 2, 1),
        due_date=date(2026, 3, 15),  # not yet due
        subtotal=Decimal('1000.00'),
        total=Decimal('1000.00'),
        amount_paid=Decimal('0.00'),
        status='posted'
    )
    report = generate_ap_aging(company, date(2026, 3, 1))
    assert report['buckets']['current']['total'] == Decimal('1000.00')
    assert report['grand_total'] == Decimal('1000.00')


@pytest.mark.django_db
def test_overdue_bill_goes_to_correct_bucket(company, vendor, tenant):
    VendorBill.objects.create(
        company=company, tenant=tenant, vendor=vendor,
        bill_number='BILL-002',
        bill_date=date(2026, 1, 1),
        due_date=date(2026, 2, 1),  # 28 days overdue as of March 1
        subtotal=Decimal('500.00'),
        total=Decimal('500.00'),
        amount_paid=Decimal('0.00'),
        status='posted'
    )
    report = generate_ap_aging(company, date(2026, 3, 1))
    assert report['buckets']['1_30']['total'] == Decimal('500.00')


@pytest.mark.django_db
def test_paid_bill_excluded(company, vendor, tenant):
    VendorBill.objects.create(
        company=company, tenant=tenant, vendor=vendor,
        bill_number='BILL-003',
        bill_date=date(2026, 1, 1),
        due_date=date(2026, 2, 1),
        subtotal=Decimal('500.00'),
        total=Decimal('500.00'),
        amount_paid=Decimal('500.00'),  # fully paid
        status='posted'
    )
    report = generate_ap_aging(company, date(2026, 3, 1))
    assert report['grand_total'] == Decimal('0')