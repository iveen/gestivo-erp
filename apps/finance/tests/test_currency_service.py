import pytest
from decimal import Decimal
from datetime import date
from apps.finance.services.currency_service import get_exchange_rate, convert_amount
from apps.finance.exceptions import CurrencyMismatchError
from apps.finance.models import Currency, ExchangeRate


@pytest.mark.django_db
def test_same_currency_returns_one():
    result = get_exchange_rate('USD', 'USD')
    assert result == Decimal('1')


@pytest.mark.django_db
def test_get_exchange_rate_returns_correct_rate():
    usd = Currency.objects.create(code='USD', name='US Dollar', symbol='$')
    eur = Currency.objects.create(code='EUR', name='Euro', symbol='€')
    ExchangeRate.objects.create(
        base_currency=usd,
        target_currency=eur,
        rate=Decimal('0.920000'),
        rate_date=date(2026, 1, 1),
    )
    rate = get_exchange_rate('USD', 'EUR', date(2026, 1, 1))
    assert rate == Decimal('0.920000')


@pytest.mark.django_db
def test_missing_rate_raises_error():
    with pytest.raises(CurrencyMismatchError):
        get_exchange_rate('USD', 'JPY', date(2026, 1, 1))

@pytest.mark.django_db
def test_convert_amount():
    gbp = Currency.objects.create(code='GBP', name='British Pound', symbol='£')
    cad = Currency.objects.create(code='CAD', name='Canadian Dollar', symbol='C$')
    ExchangeRate.objects.create(
        base_currency=gbp,
        target_currency=cad,
        rate=Decimal('1.720000'),
        rate_date=date(2026, 1, 1),
    )
    result = convert_amount(Decimal('100'), 'GBP', 'CAD', date(2026, 1, 1))
    assert result == Decimal('172.0000')
