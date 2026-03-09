from decimal import Decimal
from datetime import date
from apps.finance.models import ExchangeRate
from apps.finance.exceptions import CurrencyMismatchError


def get_exchange_rate(from_code: str, to_code: str, on_date: date = None) -> Decimal:
    if from_code == to_code:
        return Decimal('1')

    on_date = on_date or date.today()

    try:
        rate = ExchangeRate.objects.filter(
            base_currency__code=from_code,
            target_currency__code=to_code,
            rate_date__lte=on_date,
        ).latest('rate_date').rate
    except ExchangeRate.DoesNotExist:
        raise CurrencyMismatchError(
            f'No exchange rate found for {from_code}/{to_code} on {on_date}'
        )

    return rate


def convert_amount(
    amount: Decimal,
    from_code: str,
    to_code: str,
    on_date: date = None
) -> Decimal:
    rate = get_exchange_rate(from_code, to_code, on_date)
    return (amount * rate).quantize(Decimal('0.0001'))
