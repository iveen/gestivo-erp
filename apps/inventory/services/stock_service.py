from decimal import Decimal
from django.db import transaction
from apps.inventory.models import StockMove, StockQuant, Product


@transaction.atomic
def process_stock_move(move: StockMove):
    """Process a confirmed stock move — updates StockQuant for source and destination."""

    if move.state != 'confirmed':
        raise ValueError('Only confirmed moves can be processed.')

    # Deduct from source
    if move.source.location_type != 'vendor':
        source_quant, _ = StockQuant.objects.get_or_create(
            product=move.product,
            location=move.source,
            defaults={'tenant': move.tenant, 'quantity': Decimal('0')}
        )
        source_quant.quantity -= move.quantity
        source_quant.save()

    # Add to destination
    if move.destination.location_type != 'customer':
        dest_quant, _ = StockQuant.objects.get_or_create(
            product=move.product,
            location=move.destination,
            defaults={'tenant': move.tenant, 'quantity': Decimal('0')}
        )
        dest_quant.quantity += move.quantity
        dest_quant.save()

    # Update move state
    move.state = 'done'
    move.save(update_fields=['state', 'updated_at'])

    # Update product cost if receipt (from vendor)
    if move.source.location_type == 'vendor':
        _update_product_cost(move)

    return move


def _update_product_cost(move: StockMove):
    """Update product cost using weighted average costing."""
    product = move.product

    if product.valuation_method == 'average':
        from django.db.models import Sum
        current_qty = StockQuant.objects.filter(
            product=product,
            location__location_type='internal'
        ).aggregate(total=Sum('quantity'))['total'] or Decimal('0')

        current_cost = product.cost
        new_qty      = move.quantity
        new_cost     = move.unit_cost

        if current_qty > 0:
            avg_cost = (
                (current_qty * current_cost) + (new_qty * new_cost)
            ) / (current_qty + new_qty)
            product.cost = avg_cost.quantize(Decimal('0.0001'))
            product.save(update_fields=['cost', 'updated_at'])


def get_stock_on_hand(product: Product) -> Decimal:
    """Returns total quantity across all internal locations."""
    from django.db.models import Sum
    result = StockQuant.objects.filter(
        product=product,
        location__location_type='internal'
    ).aggregate(total=Sum('quantity'))
    return result['total'] or Decimal('0')


def get_available_quantity(product: Product) -> Decimal:
    """Returns quantity minus reserved across all internal locations."""
    from django.db.models import Sum
    result = StockQuant.objects.filter(
        product=product,
        location__location_type='internal'
    ).aggregate(
        total_qty=Sum('quantity'),
        total_reserved=Sum('reserved')
    )
    qty      = result['total_qty']      or Decimal('0')
    reserved = result['total_reserved'] or Decimal('0')
    return qty - reserved
