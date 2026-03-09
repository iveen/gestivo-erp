from decimal import Decimal
from django.db import models
from apps.core.models import BaseModel


class BillOfMaterials(BaseModel):
    company  = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    product  = models.ForeignKey(
                   'inventory.Product', on_delete=models.PROTECT,
                   related_name='boms'
               )
    version  = models.CharField(max_length=20, default='1.0')
    quantity = models.DecimalField(max_digits=20, decimal_places=4, default=1)
    BOM_TYPES = [
        ('manufacture',  'Manufacture'),
        ('kit',          'Kit'),
        ('subcontract',  'Subcontract'),
    ]
    bom_type = models.CharField(max_length=20, choices=BOM_TYPES, default='manufacture')
    notes    = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Bill of Materials'
        verbose_name_plural = 'Bills of Materials'

    def __str__(self):
        return f'BOM - {self.product.name} v{self.version}'


class BOMLine(BaseModel):
    bom       = models.ForeignKey(
                    BillOfMaterials, on_delete=models.CASCADE,
                    related_name='lines'
                )
    component = models.ForeignKey(
                    'inventory.Product', on_delete=models.PROTECT,
                    related_name='used_in_boms'
                )
    quantity  = models.DecimalField(max_digits=20, decimal_places=4)
    uom       = models.ForeignKey('inventory.UnitOfMeasure', on_delete=models.PROTECT)
    notes     = models.TextField(blank=True)

    def __str__(self):
        return f'{self.component.sku} x {self.quantity}'


class WorkCenter(BaseModel):
    company   = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    name      = models.CharField(max_length=100)
    code      = models.CharField(max_length=20)
    TYPES = [
        ('machine', 'Machine'),
        ('human',   'Human'),
        ('both',    'Machine + Human'),
    ]
    center_type     = models.CharField(max_length=20, choices=TYPES, default='human')
    capacity        = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    cost_per_hour   = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    class Meta:
        unique_together = [('company', 'code')]

    def __str__(self):
        return f'{self.code} - {self.name}'


class ManufacturingOrder(BaseModel):
    company        = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    bom            = models.ForeignKey(BillOfMaterials, on_delete=models.PROTECT)
    product        = models.ForeignKey(
                         'inventory.Product', on_delete=models.PROTECT,
                         related_name='manufacturing_orders'
                     )
    quantity       = models.DecimalField(max_digits=20, decimal_places=4)
    scheduled_date = models.DateField()
    MO_TYPES = [
        ('mts',         'Make to Stock'),
        ('mto',         'Make to Order'),
        ('subcontract', 'Subcontract'),
    ]
    mo_type = models.CharField(max_length=20, choices=MO_TYPES, default='mts')
    STATES = [
        ('draft',       'Draft'),
        ('confirmed',   'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done',        'Done'),
        ('cancelled',   'Cancelled'),
    ]
    state  = models.CharField(max_length=20, choices=STATES, default='draft')
    origin = models.CharField(max_length=100, blank=True)
    notes  = models.TextField(blank=True)

    def confirm(self):
        if self.state != 'draft':
            raise ValueError('Only draft orders can be confirmed.')
        self.state = 'confirmed'
        self.save(update_fields=['state', 'updated_at'])

    def __str__(self):
        return f'MO-{self.id} - {self.product.name}'


class WorkOrder(BaseModel):
    manufacturing_order = models.ForeignKey(
                              ManufacturingOrder, on_delete=models.CASCADE,
                              related_name='work_orders'
                          )
    work_center         = models.ForeignKey(WorkCenter, on_delete=models.PROTECT)
    operation_name      = models.CharField(max_length=100)
    sequence            = models.PositiveIntegerField(default=10)
    planned_hours       = models.DecimalField(max_digits=8, decimal_places=2)
    actual_hours        = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    STATES = [
        ('pending',     'Pending'),
        ('in_progress', 'In Progress'),
        ('done',        'Done'),
    ]
    state                = models.CharField(max_length=20, choices=STATES, default='pending')
    project_phase        = models.CharField(max_length=100, blank=True)
    location_description = models.TextField(blank=True)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        return f'{self.operation_name} - {self.manufacturing_order}'
