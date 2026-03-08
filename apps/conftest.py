import pytest


@pytest.fixture(autouse=False)
def with_tenant_company(settings, tenant, company):
    from apps.testing_middleware import InjectTenantCompanyMiddleware
    InjectTenantCompanyMiddleware._tenant  = tenant
    InjectTenantCompanyMiddleware._company = company

    settings.MIDDLEWARE = [
        m for m in settings.MIDDLEWARE
        if m not in (
            'apps.tenants.middleware.TenantMiddleware',
            'apps.accounts.middleware.CompanyMiddleware',
        )
    ] + ['apps.testing_middleware.InjectTenantCompanyMiddleware']

    return tenant, company