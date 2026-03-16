from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import (
    Account, AccountType, Journal, JournalEntry, JournalEntryLine,
    VendorBill, VendorBillLine, CustomerInvoice, CustomerInvoiceLine
)
from .exceptions import UnbalancedJournalEntryError


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Account
        fields = ['id', 'code', 'name', 'account_type', 'currency', 'is_active']


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Journal
        fields = ['id', 'name', 'code', 'journal_type', 'is_active']


class JournalEntryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model  = JournalEntryLine
        fields = ['id', 'account', 'label', 'debit', 'credit']
        read_only_fields = ['id']


class JournalEntrySerializer(serializers.ModelSerializer):
    lines      = JournalEntryLineSerializer(many=True)
    journal_name = serializers.ReadOnlyField(source='journal.name')

    class Meta:
        model  = JournalEntry
        fields = ['id', 'journal', 'journal_name', 'date', 'reference', 'is_posted', 'lines']
        read_only_fields = ['id', 'is_posted']

    def validate(self, data):
        lines = data.get('lines', [])
        total_debit  = sum(l.get('debit',  0) for l in lines)
        total_credit = sum(l.get('credit', 0) for l in lines)
        if lines and total_debit != total_credit:
            raise serializers.ValidationError(
                f'Debits ({total_debit}) must equal credits ({total_credit}).'
            )
        return data

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        entry = JournalEntry.objects.create(**validated_data)
        for line in lines_data:
            JournalEntryLine.objects.create(entry=entry, tenant=entry.tenant, **line)
        return entry


# ── AP ──────────────────────────────────────────────────────────────────────

class VendorBillLineSerializer(serializers.ModelSerializer):
    account_name = serializers.ReadOnlyField(source='account.name')

    class Meta:
        model  = VendorBillLine
        fields = ['id', 'account', 'account_name', 'description', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['id', 'subtotal']


class VendorBillSerializer(serializers.ModelSerializer):
    lines       = VendorBillLineSerializer(many=True, required=False)
    amount_due  = serializers.ReadOnlyField()
    is_overdue  = serializers.ReadOnlyField()
    vendor_name = serializers.ReadOnlyField(source='vendor.name')

    class Meta:
        model  = VendorBill
        fields = [
            'id', 'vendor', 'vendor_name', 'bill_number', 'bill_date', 'due_date',
            'subtotal', 'tax_amount', 'total', 'amount_paid',
            'amount_due', 'is_overdue', 'notes', 'status', 'lines'
        ]
        read_only_fields = ['id', 'subtotal', 'total', 'status']

    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        bill = VendorBill.objects.create(subtotal=0, total=0, **validated_data)
        subtotal = 0
        for line in lines_data:
            l = VendorBillLine.objects.create(bill=bill, tenant=bill.tenant, **line)
            subtotal += l.subtotal
        bill.subtotal = subtotal
        bill.total    = subtotal + bill.tax_amount
        bill.save(update_fields=['subtotal', 'total'])
        return bill

    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if lines_data is not None:
            instance.lines.all().delete()
            subtotal = 0
            for line in lines_data:
                l = VendorBillLine.objects.create(bill=instance, tenant=instance.tenant, **line)
                subtotal += l.subtotal
            instance.subtotal = subtotal
            instance.total    = subtotal + instance.tax_amount
            instance.save(update_fields=['subtotal', 'total'])
        return instance


# ── AR ──────────────────────────────────────────────────────────────────────

class CustomerInvoiceLineSerializer(serializers.ModelSerializer):
    account_name = serializers.ReadOnlyField(source='account.name')

    class Meta:
        model  = CustomerInvoiceLine
        fields = ['id', 'account', 'account_name', 'description', 'quantity', 'unit_price', 'discount', 'subtotal']
        read_only_fields = ['id', 'subtotal']


class CustomerInvoiceSerializer(serializers.ModelSerializer):
    lines         = CustomerInvoiceLineSerializer(many=True, required=False)
    amount_due    = serializers.ReadOnlyField()
    is_overdue    = serializers.ReadOnlyField()
    customer_name = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model  = CustomerInvoice
        fields = [
            'id', 'customer', 'customer_name', 'invoice_number', 'invoice_date', 'due_date',
            'subtotal', 'tax_amount', 'total', 'amount_paid',
            'amount_due', 'is_overdue', 'notes', 'status', 'lines'
        ]
        read_only_fields = ['id', 'subtotal', 'total', 'status']

    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        invoice = CustomerInvoice.objects.create(subtotal=0, total=0, **validated_data)
        subtotal = 0
        for line in lines_data:
            l = CustomerInvoiceLine.objects.create(invoice=invoice, tenant=invoice.tenant, **line)
            subtotal += l.subtotal
        invoice.subtotal = subtotal
        invoice.total    = subtotal + invoice.tax_amount
        invoice.save(update_fields=['subtotal', 'total'])
        return invoice

    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if lines_data is not None:
            instance.lines.all().delete()
            subtotal = 0
            for line in lines_data:
                l = CustomerInvoiceLine.objects.create(invoice=instance, tenant=instance.tenant, **line)
                subtotal += l.subtotal
            instance.subtotal = subtotal
            instance.total    = subtotal + instance.tax_amount
            instance.save(update_fields=['subtotal', 'total'])
        return instance
