from rest_framework import serializers
from .models import PurchaseOrder, PurchaseOrderLine


class PurchaseOrderLineSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_sku  = serializers.ReadOnlyField(source='product.sku')

    class Meta:
        model  = PurchaseOrderLine
        fields = [
            'id', 'product', 'product_name', 'product_sku',
            'description', 'quantity', 'unit_price', 'subtotal'
        ]
        read_only_fields = ['id', 'subtotal']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    lines       = PurchaseOrderLineSerializer(many=True, required=False)
    approved_by = serializers.StringRelatedField(read_only=True)
    vendor_name = serializers.ReadOnlyField(source='vendor.name')

    class Meta:
        model  = PurchaseOrder
        fields = [
            'id', 'vendor', 'vendor_name', 'order_date', 'expected_date',
            'currency', 'subtotal', 'tax_amount', 'total',
            'notes', 'status', 'approved_by', 'approved_at', 'lines'
        ]
        read_only_fields = ['id', 'subtotal', 'total', 'status', 'approved_by', 'approved_at']

    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        po = PurchaseOrder.objects.create(**validated_data)
        subtotal = 0
        for line in lines_data:
            l = PurchaseOrderLine.objects.create(order=po, tenant=po.tenant, **line)
            subtotal += l.subtotal
        po.subtotal = subtotal
        po.total    = subtotal + po.tax_amount
        po.save(update_fields=['subtotal', 'total'])
        return po

    def update(self, instance, validated_data):
        lines_data = validated_data.pop('lines', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if lines_data is not None:
            instance.lines.all().delete()
            subtotal = 0
            for line in lines_data:
                l = PurchaseOrderLine.objects.create(order=instance, **line)
                subtotal += l.subtotal
            instance.subtotal = subtotal
            instance.total    = subtotal + instance.tax_amount
            instance.save(update_fields=['subtotal', 'total'])
        return instance
