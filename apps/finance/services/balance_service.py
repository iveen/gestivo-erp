from decimal import Decimal
from django.db.models import Sum
from apps.finance.models import JournalEntryLine, Account


def get_account_balance(account: Account, as_of_date=None) -> Decimal:
    qs = JournalEntryLine.objects.filter(
        account=account,
        entry__is_posted=True,
    )
    if as_of_date:
        qs = qs.filter(entry__date__lte=as_of_date)

    result = qs.aggregate(
        total_debit=Sum('debit'),
        total_credit=Sum('credit')
    )
    debit  = result['total_debit']  or Decimal('0')
    credit = result['total_credit'] or Decimal('0')

    if account.normal_balance == 'debit':
        return debit - credit
    return credit - debit


def get_trial_balance(company, as_of_date=None):
    accounts = Account.objects.filter(
        company=company,
        is_active=True
    ).order_by('code')

    rows = []
    for acct in accounts:
        balance = get_account_balance(acct, as_of_date)
        if balance != 0:
            rows.append({
                'account': acct,
                'balance': balance,
                'debit':   balance if acct.normal_balance == 'debit'  else Decimal('0'),
                'credit':  balance if acct.normal_balance == 'credit' else Decimal('0'),
            })
    return rows