import pytest
from decimal import Decimal
from django.utils import timezone
from apps.inventory.models import (
    Product, ProductCategory, UnitOfMeasure,
    Warehouse, StockLocation, StockQuant
)
from apps.inventory.services.alert_service import get_low_stock_products
from apps.tenants.models import Tenant
from apps.accounts.models import Company


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='Alert Tenant', slug='alert-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='Alert Company', tenant=tenant)


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
def warehouse(company, tenant):
    return Warehouse.objects.create(
        company=company, tenant=tenant,
        name='Main Warehouse', code='WH2'
    )


@pytest.fixture
def internal_location(warehouse, tenant):
    return StockLocation.objects.create(
        tenant=tenant, warehouse=warehouse,
        name='Stock', full_path='WH2/STOCK',
        location_type='internal'
    )


@pytest.mark.django_db
def test_no_alerts_when_stock_sufficient(company, tenant, category, uom, internal_location):
    product = Product.objects.create(
        company=company, tenant=tenant,
        name='Well Stocked', sku='SKU-100',
        category=category, uom=uom,
        cost=Decimal('10.00'), sales_price=Decimal('15.00'),
        reorder_point=Decimal('10.00'),
        reorder_qty=Decimal('50.00')
    )
    StockQuant.objects.create(
        tenant=tenant, product=product,
        location=internal_location,
        quantity=Decimal('100.00')
    )
    alerts = get_low_stock_products(company)
    assert len(alerts) == 0


@pytest.mark.django_db
def test_alert_when_stock_below_reorder_point(company, tenant, category, uom, internal_location):
    product = Product.objects.create(
        company=company, tenant=tenant,
        name='Low Stock Product', sku='SKU-101',
        category=category, uom=uom,
        cost=Decimal('10.00'), sales_price=Decimal('15.00'),
        reorder_point=Decimal('20.00'),
        reorder_qty=Decimal('50.00')
    )
    StockQuant.objects.create(
        tenant=tenant, product=product,
        location=internal_location,
        quantity=Decimal('5.00')
    )
    alerts = get_low_stock_products(company)
    assert len(alerts) == 1
    assert alerts[0]['sku'] == 'SKU-101'
    assert alerts[0]['shortage'] == Decimal('15.00')


@pytest.mark.django_db
def test_no_alert_when_reorder_point_is_zero(company, tenant, category, uom):
    Product.objects.create(
        company=company, tenant=tenant,
        name='No Reorder', sku='SKU-102',
        category=category, uom=uom,
        cost=Decimal('10.00'), sales_price=Decimal('15.00'),
        reorder_point=Decimal('0.00'),
        reorder_qty=Decimal('0.00')
    )
    alerts = get_low_stock_products(company)
    assert len(alerts) == 0