from rest_framework import serializers
from .models import BillOfMaterials, BOMLine, WorkCenter, ManufacturingOrder, WorkOrder


class BOMLineSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BOMLine
        fields = ['id', 'component', 'quantity', 'uom', 'notes']


class BillOfMaterialsSerializer(serializers.ModelSerializer):
    lines = BOMLineSerializer(many=True, read_only=True)

    class Meta:
        model  = BillOfMaterials
        fields = ['id', 'product', 'version', 'quantity', 'bom_type', 'notes', 'lines']


class WorkCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WorkCenter
        fields = ['id', 'name', 'code', 'center_type', 'capacity', 'cost_per_hour']


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WorkOrder
        fields = [
            'id', 'work_center', 'operation_name', 'sequence',
            'planned_hours', 'actual_hours', 'state',
            'project_phase', 'location_description'
        ]


class ManufacturingOrderSerializer(serializers.ModelSerializer):
    work_orders = WorkOrderSerializer(many=True, read_only=True)

    class Meta:
        model  = ManufacturingOrder
        fields = [
            'id', 'bom', 'product', 'quantity', 'scheduled_date',
            'mo_type', 'state', 'origin', 'notes', 'work_orders'
        ]
