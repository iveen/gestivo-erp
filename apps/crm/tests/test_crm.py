import pytest
from decimal import Decimal
from apps.crm.models import Lead
from apps.tenants.models import Tenant
from apps.accounts.models import Company, User


@pytest.fixture
def tenant():
    return Tenant.objects.create(name='CRM Tenant', slug='crm-tenant')


@pytest.fixture
def company(tenant):
    return Company.objects.create(name='CRM Company', tenant=tenant)


@pytest.fixture
def user():
    return User.objects.create_user(
        email='crm@test.com',
        password='pass123',
        first_name='CRM',
        last_name='User'
    )


@pytest.fixture
def lead(company, tenant, user):
    return Lead.objects.create(
        company=company, tenant=tenant,
        name='Big Deal', contact='John Doe',
        email='john@example.com',
        stage='negotiation',
        probability=Decimal('75.00'),
        expected_revenue=Decimal('50000.00'),
        salesperson=user
    )


@pytest.mark.django_db
def test_mark_lead_won(lead):
    lead.mark_won()
    lead.refresh_from_db()
    assert lead.stage == 'won'
    assert lead.probability == Decimal('100.00')


@pytest.mark.django_db
def test_mark_lead_lost(lead):
    lead.mark_lost()
    lead.refresh_from_db()
    assert lead.stage == 'lost'
    assert lead.probability == Decimal('0.00')


@pytest.mark.django_db
def test_lost_lead_cannot_be_won(lead):
    lead.mark_lost()
    with pytest.raises(ValueError):
        lead.mark_won()


@pytest.mark.django_db
def test_won_lead_cannot_be_lost(lead):
    lead.mark_won()
    with pytest.raises(ValueError):
        lead.mark_lost()


@pytest.mark.django_db
def test_lead_default_stage_is_new(company, tenant):
    lead = Lead.objects.create(
        company=company, tenant=tenant,
        name='New Lead',
        expected_revenue=Decimal('1000.00')
    )
    assert lead.stage == 'new'
    assert lead.probability == Decimal('0.00')