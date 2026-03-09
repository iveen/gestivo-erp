from datetime import date
from decimal import Decimal
from apps.finance.models import CustomerInvoice


def generate_ar_aging(company, as_of: date = None):
    as_of = as_of or date.today()

    buckets = {
        'current': {'items': [], 'total': Decimal('0')},
        '1_30':    {'items': [], 'total': Decimal('0')},
        '31_60':   {'items': [], 'total': Decimal('0')},
        '61_90':   {'items': [], 'total': Decimal('0')},
        'over_90': {'items': [], 'total': Decimal('0')},
    }

    invoices = CustomerInvoice.objects.filter(
        company=company,
        status__in=['sent', 'overdue'],
    ).select_related('customer')

    for invoice in invoices:
        due = invoice.amount_due
        if due <= 0:
            continue

        days = (as_of - invoice.due_date).days

        item = {
            'invoice_number': invoice.invoice_number,
            'customer':       invoice.customer.name,
            'due_date':       invoice.due_date,
            'amount_due':     due,
            'days_overdue':   days,
        }

        if days <= 0:
            bucket = 'current'
        elif days <= 30:
            bucket = '1_30'
        elif days <= 60:
            bucket = '31_60'
        elif days <= 90:
            bucket = '61_90'
        else:
            bucket = 'over_90'

        buckets[bucket]['items'].append(item)
        buckets[bucket]['total'] += due

    return {
        'as_of':       as_of,
        'buckets':     buckets,
        'grand_total': sum(b['total'] for b in buckets.values()),
    }
