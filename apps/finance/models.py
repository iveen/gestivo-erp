import uuid
from django.db import models
from apps.core.models import BaseModel
from decimal import Decimal
from apps.finance.exceptions import UnbalancedJournalEntryError

BALANCE_TOLERANCE = Decimal('0.0001')

class AccountType(models.TextChoices):
    ASSET     = 'asset',     'Asset'
    LIABILITY = 'liability', 'Liability'
    EQUITY    = 'equity',    'Equity'
    REVENUE   = 'revenue',   'Revenue'
    EXPENSE   = 'expense',   'Expense'


class Account(BaseModel):
    company      = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    code         = models.CharField(max_length=20)
    name         = models.CharField(max_length=200)
    account_type = models.CharField(max_length=20, choices=AccountType.choices)
    parent       = models.ForeignKey(
                       'self', null=True, blank=True,
                       on_delete=models.PROTECT, related_name='children'
                   )
    description      = models.TextField(blank=True)
    is_reconcilable  = models.BooleanField(default=False)
    currency         = models.CharField(max_length=3, default='USD')

    class Meta:
        unique_together = [('company', 'code')]

    @property
    def normal_balance(self):
        return 'debit' if self.account_type in (
            AccountType.ASSET, AccountType.EXPENSE
        ) else 'credit'

    def __str__(self):
        return f'{self.code} - {self.name}'

class FiscalYear(BaseModel):
    company    = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    name       = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date   = models.DateField()
    is_closed  = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.company.name} - {self.name}'


class FiscalPeriod(BaseModel):
    fiscal_year = models.ForeignKey(
                      FiscalYear, on_delete=models.PROTECT,
                      related_name='periods'
                  )
    name        = models.CharField(max_length=50)
    start_date  = models.DateField()
    end_date    = models.DateField()
    is_closed   = models.BooleanField(default=False)

    def close(self):
        self.is_closed = True
        self.save(update_fields=['is_closed', 'updated_at'])

    def __str__(self):
        return f'{self.fiscal_year.name} - {self.name}'

class Journal(BaseModel):
    company      = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    name         = models.CharField(max_length=100)
    code         = models.CharField(max_length=10)
    TYPES = [
        ('sales',    'Sales'),
        ('purchase', 'Purchase'),
        ('cash',     'Cash'),
        ('bank',     'Bank'),
        ('general',  'General'),
        ('opening',  'Opening'),
    ]
    journal_type = models.CharField(max_length=20, choices=TYPES, default='general')

    class Meta:
        unique_together = [('company', 'code')]

    def __str__(self):
        return f'{self.code} - {self.name}'


class JournalEntry(BaseModel):
    journal     = models.ForeignKey(Journal, on_delete=models.PROTECT)
    date        = models.DateField()
    reference   = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    is_posted   = models.BooleanField(default=False)
    period      = models.ForeignKey(
                      FiscalPeriod, on_delete=models.PROTECT,
                      null=True, blank=True
                  )

    @staticmethod
    def validate_balance(lines, raise_on_error=False):
        total_debit  = sum(Decimal(str(line["debit"]))  for line in lines)
        total_credit = sum(Decimal(str(line["credit"])) for line in lines)
        diff = abs(total_debit - total_credit)
        if diff <= BALANCE_TOLERANCE:
            return True
        if raise_on_error:
            raise UnbalancedJournalEntryError(
                f'Entry unbalanced by {diff}. Debits: {total_debit}, Credits: {total_credit}'
            )
        return False

    def post(self):
        from django.db import transaction
        with transaction.atomic():
            lines = list(self.lines.values('debit', 'credit'))
            self.validate_balance(lines, raise_on_error=True)
            self.is_posted = True
            self.save(update_fields=['is_posted', 'updated_at'])

    def __str__(self):
        return f'{self.journal.code} - {self.date} - {self.reference}'


class JournalEntryLine(BaseModel):
    entry       = models.ForeignKey(
                      JournalEntry, on_delete=models.CASCADE,
                      related_name='lines'
                  )
    account     = models.ForeignKey(Account, on_delete=models.PROTECT)
    debit       = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    credit      = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(debit__gte=0) & models.Q(credit__gte=0),
                name='non_negative_amounts'
            )
        ]

    def __str__(self):
        return f'{self.account.code} - Dr:{self.debit} Cr:{self.credit}'

