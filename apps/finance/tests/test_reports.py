import pytest
from decimal import Decimal
from datetime import date
from apps.finance.models import (
    Account, AccountType, Journal, JournalEntry, JournalEntryLine
)
from apps.finance.services.reports.balance_sheet import generate_balance_sheet
from apps.finance.services.reports.profit_loss import generate_profit_loss
from apps.tenants.models import Tenant
from apps.accounts.models import Company


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='Report Tenant', slug='report-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='Report Company', tenant=tenant)


@pytest.fixture
def journal(company, tenant):
    return Journal.objects.create(
        company=company, tenant=tenant,
        name='General Journal', code='GJ2', journal_type='general'
    )


@pytest.fixture
def accounts(company, tenant):
    cash = Account.objects.create(
        company=company, tenant=tenant,
        code='1001', name='Cash',
        account_type=AccountType.ASSET, currency='USD'
    )
    equity = Account.objects.create(
        company=company, tenant=tenant,
        code='3001', name='Equity',
        account_type=AccountType.EQUITY, currency='USD'
    )
    revenue = Account.objects.create(
        company=company, tenant=tenant,
        code='4001', name='Revenue',
        account_type=AccountType.REVENUE, currency='USD'
    )
    expense = Account.objects.create(
        company=company, tenant=tenant,
        code='5001', name='Expenses',
        account_type=AccountType.EXPENSE, currency='USD'
    )
    return {'cash': cash, 'equity': equity, 'revenue': revenue, 'expense': expense}


@pytest.mark.django_db
def test_balance_sheet_is_balanced(company, journal, accounts, tenant):
    entry = JournalEntry.objects.create(
        tenant=tenant, journal=journal,
        date=date(2026, 1, 1), is_posted=True
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry,
        account=accounts['cash'],
        debit=Decimal('5000.00'), credit=Decimal('0.00')
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry,
        account=accounts['equity'],
        debit=Decimal('0.00'), credit=Decimal('5000.00')
    )
    report = generate_balance_sheet(company, date(2026, 1, 1))
    assert report['is_balanced'] is True
    assert report['assets']['total'] == Decimal('5000.00')
    assert report['equity']['total'] == Decimal('5000.00')


@pytest.mark.django_db
def test_profit_loss_net_income(company, journal, accounts, tenant):
    entry = JournalEntry.objects.create(
        tenant=tenant, journal=journal,
        date=date(2026, 1, 15), is_posted=True
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry,
        account=accounts['cash'],
        debit=Decimal('1000.00'), credit=Decimal('0.00')
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry,
        account=accounts['revenue'],
        debit=Decimal('0.00'), credit=Decimal('1000.00')
    )
    report = generate_profit_loss(company, date(2026, 1, 1), date(2026, 1, 31))
    assert report['revenue']['total'] == Decimal('1000.00')
    assert report['net_income'] == Decimal('1000.00')


@pytest.mark.django_db
def test_profit_loss_with_expenses(company, journal, accounts, tenant):
    entry = JournalEntry.objects.create(
        tenant=tenant, journal=journal,
        date=date(2026, 1, 15), is_posted=True
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry,
        account=accounts['revenue'],
        debit=Decimal('0.00'), credit=Decimal('2000.00')
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry,
        account=accounts['expense'],
        debit=Decimal('800.00'), credit=Decimal('0.00')
    )
    JournalEntryLine.objects.create(
        tenant=tenant, entry=entry,
        account=accounts['cash'],
        debit=Decimal('1200.00'), credit=Decimal('0.00')
    )
    report = generate_profit_loss(company, date(2026, 1, 1), date(2026, 1, 31))
    assert report['revenue']['total'] == Decimal('2000.00')
    assert report['expenses']['total'] == Decimal('800.00')
    assert report['net_income'] == Decimal('1200.00')