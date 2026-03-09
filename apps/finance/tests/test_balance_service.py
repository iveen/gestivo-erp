import pytest
from decimal import Decimal
from datetime import date
from apps.finance.models import (
    Account, AccountType, Journal, JournalEntry, JournalEntryLine
)
from apps.finance.services.balance_service import get_account_balance, get_trial_balance
from apps.tenants.models import Tenant
from apps.accounts.models import Company


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='Test Tenant', slug='test-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='Test Company', tenant=tenant)


@pytest.fixture
def journal(company, tenant):
    return Journal.objects.create(
        company=company,
        tenant=tenant,
        name='General Journal',
        code='GJ',
        journal_type='general'
    )


@pytest.fixture
def cash_account(company, tenant):
    return Account.objects.create(
        company=company,
        tenant=tenant,
        code='1001',
        name='Cash',
        account_type=AccountType.ASSET,
        currency='USD'
    )


@pytest.fixture
def revenue_account(company, tenant):
    return Account.objects.create(
        company=company,
        tenant=tenant,
        code='4001',
        name='Revenue',
        account_type=AccountType.REVENUE,
        currency='USD'
    )


@pytest.mark.django_db
def test_account_balance_with_no_entries(cash_account):
    balance = get_account_balance(cash_account)
    assert balance == Decimal('0')


@pytest.mark.django_db
def test_asset_account_balance(cash_account, journal, tenant):
    entry = JournalEntry.objects.create(
        tenant=tenant,
        journal=journal,
        date=date(2026, 1, 1),
        is_posted=True
    )
    JournalEntryLine.objects.create(
        tenant=tenant,
        entry=entry,
        account=cash_account,
        debit=Decimal('1000.00'),
        credit=Decimal('0.00')
    )
    balance = get_account_balance(cash_account)
    assert balance == Decimal('1000.00')


@pytest.mark.django_db
def test_unposted_entries_excluded(cash_account, journal, tenant):
    entry = JournalEntry.objects.create(
        tenant=tenant,
        journal=journal,
        date=date(2026, 1, 1),
        is_posted=False
    )
    JournalEntryLine.objects.create(
        tenant=tenant,
        entry=entry,
        account=cash_account,
        debit=Decimal('500.00'),
        credit=Decimal('0.00')
    )
    balance = get_account_balance(cash_account)
    assert balance == Decimal('0')


@pytest.mark.django_db
def test_trial_balance_debits_equal_credits(company, cash_account, revenue_account, journal, tenant):
    entry = JournalEntry.objects.create(
        tenant=tenant,
        journal=journal,
        date=date(2026, 1, 1),
        is_posted=True
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry, account=cash_account,
        debit=Decimal('1000.00'), credit=Decimal('0.00')
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry, account=revenue_account,
        debit=Decimal('0.00'), credit=Decimal('1000.00')
    )
    rows = get_trial_balance(company)
    total_debit  = sum(r['debit']  for r in rows)
    total_credit = sum(r['credit'] for r in rows)
    assert abs(total_debit - total_credit) <= Decimal('0.0001')
