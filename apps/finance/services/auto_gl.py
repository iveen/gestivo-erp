"""
Auto GL Journal Entry generation service.

Creates draft journal entries from source documents (vendor bills,
customer invoices) with full traceability back to the source.
"""
from datetime import date
from django.db import transaction
from apps.finance.models import Journal, JournalEntry, JournalEntryLine, JournalEntryAuditLog


def _get_company_settings(company):
    """Get or return None for company settings."""
    try:
        return company.settings
    except Exception:
        return None


def _get_default_journal(company, journal_type, settings_journal):
    """Get journal from settings or fall back to first matching journal."""
    if settings_journal:
        return settings_journal
    return Journal.objects.filter(
        company=company, journal_type=journal_type
    ).first()


def create_gl_from_vendor_bill(bill, created_by=None):
    """
    Create a draft GL journal entry from a posted vendor bill.

    Debits:  each bill line's expense account
    Credits: AP control account (from CompanySettings or vendor's account_payable)
    """
    settings = _get_company_settings(bill.company)

    # Determine AP account - vendor override > company default
    ap_account = None
    if hasattr(bill.vendor, 'account_payable') and bill.vendor.account_payable:
        ap_account = bill.vendor.account_payable
    elif settings and settings.default_ap_account:
        ap_account = settings.default_ap_account

    if not ap_account:
        return None  # Cannot create GL without AP account

    # Determine journal
    journal = _get_default_journal(
        bill.company, 'purchase',
        settings.default_ap_journal if settings else None
    )
    if not journal:
        return None

    with transaction.atomic():
        entry = JournalEntry.objects.create(
            tenant=bill.tenant,
            journal=journal,
            date=bill.bill_date,
            reference=bill.bill_number,
            description=f'Vendor Bill: {bill.vendor.name} - {bill.bill_number}',
            is_posted=False,
            source_type='vendor_bill',
            source_id=bill.id,
        )

        # Debit each expense line
        for line in bill.lines.all():
            JournalEntryLine.objects.create(
                tenant=bill.tenant,
                entry=entry,
                account=line.account,
                debit=line.subtotal,
                credit=0,
                description=line.description or f'{bill.vendor.name} - {line.account.name}',
            )

        # Credit AP control account (total)
        JournalEntryLine.objects.create(
            tenant=bill.tenant,
            entry=entry,
            account=ap_account,
            debit=0,
            credit=bill.total,
            description=f'AP: {bill.vendor.name} - {bill.bill_number}',
        )

        # Audit log
        JournalEntryAuditLog.objects.create(
            tenant=bill.tenant,
            entry=entry,
            changed_by=created_by,
            change_type='line_added',
            description=f'Auto-generated from Vendor Bill {bill.bill_number}',
            before_data=None,
            after_data={
                'source_type': 'vendor_bill',
                'source_id':   str(bill.id),
                'bill_number': bill.bill_number,
                'vendor':      bill.vendor.name,
                'total':       str(bill.total),
            }
        )

    return entry


def create_gl_from_customer_invoice(invoice, created_by=None):
    """
    Create a draft GL journal entry from a posted customer invoice.

    Debits:  AR control account (from CompanySettings)
    Credits: each invoice line's revenue account
    """
    settings = _get_company_settings(invoice.company)

    # Determine AR account
    ar_account = None
    if settings and settings.default_ar_account:
        ar_account = settings.default_ar_account

    if not ar_account:
        return None  # Cannot create GL without AR account

    # Determine journal
    journal = _get_default_journal(
        invoice.company, 'sales',
        settings.default_ar_journal if settings else None
    )
    if not journal:
        return None

    with transaction.atomic():
        entry = JournalEntry.objects.create(
            tenant=invoice.tenant,
            journal=journal,
            date=invoice.invoice_date,
            reference=invoice.invoice_number,
            description=f'Customer Invoice: {invoice.customer.name} - {invoice.invoice_number}',
            is_posted=False,
            source_type='customer_invoice',
            source_id=invoice.id,
        )

        # Debit AR control account (total)
        JournalEntryLine.objects.create(
            tenant=invoice.tenant,
            entry=entry,
            account=ar_account,
            debit=invoice.total,
            credit=0,
            description=f'AR: {invoice.customer.name} - {invoice.invoice_number}',
        )

        # Credit each revenue line
        for line in invoice.lines.all():
            JournalEntryLine.objects.create(
                tenant=invoice.tenant,
                entry=entry,
                account=line.account,
                debit=0,
                credit=line.subtotal,
                description=line.description or f'{invoice.customer.name} - {line.account.name}',
            )

        # Audit log
        JournalEntryAuditLog.objects.create(
            tenant=invoice.tenant,
            entry=entry,
            changed_by=created_by,
            change_type='line_added',
            description=f'Auto-generated from Customer Invoice {invoice.invoice_number}',
            before_data=None,
            after_data={
                'source_type':      'customer_invoice',
                'source_id':        str(invoice.id),
                'invoice_number':   invoice.invoice_number,
                'customer':         invoice.customer.name,
                'total':            str(invoice.total),
            }
        )

    return entry


def log_journal_entry_change(entry, changed_by, change_type, description, before_data, after_data):
    """Log a manual change to an auto-generated journal entry."""
    JournalEntryAuditLog.objects.create(
        tenant=entry.tenant,
        entry=entry,
        changed_by=changed_by,
        change_type=change_type,
        description=description,
        before_data=before_data,
        after_data=after_data,
    )
