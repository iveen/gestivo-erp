import pytest
from decimal import Decimal
from datetime import date
from apps.sales.models import SalesQuotation, SalesQuotationLine, SalesOrder
from apps.finance.models import Customer
from apps.inventory.models import Product, ProductCategory, UnitOfMeasure
from apps.tenants.models import Tenant
from apps.accounts.models import Company, User


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='Sales Tenant', slug='sales-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='Sales Company', tenant=tenant)


@pytest.fixture
def user(tenant):
    return User.objects.create_user(
        email='sales@test.com',
        password='pass123',
        first_name='Sales',
        last_name='User'
    )


@pytest.fixture
def customer(company, tenant):
    return Customer.objects.create(
        company=company, tenant=tenant,
        name='Test Customer', currency='USD'
    )


@pytest.fixture
def uom(tenant):
    return UnitOfMeasure.objects.create(
        tenant=tenant, name='Unit', symbol='u', category='unit'
    )


@pytest.fixture
def category(company, tenant):
    return ProductCategory.objects.create(
        company=company, tenant=tenant, name='General'
    )


@pytest.fixture
def product(company, tenant, category, uom):
    return Product.objects.create(
        company=company, tenant=tenant,
        name='Test Product', sku='SKU-SALES-001',
        category=category, uom=uom,
        cost=Decimal('10.00'), sales_price=Decimal('20.00'),
        valuation_method='average'
    )


@pytest.fixture
def quotation(company, tenant, customer, user):
    return SalesQuotation.objects.create(
        company=company, tenant=tenant,
        customer=customer, salesperson=user,
        quotation_date=date(2026, 3, 1),
        currency='USD',
        subtotal=Decimal('1000.00'),
        total=Decimal('1000.00'),
        status='sent'
    )


@pytest.mark.django_db
def test_quotation_line_subtotal(quotation, product, tenant):
    line = SalesQuotationLine.objects.create(
        tenant=tenant, quotation=quotation,
        product=product,
        quantity=Decimal('5.00'),
        unit_price=Decimal('20.00'),
        discount=Decimal('10.00')
    )
    assert line.subtotal == Decimal('90.0000')


@pytest.mark.django_db
def test_confirm_quotation_creates_sales_order(quotation, tenant):
    order = quotation.confirm()
    assert isinstance(order, SalesOrder)
    assert order.customer == quotation.customer
    assert order.total == quotation.total
    assert order.status == 'confirmed'


@pytest.mark.django_db
def test_confirmed_quotation_status_changes(quotation, tenant):
    quotation.confirm()
    quotation.refresh_from_db()
    assert quotation.status == 'confirmed'


@pytest.mark.django_db
def test_draft_quotation_cannot_be_confirmed(company, tenant, customer, user):
    draft = SalesQuotation.objects.create(
        company=company, tenant=tenant,
        customer=customer, salesperson=user,
        quotation_date=date(2026, 3, 1),
        currency='USD', total=Decimal('500.00'),
        status='draft'
    )
    with pytest.raises(ValueError):
        draft.confirm()
