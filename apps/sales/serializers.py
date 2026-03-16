from rest_framework import serializers
from .models import SalesQuotation, SalesQuotationLine, SalesOrder


class SalesQuotationLineSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_sku  = serializers.ReadOnlyField(source='product.sku')

    class Meta:
        model  = SalesQuotationLine
        fields = [
            'id', 'product', 'product_name', 'product_sku',
            'description', 'quantity', 'unit_price', 'discount', 'subtotal'
        ]
        read_only_fields = ['id', 'subtotal']


class SalesQuotationSerializer(serializers.ModelSerializer):
    lines            = SalesQuotationLineSerializer(many=True, required=False)
    customer_name    = serializers.ReadOnlyField(source='customer.name')
    salesperson_name = serializers.ReadOnlyField(source='salesperson.get_full_name')

    class Meta:
        model  = SalesQuotation
        fields = [
            'id', 'customer', 'customer_name', 'salesperson', 'salesperson_name',
            'quotation_date', 'expiry_date', 'currency',
            'subtotal', 'tax_amount', 'total', 'notes', 'status', 'lines'
        ]
        read_only_fields = ['id', 'subtotal', 'total', 'status']

    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        quotation = SalesQuotation.objects.create(**validated_data)
        subtotal = 0
        for line in lines_data:
            l = SalesQuotationLine.objects.create(
                quotation=quotation, tenant=quotation.tenant, **line
            )
            subtotal += l.subtotal
        quotation.subtotal = subtotal
        quotation.total    = subtotal + quotation.tax_amount
        quotation.save(update_fields=['subtotal', 'total'])
        return quotation

    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if lines_data is not None:
            instance.lines.all().delete()
            subtotal = 0
            for line in lines_data:
                l = SalesQuotationLine.objects.create(
                    quotation=instance, tenant=instance.tenant, **line
                )
                subtotal += l.subtotal
            instance.subtotal = subtotal
            instance.total    = subtotal + instance.tax_amount
            instance.save(update_fields=['subtotal', 'total'])
        return instance


class SalesOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model  = SalesOrder
        fields = [
            'id', 'customer', 'customer_name', 'quotation',
            'order_date', 'currency', 'total', 'notes', 'status'
        ]
        read_only_fields = ['id', 'order_date', 'status']