class Currency(models.Model):
    code     = models.CharField(max_length=3, unique=True)
    name     = models.CharField(max_length=100)
    symbol   = models.CharField(max_length=5)
    is_base  = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code} - {self.name}'


class ExchangeRate(models.Model):
    base_currency   = models.ForeignKey(
                          Currency, on_delete=models.PROTECT,
                          related_name='base_rates'
                      )
    target_currency = models.ForeignKey(
                          Currency, on_delete=models.PROTECT,
                          related_name='target_rates'
                      )
    rate      = models.DecimalField(max_digits=18, decimal_places=6)
    rate_date = models.DateField()
    source    = models.CharField(max_length=50, default='manual')

    class Meta:
        unique_together = [('base_currency', 'target_currency', 'rate_date')]
        get_latest_by   = 'rate_date'

    def __str__(self):
        return f'{self.base_currency.code}/{self.target_currency.code} - {self.rate_date}'

class VendorBill(BaseModel):
    company     = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    vendor      = models.ForeignKey('contacts.Contact', on_delete=models.PROTECT, related_name='vendor_bills')
    bill_number = models.CharField(max_length=50)
    bill_date   = models.DateField()
    due_date    = models.DateField()
    subtotal    = models.DecimalField(max_digits=20, decimal_places=4)
    tax_amount  = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    total       = models.DecimalField(max_digits=20, decimal_places=4)
    amount_paid = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    notes       = models.TextField(blank=True)
    STATUS = [
        ('draft',      'Draft'),
        ('posted',     'Posted'),
        ('paid',       'Paid'),
        ('cancelled',  'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='draft')

    @property
    def amount_due(self) -> Decimal:
        return self.total - self.amount_paid

    @property
    def is_overdue(self) -> bool:
        from datetime import date
        return self.due_date < date.today() and self.amount_due > 0

    def __str__(self):
        return f'{self.vendor.name} - {self.bill_number}'

class VendorBillLine(BaseModel):
    bill        = models.ForeignKey(VendorBill, on_delete=models.CASCADE, related_name='lines')
    account     = models.ForeignKey(Account, on_delete=models.PROTECT)
    description = models.CharField(max_length=200, blank=True)
    quantity    = models.DecimalField(max_digits=20, decimal_places=4, default=1)
    unit_price  = models.DecimalField(max_digits=20, decimal_places=4)
    subtotal    = models.DecimalField(max_digits=20, decimal_places=4)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.bill.bill_number} - {self.description}'

class CustomerInvoice(BaseModel):
    company        = models.ForeignKey('accounts.Company', on_delete=models.PROTECT)
    customer       = models.ForeignKey('contacts.Contact', on_delete=models.PROTECT, related_name='customer_invoices')
    invoice_number = models.CharField(max_length=50)
    invoice_date   = models.DateField()
    due_date       = models.DateField()
    subtotal       = models.DecimalField(max_digits=20, decimal_places=4)
    tax_amount     = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    total          = models.DecimalField(max_digits=20, decimal_places=4)
    amount_paid    = models.DecimalField(max_digits=20, decimal_places=4, default=0)
    notes          = models.TextField(blank=True)
    STATUS = [
        ('draft',      'Draft'),
        ('sent',       'Sent'),
        ('paid',       'Paid'),
        ('overdue',    'Overdue'),
        ('cancelled',  'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='draft')

    @property
    def amount_due(self) -> Decimal:
        return self.total - self.amount_paid

    @property
    def is_overdue(self) -> bool:
        from datetime import date
        return self.due_date < date.today() and self.amount_due > 0

    def __str__(self):
        return f'{self.customer.name} - {self.invoice_number}'


class CustomerInvoiceLine(BaseModel):
    invoice     = models.ForeignKey(CustomerInvoice, on_delete=models.CASCADE, related_name='lines')
    account     = models.ForeignKey(Account, on_delete=models.PROTECT)
    description = models.CharField(max_length=200, blank=True)
    quantity    = models.DecimalField(max_digits=20, decimal_places=4, default=1)
    unit_price  = models.DecimalField(max_digits=20, decimal_places=4)
    discount    = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # percent
    subtotal    = models.DecimalField(max_digits=20, decimal_places=4)

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price * (1 - self.discount / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.invoice.invoice_number} - {self.description}'
