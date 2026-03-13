from rest_framework import serializers
from .models import Contact, ContactPoint


class ContactPointSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ContactPoint
        fields = ['id', 'type', 'name', 'email', 'phone', 'address']
        read_only_fields = ['id']


class ContactSerializer(serializers.ModelSerializer):
    contact_points = ContactPointSerializer(many=True, read_only=True)

    class Meta:
        model  = Contact
        fields = [
            'id', 'contact_type', 'parent', 'name', 'tax_id',
            'email', 'phone', 'address', 'currency', 'payment_terms',
            'notes', 'is_vendor', 'is_customer', 'contact_points'
        ]
        read_only_fields = ['id']
