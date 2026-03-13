from decimal import Decimal
from django.db import models
from apps.core.models import BaseModel


class PurchaseOrder(BaseModel):
    company       = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    vendor        = models.ForeignKey('contacts.Contact', on_delete=models.PROTECT)
    order_date    = models.DateField()
    expected_date = models.DateField(null=True, blank=True)
    currency      = models.CharField(max_length=3, default='USD')
    subtotal      = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    tax_amount    = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    total         = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    notes         = models.TextField(blank=True)
    STATUS = [
        ('draft',      'Draft'),
        ('pending',    'Pending Approval'),
        ('approved',   'Approved'),
        ('received',   'Received'),
        ('cancelled',  'Cancelled'),
    ]
    status      = models.CharField(max_length=20, choices=STATUS, default='draft')
    approved_by = models.ForeignKey(
                      'accounts.User', on_delete=models.PROTECT,
                      null=True, blank=True, related_name='approved_pos'
                  )
    approved_at = models.DateTimeField(null=True, blank=True)

    def submit_for_approval(self):
        if self.status != 'draft':
            raise ValueError('Only draft orders can be submitted for approval.')
        self.status = 'pending'
        self.save(update_fields=['status', 'updated_at'])

    def approve(self, user):
        if self.status != 'pending':
            raise ValueError('Only pending orders can be approved.')
        from django.utils import timezone
        self.status      = 'approved'
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save(update_fields=['status', 'approved_by', 'approved_at', 'updated_at'])

    def __str__(self):
        return f'PO-{self.id} - {self.vendor.name}'


class PurchaseOrderLine(BaseModel):
    order       = models.ForeignKey(
                      PurchaseOrder, on_delete=models.CASCADE,
                      related_name='lines'
                  )
    product     = models.ForeignKey('inventory.Product', on_delete=models.PROTECT)
    description = models.CharField(max_length=200, blank=True)
    quantity    = models.DecimalField(max_digits=20, decimal_places=4)
    unit_price  = models.DecimalField(max_digits=20, decimal_places=4)
    subtotal    = models.DecimalField(max_digits=20, decimal_places=4, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.sku} x {self.quantity}'
