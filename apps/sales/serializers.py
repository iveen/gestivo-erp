from rest_framework import serializers
from .models import SalesQuotation, SalesQuotationLine, SalesOrder


class SalesQuotationLineSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SalesQuotationLine
        fields = [
            'id', 'product', 'description',
            'quantity', 'unit_price', 'discount', 'subtotal'
        ]


class SalesQuotationSerializer(serializers.ModelSerializer):
    lines = SalesQuotationLineSerializer(many=True, read_only=True)

    class Meta:
        model  = SalesQuotation
        fields = [
            'id', 'customer', 'salesperson', 'quotation_date',
            'expiry_date', 'currency', 'subtotal', 'tax_amount',
            'total', 'notes', 'status', 'lines'
        ]


class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = SalesOrder
        fields = [
            'id', 'customer', 'quotation', 'order_date',
            'currency', 'total', 'notes', 'status'
        ]
