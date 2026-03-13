import pytest
from decimal import Decimal
from datetime import date
from django.utils import timezone
from apps.contacts.models import Contact
from apps.finance.models import (
    Account, AccountType, FiscalYear, FiscalPeriod,
    Journal, JournalEntry, JournalEntryLine,
    VendorBill, CustomerInvoice
)
from apps.finance.exceptions import UnbalancedJournalEntryError
from apps.tenants.models import Tenant
from apps.accounts.models import Company


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='Model Tenant', slug='model-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='Model Company', tenant=tenant)


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
        name='General Journal', code='GJ3',
        journal_type='general'
    )


@pytest.mark.django_db
def test_liability_account_normal_balance(company, tenant):
    acct = Account.objects.create(
        company=company, tenant=tenant,
        code='2001', name='Accounts Payable',
        account_type=AccountType.LIABILITY,
        currency='USD'
    )
    assert acct.normal_balance == 'credit'


@pytest.mark.django_db
def test_equity_account_normal_balance(company, tenant):
    acct = Account.objects.create(
        company=company, tenant=tenant,
        code='3001', name='Equity',
        account_type=AccountType.EQUITY,
        currency='USD'
    )
    assert acct.normal_balance == 'credit'


@pytest.mark.django_db
def test_revenue_account_normal_balance(company, tenant):
    acct = Account.objects.create(
        company=company, tenant=tenant,
        code='4001', name='Revenue',
        account_type=AccountType.REVENUE,
        currency='USD'
    )
    assert acct.normal_balance == 'credit'


@pytest.mark.django_db
def test_expense_account_normal_balance(company, tenant):
    acct = Account.objects.create(
        company=company, tenant=tenant,
        code='5001', name='Expenses',
        account_type=AccountType.EXPENSE,
        currency='USD'
    )
    assert acct.normal_balance == 'debit'


@pytest.mark.django_db
def test_fiscal_period_close(company, tenant):
    fy = FiscalYear.objects.create(
        company=company, tenant=tenant,
        name='FY2026',
        start_date=date(2026, 1, 1),
        end_date=date(2026, 12, 31)
    )
    period = FiscalPeriod.objects.create(
        tenant=tenant, fiscal_year=fy,
        name='Jan 2026',
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 31)
    )
    period.close()
    period.refresh_from_db()
    assert period.is_closed is True


@pytest.mark.django_db
def test_journal_entry_post(company, tenant, account, journal):
    entry = JournalEntry.objects.create(
        tenant=tenant, journal=journal,
        date=date(2026, 1, 1), is_posted=False
    )
    acct2 = Account.objects.create(
        company=company, tenant=tenant,
        code='4001', name='Revenue',
        account_type=AccountType.REVENUE,
        currency='USD'
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry, account=account,
        debit=Decimal('1000.00'), credit=Decimal('0.00')
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry, account=acct2,
        debit=Decimal('0.00'), credit=Decimal('1000.00')
    )
    entry.post()
    entry.refresh_from_db()
    assert entry.is_posted is True


@pytest.mark.django_db
def test_journal_entry_post_fails_if_unbalanced(company, tenant, account, journal):
    entry = JournalEntry.objects.create(
        tenant=tenant, journal=journal,
        date=date(2026, 1, 1), is_posted=False
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry, account=account,
        debit=Decimal('1000.00'), credit=Decimal('0.00')
    )
    with pytest.raises(UnbalancedJournalEntryError):
        entry.post()


@pytest.mark.django_db
def test_vendor_bill_str(company, tenant):
    vendor = Contact.objects.create(
        company=company, tenant=tenant,
        name='Test Vendor', currency='USD', is_vendor=True
    )
    bill = VendorBill.objects.create(
        company=company, tenant=tenant,
        vendor=vendor,
        bill_number='BILL-STR-001',
        bill_date=date(2026, 1, 1),
        due_date=date(2026, 2, 1),
        subtotal=Decimal('500.00'),
        total=Decimal('500.00'),
        status='draft'
    )
    assert 'BILL-STR-001' in str(bill)


@pytest.mark.django_db
def test_customer_invoice_is_not_overdue_when_future(company, tenant):
    customer = Contact.objects.create(
        company=company, tenant=tenant,
        name='Test Customer', currency='USD', is_customer=True
    )
    invoice = CustomerInvoice.objects.create(
        company=company, tenant=tenant,
        customer=customer,
        invoice_number='INV-FUTURE',
        invoice_date=date(2026, 1, 1),
        due_date=date(2099, 12, 31),
        subtotal=Decimal('1000.00'),
        total=Decimal('1000.00'),
        status='sent'
    )
    assert invoice.is_overdue is False
