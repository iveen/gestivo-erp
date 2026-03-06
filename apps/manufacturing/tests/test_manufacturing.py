import pytest
from decimal import Decimal
from datetime import date
from apps.manufacturing.models import (
    BillOfMaterials, BOMLine, WorkCenter,
    ManufacturingOrder, WorkOrder
)
from apps.inventory.models import Product, ProductCategory, UnitOfMeasure
from apps.tenants.models import Tenant
from apps.accounts.models import Company


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='MFG Tenant', slug='mfg-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='MFG Company', tenant=tenant)


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
def finished_product(company, tenant, category, uom):
    return Product.objects.create(
        company=company, tenant=tenant,
        name='Finished Product', sku='FIN-001',
        category=category, uom=uom,
        cost=Decimal('50.00'), sales_price=Decimal('100.00'),
        valuation_method='average'
    )


@pytest.fixture
def component(company, tenant, category, uom):
    return Product.objects.create(
        company=company, tenant=tenant,
        name='Component A', sku='COMP-001',
        category=category, uom=uom,
        cost=Decimal('10.00'), sales_price=Decimal('15.00'),
        valuation_method='average'
    )


@pytest.fixture
def bom(company, tenant, finished_product):
    return BillOfMaterials.objects.create(
        company=company, tenant=tenant,
        product=finished_product,
        quantity=Decimal('1.00'),
        bom_type='manufacture'
    )


@pytest.fixture
def work_center(company, tenant):
    return WorkCenter.objects.create(
        company=company, tenant=tenant,
        name='Assembly Line', code='AL-01',
        center_type='human',
        cost_per_hour=Decimal('25.00')
    )


@pytest.mark.django_db
def test_bom_line_created(bom, component, uom, tenant):
    line = BOMLine.objects.create(
        tenant=tenant, bom=bom,
        component=component,
        quantity=Decimal('2.00'),
        uom=uom
    )
    assert line.quantity == Decimal('2.00')
    assert line.component == component


@pytest.mark.django_db
def test_manufacturing_order_confirm(company, tenant, bom, finished_product):
    mo = ManufacturingOrder.objects.create(
        company=company, tenant=tenant,
        bom=bom, product=finished_product,
        quantity=Decimal('10.00'),
        scheduled_date=date(2026, 4, 1),
        mo_type='mts', state='draft'
    )
    mo.confirm()
    mo.refresh_from_db()
    assert mo.state == 'confirmed'


@pytest.mark.django_db
def test_confirmed_order_cannot_be_confirmed_again(company, tenant, bom, finished_product):
    mo = ManufacturingOrder.objects.create(
        company=company, tenant=tenant,
        bom=bom, product=finished_product,
        quantity=Decimal('10.00'),
        scheduled_date=date(2026, 4, 1),
        mo_type='mts', state='confirmed'
    )
    with pytest.raises(ValueError):
        mo.confirm()


@pytest.mark.django_db
def test_work_order_created(company, tenant, bom, finished_product, work_center):
    mo = ManufacturingOrder.objects.create(
        company=company, tenant=tenant,
        bom=bom, product=finished_product,
        quantity=Decimal('10.00'),
        scheduled_date=date(2026, 4, 1),
        mo_type='mts', state='confirmed'
    )
    wo = WorkOrder.objects.create(
        tenant=tenant,
        manufacturing_order=mo,
        work_center=work_center,
        operation_name='Assembly',
        sequence=10,
        planned_hours=Decimal('4.00')
    )
    assert wo.state == 'pending'
    assert wo.actual_hours == Decimal('0.00')