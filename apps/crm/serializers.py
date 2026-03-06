from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    salesperson = serializers.StringRelatedField(read_only=True)

    class Meta:
        model  = Lead
        fields = [
            'id', 'name', 'contact', 'email', 'phone',
            'stage', 'probability', 'expected_revenue',
            'salesperson', 'sales_order', 'expected_close',
            'notes', 'is_active'
        ]