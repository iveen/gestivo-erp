from decimal import Decimal
from datetime import date
from apps.finance.models import Account, AccountType
from apps.finance.services.balance_service import get_account_balance


def generate_balance_sheet(company, as_of_date: date):
    accounts = Account.objects.filter(
        company=company,
        is_active=True
    ).order_by('code')

    def section(account_type):
        items = []
        total = Decimal('0')
        for acct in accounts.filter(account_type=account_type):
            balance = get_account_balance(acct, as_of_date)
            if balance != 0:
                items.append({
                    'code':    acct.code,
                    'name':    acct.name,
                    'balance': balance,
                })
                total += balance
        return {'items': items, 'total': total}

    assets      = section(AccountType.ASSET)
    liabilities = section(AccountType.LIABILITY)
    equity      = section(AccountType.EQUITY)

    diff        = assets['total'] - (liabilities['total'] + equity['total'])
    is_balanced = abs(diff) <= Decimal('0.0001')

    return {
        'as_of_date':   as_of_date,
        'currency':     company.currency,
        'assets':       assets,
        'liabilities':  liabilities,
        'equity':       equity,
        'is_balanced':  is_balanced,
        'imbalance':    diff,
    }
