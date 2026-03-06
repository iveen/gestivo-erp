from decimal import Decimal
from django.db import models
from apps.core.models import BaseModel


class SalesQuotation(BaseModel):
    company        = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    customer       = models.ForeignKey('finance.Customer', on_delete=models.PROTECT)
    quotation_date = models.DateField()
    expiry_date    = models.DateField(null=True, blank=True)
    salesperson    = models.ForeignKey('accounts.User', on_delete=models.PROTECT)
    currency       = models.CharField(max_length=3, default='USD')
    subtotal       = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    tax_amount     = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    total          = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    notes          = models.TextField(blank=True)
    STATUS = [
        ('draft',     'Draft'),
        ('sent',      'Sent'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='draft')

    def confirm(self):
        if self.status != 'sent':
            raise ValueError('Only sent quotations can be confirmed.')
        order = SalesOrder.objects.create(
            tenant=self.tenant,
            company=self.company,
            customer=self.customer,
            quotation=self,
            currency=self.currency,
            total=self.total,
        )
        self.status = 'confirmed'
        self.save(update_fields=['status', 'updated_at'])
        return order

    def __str__(self):
        return f'QUO-{self.id} - {self.customer.name}'


class SalesQuotationLine(BaseModel):
    quotation   = models.ForeignKey(
                      SalesQuotation, on_delete=models.CASCADE,
                      related_name='lines'
                  )
    product     = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    description = models.CharField(max_length=200, blank=True)
    quantity    = models.DecimalField(max_digits=20, decimal_places=4)
    unit_price  = models.DecimalField(max_digits=20, decimal_places=4)
    discount    = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    subtotal    = models.DecimalField(max_digits=20, decimal_places=4, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price * (1 - self.discount / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.sku} x {self.quantity}'


class SalesOrder(BaseModel):
    company    = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    customer   = models.ForeignKey('finance.Customer', on_delete=models.PROTECT)
    quotation  = models.OneToOneField(
                     SalesQuotation, on_delete=models.PROTECT,
                     null=True, blank=True, related_name='order'
                 )
    order_date = models.DateField(auto_now_add=True)
    currency   = models.CharField(max_length=3, default='USD')
    total      = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    notes      = models.TextField(blank=True)
    STATUS = [
        ('confirmed',   'Confirmed'),
        ('in_delivery', 'In Delivery'),
        ('done',        'Done'),
        ('cancelled',   'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='confirmed')

    def __str__(self):
        return f'SO-{self.id} - {self.customer.name}'