from django.db import models
from apps.core.models import BaseModel


class Contact(BaseModel):
    CONTACT_TYPES = [
        ('company', 'Company'),
        ('person',  'Person'),
    ]
    tenant       = models.ForeignKey('tenants.Tenant', on_delete=models.PROTECT)
    company      = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    contact_type = models.CharField(max_length=10, choices=CONTACT_TYPES, default='company')
    parent       = models.ForeignKey(
                       'self', on_delete=models.CASCADE,
                       null=True, blank=True, related_name='persons'
                   )
    name         = models.CharField(max_length=200)
    tax_id       = models.CharField(max_length=50, blank=True)
    email        = models.EmailField(blank=True)
    phone        = models.CharField(max_length=30, blank=True)
    address      = models.TextField(blank=True)
    currency     = models.CharField(max_length=3, default='USD')
    payment_terms = models.PositiveIntegerField(default=30)  # days
    notes        = models.TextField(blank=True)
    is_vendor    = models.BooleanField(default=False)
    is_customer  = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ContactPoint(BaseModel):
    POINT_TYPES = [
        ('billing',  'Billing'),
        ('orders',   'Orders'),
        ('shipping', 'Shipping'),
        ('general',  'General'),
        ('other',    'Other'),
    ]
    contact      = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_points')
    type         = models.CharField(max_length=20, choices=POINT_TYPES, default='general')
    name         = models.CharField(max_length=200)
    email        = models.EmailField(blank=True)
    phone        = models.CharField(max_length=30, blank=True)
    address      = models.TextField(blank=True)

    def __str__(self):
        return f'{self.contact.name} - {self.type} - {self.name}'
