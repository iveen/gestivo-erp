from decimal import Decimal
from datetime import date
from django.db.models import Sum
from apps.finance.models import Account, AccountType, JournalEntryLine


def generate_profit_loss(company, start_date: date, end_date: date):
    accounts = Account.objects.filter(
        company=company,
        is_active=True
    ).order_by('code')

    def section(account_type):
        items = []
        total = Decimal('0')
        for acct in accounts.filter(account_type=account_type):
            result = JournalEntryLine.objects.filter(
                account=acct,
                entry__is_posted=True,
                entry__date__gte=start_date,
                entry__date__lte=end_date,
            ).aggregate(
                total_debit=Sum('debit'),
                total_credit=Sum('credit')
            )
            debit  = result['total_debit']  or Decimal('0')
            credit = result['total_credit'] or Decimal('0')

            if account_type == AccountType.REVENUE:
                balance = credit - debit
            else:
                balance = debit - credit

            if balance != 0:
                items.append({
                    'code':    acct.code,
                    'name':    acct.name,
                    'balance': balance,
                })
                total += balance
        return {'items': items, 'total': total}

    revenue    = section(AccountType.REVENUE)
    expenses   = section(AccountType.EXPENSE)
    net_income = revenue['total'] - expenses['total']

    return {
        'period': {
            'start': start_date,
            'end':   end_date,
        },
        'currency':   company.currency,
        'revenue':    revenue,
        'expenses':   expenses,
        'net_income': net_income,
    }