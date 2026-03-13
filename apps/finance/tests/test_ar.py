import pytest
from decimal import Decimal
from datetime import date
from apps.finance.models import CustomerInvoice, CustomerInvoiceLine, Account, AccountType
from apps.contacts.models import Contact
from apps.tenants.models import Tenant
from apps.accounts.models import Company


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='AR Tenant', slug='ar-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='AR Company', tenant=tenant)


@pytest.fixture
def customer(company, tenant):
    return Contact.objects.create(
        company=company,
        tenant=tenant,
        name='Test Customer',
        currency='USD',
        is_customer=True
    )


@pytest.fixture
def invoice(company, tenant, customer):
    return CustomerInvoice.objects.create(
        company=company,
        tenant=tenant,
        customer=customer,
        invoice_number='INV-001',
        invoice_date=date(2026, 1, 1),
        due_date=date(2026, 1, 31),
        subtotal=Decimal('1000.00'),
        total=Decimal('1000.00'),
        amount_paid=Decimal('0.00'),
        status='sent'
    )


@pytest.mark.django_db
def test_invoice_amount_due(invoice):
    assert invoice.amount_due == Decimal('1000.00')


@pytest.mark.django_db
def test_invoice_partially_paid(invoice):
    invoice.amount_paid = Decimal('400.00')
    invoice.save()
    assert invoice.amount_due == Decimal('600.00')


@pytest.mark.django_db
def test_invoice_is_overdue(invoice):
    invoice.due_date = date(2026, 1, 1)
    invoice.save()
    assert invoice.is_overdue is True


@pytest.mark.django_db
def test_invoice_not_overdue_when_paid(invoice):
    invoice.amount_paid = invoice.total
    invoice.save()
    assert invoice.is_overdue is False


@pytest.mark.django_db
def test_invoice_line_subtotal(company, tenant, invoice):
    account = Account.objects.create(
        company=company, tenant=tenant,
        code='4001', name='Revenue',
        account_type=AccountType.REVENUE, currency='USD'
    )
    line = CustomerInvoiceLine.objects.create(
        tenant=tenant,
        invoice=invoice,
        account=account,
        description='Service Fee',
        quantity=Decimal('5.00'),
        unit_price=Decimal('200.00'),
        discount=Decimal('10.00')
    )
    assert line.subtotal == Decimal('900.0000')
