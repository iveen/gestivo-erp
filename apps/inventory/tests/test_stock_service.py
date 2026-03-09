import pytest
from decimal import Decimal
from django.utils import timezone
from apps.inventory.models import (
    Product, ProductCategory, UnitOfMeasure,
    Warehouse, StockLocation, StockMove, StockQuant
)
from apps.inventory.services.stock_service import (
    process_stock_move, get_stock_on_hand, get_available_quantity
)
from apps.tenants.models import Tenant
from apps.accounts.models import Company


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='Inventory Tenant', slug='inventory-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='Inventory Company', tenant=tenant)


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
        name='Test Product', sku='SKU-001',
        category=category, uom=uom,
        cost=Decimal('10.00'), sales_price=Decimal('15.00'),
        valuation_method='average'
    )


@pytest.fixture
def warehouse(company, tenant):
    return Warehouse.objects.create(
        company=company, tenant=tenant,
        name='Main Warehouse', code='WH1'
    )


@pytest.fixture
def vendor_location(warehouse, tenant):
    return StockLocation.objects.create(
        tenant=tenant, warehouse=warehouse,
        name='Vendor', full_path='WH1/VENDOR',
        location_type='vendor'
    )


@pytest.fixture
def internal_location(warehouse, tenant):
    return StockLocation.objects.create(
        tenant=tenant, warehouse=warehouse,
        name='Stock', full_path='WH1/STOCK',
        location_type='internal'
    )


@pytest.fixture
def customer_location(warehouse, tenant):
    return StockLocation.objects.create(
        tenant=tenant, warehouse=warehouse,
        name='Customer', full_path='WH1/CUSTOMER',
        location_type='customer'
    )


@pytest.mark.django_db
def test_process_receipt_updates_stock(product, vendor_location, internal_location, tenant):
    move = StockMove.objects.create(
        tenant=tenant, product=product,
        source=vendor_location,
        destination=internal_location,
        quantity=Decimal('100.00'),
        unit_cost=Decimal('10.00'),
        move_date=timezone.now(),
        state='confirmed'
    )
    process_stock_move(move)
    on_hand = get_stock_on_hand(product)
    assert on_hand == Decimal('100.00')


@pytest.mark.django_db
def test_process_delivery_reduces_stock(product, vendor_location, internal_location, customer_location, tenant):
    # First receive stock
    receipt = StockMove.objects.create(
        tenant=tenant, product=product,
        source=vendor_location,
        destination=internal_location,
        quantity=Decimal('100.00'),
        unit_cost=Decimal('10.00'),
        move_date=timezone.now(),
        state='confirmed'
    )
    process_stock_move(receipt)

    # Then deliver
    delivery = StockMove.objects.create(
        tenant=tenant, product=product,
        source=internal_location,
        destination=customer_location,
        quantity=Decimal('30.00'),
        unit_cost=Decimal('10.00'),
        move_date=timezone.now(),
        state='confirmed'
    )
    process_stock_move(delivery)
    assert get_stock_on_hand(product) == Decimal('70.00')


@pytest.mark.django_db
def test_weighted_average_cost_updated(product, vendor_location, internal_location, tenant):
    move = StockMove.objects.create(
        tenant=tenant, product=product,
        source=vendor_location,
        destination=internal_location,
        quantity=Decimal('100.00'),
        unit_cost=Decimal('12.00'),
        move_date=timezone.now(),
        state='confirmed'
    )
    process_stock_move(move)
    product.refresh_from_db()
    assert product.cost == Decimal('11.0000')


@pytest.mark.django_db
def test_unconfirmed_move_raises_error(product, vendor_location, internal_location, tenant):
    move = StockMove.objects.create(
        tenant=tenant, product=product,
        source=vendor_location,
        destination=internal_location,
        quantity=Decimal('10.00'),
        unit_cost=Decimal('10.00'),
        move_date=timezone.now(),
        state='draft'
    )
    with pytest.raises(ValueError):
        process_stock_move(move)
