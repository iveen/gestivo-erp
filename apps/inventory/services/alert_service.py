from decimal import Decimal
from django.db.models import Sum
from apps.inventory.models import Product, StockQuant


def get_low_stock_products(company):
    """
    Returns a list of products that are at or below their reorder point.
    """
    products = Product.objects.filter(
        company=company,
        is_active=True,
        reorder_point__gt=0
    )

    alerts = []
    for product in products:
        on_hand = StockQuant.objects.filter(
            product=product,
            location__location_type='internal'
        ).aggregate(total=Sum('quantity'))['total'] or Decimal('0')

        if on_hand <= product.reorder_point:
            alerts.append({
                'product':       product.name,
                'sku':           product.sku,
                'on_hand':       on_hand,
                'reorder_point': product.reorder_point,
                'reorder_qty':   product.reorder_qty,
                'shortage':      product.reorder_point - on_hand,
            })

    return alerts
