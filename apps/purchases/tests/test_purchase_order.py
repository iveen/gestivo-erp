import pytest
from decimal import Decimal
from datetime import date
from apps.purchases.models import PurchaseOrder, PurchaseOrderLine
from apps.finance.models import Vendor
from apps.inventory.models import Product, ProductCategory, UnitOfMeasure
from apps.tenants.models import Tenant
from apps.accounts.models import Company, User


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='PO Tenant', slug='po-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='PO Company', tenant=tenant)


@pytest.fixture
def user(tenant):
    return User.objects.create_user(
        email='purchasing@test.com',
        password='pass123',
        first_name='Purchase',
        last_name='Manager'
    )


@pytest.fixture
def vendor(company, tenant):
    return Vendor.objects.create(
        company=company, tenant=tenant,
        name='Test Vendor', currency='USD'
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
        name='Test Product', sku='SKU-PO-001',
        category=category, uom=uom,
        cost=Decimal('10.00'), sales_price=Decimal('15.00'),
        valuation_method='average'
    )


@pytest.fixture
def purchase_order(company, tenant, vendor):
    return PurchaseOrder.objects.create(
        company=company, tenant=tenant,
        vendor=vendor,
        order_date=date(2026, 3, 1),
        currency='USD',
        subtotal=Decimal('1000.00'),
        total=Decimal('1000.00'),
        status='draft'
    )


@pytest.mark.django_db
def test_purchase_order_line_subtotal(purchase_order, product, tenant):
    line = PurchaseOrderLine.objects.create(
        tenant=tenant,
        order=purchase_order,
        product=product,
        quantity=Decimal('10.00'),
        unit_price=Decimal('50.00')
    )
    assert line.subtotal == Decimal('500.0000')


@pytest.mark.django_db
def test_submit_for_approval(purchase_order):
    purchase_order.submit_for_approval()
    purchase_order.refresh_from_db()
    assert purchase_order.status == 'pending'


@pytest.mark.django_db
def test_draft_cannot_be_approved(purchase_order, user):
    with pytest.raises(ValueError):
        purchase_order.approve(user)


@pytest.mark.django_db
def test_approve_purchase_order(purchase_order, user):
    purchase_order.submit_for_approval()
    purchase_order.approve(user)
    purchase_order.refresh_from_db()
    assert purchase_order.status == 'approved'
    assert purchase_order.approved_by == user
    assert purchase_order.approved_at is not None


@pytest.mark.django_db
def test_cannot_submit_approved_order(purchase_order, user):
    purchase_order.submit_for_approval()
    purchase_order.approve(user)
    with pytest.raises(ValueError):
        purchase_order.submit_for_approval()
