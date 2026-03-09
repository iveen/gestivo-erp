from datetime import date
from decimal import Decimal
from apps.finance.models import VendorBill


def generate_ap_aging(company, as_of: date = None):
    as_of = as_of or date.today()

    buckets = {
        'current': {'items': [], 'total': Decimal('0')},
        '1_30':    {'items': [], 'total': Decimal('0')},
        '31_60':   {'items': [], 'total': Decimal('0')},
        '61_90':   {'items': [], 'total': Decimal('0')},
        'over_90': {'items': [], 'total': Decimal('0')},
    }

    bills = VendorBill.objects.filter(
        company=company,
        status='posted',
    ).select_related('vendor')

    for bill in bills:
        due = bill.amount_due
        if due <= 0:
            continue

        days = (as_of - bill.due_date).days

        item = {
            'bill_number': bill.bill_number,
            'vendor':      bill.vendor.name,
            'due_date':    bill.due_date,
            'amount_due':  due,
            'days_overdue': days,
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
        'as_of':   as_of,
        'buckets': buckets,
        'grand_total': sum(b['total'] for b in buckets.values()),
    }
