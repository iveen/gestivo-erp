from rest_framework import serializers
from .models import (
    ProductCategory, UnitOfMeasure, Product,
    Warehouse, StockLocation, StockMove, StockQuant
)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProductCategory
        fields = ['id', 'name', 'parent', 'is_active']


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UnitOfMeasure
        fields = ['id', 'name', 'symbol', 'category']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'sku', 'barcode', 'category', 'uom',
            'cost', 'sales_price', 'valuation_method',
            'reorder_point', 'reorder_qty',
            'product_type', 'can_be_purchased', 'can_be_sold', 'digital_url',
            'is_active'
        ]


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Warehouse
        fields = ['id', 'name', 'code', 'address', 'is_active']


class StockLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StockLocation
        fields = ['id', 'warehouse', 'name', 'full_path', 'location_type', 'is_active']


class StockMoveSerializer(serializers.ModelSerializer):
    class Meta:
        model  = StockMove
        fields = [
            'id', 'product', 'source', 'destination',
            'quantity', 'unit_cost', 'move_date',
            'reference', 'state'
        ]


class StockQuantSerializer(serializers.ModelSerializer):
    available_quantity = serializers.ReadOnlyField()

    class Meta:
        model  = StockQuant
        fields = ['id', 'product', 'location', 'quantity', 'reserved', 'available_quantity']
