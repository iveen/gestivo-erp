from rest_framework import serializers
from .models import PurchaseOrder, PurchaseOrderLine
from apps.contacts.serializers import ContactSerializer  # noqa


class PurchaseOrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PurchaseOrderLine
        fields = [
            'id', 'product', 'description',
            'quantity', 'unit_price', 'subtotal'
        ]


class PurchaseOrderSerializer(serializers.ModelSerializer):
    lines       = PurchaseOrderLineSerializer(many=True, read_only=True)
    approved_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model  = PurchaseOrder
        fields = [
            'id', 'vendor', 'vendor_name', 'order_date', 'expected_date',
            'currency', 'subtotal', 'tax_amount', 'total',
            'notes', 'status', 'approved_by', 'approved_at', 'lines'
        ]
