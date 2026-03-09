from decimal import Decimal
from django.db import models
from apps.core.models import BaseModel


class Lead(BaseModel):
    company  = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    name     = models.CharField(max_length=200)
    contact  = models.CharField(max_length=200, blank=True)
    email    = models.EmailField(blank=True)
    phone    = models.CharField(max_length=30, blank=True)
    STAGES = [
        ('new',          'New'),
        ('qualified',    'Qualified'),
        ('proposition',  'Proposition'),
        ('negotiation',  'Negotiation'),
        ('won',          'Won'),
        ('lost',         'Lost'),
    ]
    stage            = models.CharField(max_length=20, choices=STAGES, default='new')
    probability      = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    expected_revenue = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    salesperson      = models.ForeignKey(
                           'accounts.User', on_delete=models.PROTECT,
                           null=True, blank=True
                       )
    sales_order      = models.ForeignKey(
                           'sales.SalesOrder', on_delete=models.PROTECT,
                           null=True, blank=True, related_name='leads'
                       )
    expected_close   = models.DateField(null=True, blank=True)
    notes            = models.TextField(blank=True)

    def mark_won(self):
        if self.stage == 'lost':
            raise ValueError('Lost leads cannot be marked as won.')
        self.stage       = 'won'
        self.probability = Decimal('100.00')
        self.save(update_fields=['stage', 'probability', 'updated_at'])

    def mark_lost(self):
        if self.stage == 'won':
            raise ValueError('Won leads cannot be marked as lost.')
        self.stage       = 'lost'
        self.probability = Decimal('0.00')
        self.save(update_fields=['stage', 'probability', 'updated_at'])

    def __str__(self):
        return f'{self.name} - {self.stage}'
