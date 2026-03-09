from decimal import Decimal
import uuid
from django.db import models
from apps.core.models import BaseModel


class ProductCategory(BaseModel):
    company = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    name    = models.CharField(max_length=100)
    parent  = models.ForeignKey(
                  'self', null=True, blank=True,
                  on_delete=models.SET_NULL, related_name='children'
              )

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name


class UnitOfMeasure(BaseModel):
    name     = models.CharField(max_length=50)
    symbol   = models.CharField(max_length=10)
    CATEGORIES = [
        ('unit',   'Unit'),
        ('weight', 'Weight'),
        ('volume', 'Volume'),
        ('length', 'Length'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORIES, default='unit')

    def __str__(self):
        return f'{self.name} ({self.symbol})'


class Product(BaseModel):
    company          = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    name             = models.CharField(max_length=200)
    sku              = models.CharField(max_length=100)
    barcode          = models.CharField(max_length=100, blank=True)
    category         = models.ForeignKey(ProductCategory, on_delete=models.PROTECT)
    uom              = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT)
    cost             = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    sales_price      = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    VALUATION_METHODS = [
        ('fifo',    'FIFO'),
        ('average', 'Weighted Average'),
    ]
    valuation_method = models.CharField(max_length=20, choices=VALUATION_METHODS, default='average')
    reorder_point    = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    reorder_qty      = models.DecimalField(max_digits=20, decimal_places=4, default=0)

    class Meta:
        unique_together = [('company', 'sku')]

    def __str__(self):
        return f'{self.sku} - {self.name}'

class Warehouse(BaseModel):
    company = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    name    = models.CharField(max_length=100)
    code    = models.CharField(max_length=10)
    address = models.TextField(blank=True)

    class Meta:
        unique_together = [('company', 'code')]

    def __str__(self):
        return f'{self.code} - {self.name}'


class StockLocation(BaseModel):
    warehouse = models.ForeignKey(
                    Warehouse, on_delete=models.PROTECT,
                    related_name='locations'
                )
    name      = models.CharField(max_length=100)
    full_path = models.CharField(max_length=200)
    TYPES = [
        ('internal',  'Internal'),
        ('customer',  'Customer'),
        ('vendor',    'Vendor'),
        ('transit',   'Transit'),
    ]
    location_type = models.CharField(max_length=20, choices=TYPES, default='internal')

    def __str__(self):
        return self.full_path



class StockMove(BaseModel):
    product     = models.ForeignKey(Product, on_delete=models.PROTECT)
    source      = models.ForeignKey(
                      StockLocation, on_delete=models.PROTECT,
                      related_name='outgoing_moves'
                  )
    destination = models.ForeignKey(
                      StockLocation, on_delete=models.PROTECT,
                      related_name='incoming_moves'
                  )
    quantity    = models.DecimalField(max_digits=20, decimal_places=4)
    unit_cost   = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    move_date   = models.DateTimeField()
    reference   = models.CharField(max_length=100, blank=True)
    STATES = [
        ('draft',       'Draft'),
        ('confirmed',   'Confirmed'),
        ('done',        'Done'),
        ('cancelled',   'Cancelled'),
    ]
    state = models.CharField(max_length=20, choices=STATES, default='draft')

    def __str__(self):
        return f'{self.product.sku} - {self.quantity} - {self.state}'


class StockQuant(BaseModel):
    product   = models.ForeignKey(Product, on_delete=models.PROTECT)
    location  = models.ForeignKey(StockLocation, on_delete=models.PROTECT)
    quantity  = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    reserved  = models.DecimalField(max_digits=20, decimal_places=4, default=0)

    class Meta:
        unique_together = [('product', 'location')]

    @property
    def available_quantity(self) -> Decimal:
        return self.quantity - self.reserved

    def __str__(self):
        return f'{self.product.sku} - {self.location.full_path} - {self.quantity}'
