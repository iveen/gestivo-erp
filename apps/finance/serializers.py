from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Account, Journal, JournalEntry, JournalEntryLine
from .exceptions import UnbalancedJournalEntryError


@property
def normal_balance(self) -> str:
    return 'debit' if self.account_type in (
        AccountType.ASSET, AccountType.EXPENSE
    ) else 'credit'

class AccountSerializer(serializers.ModelSerializer):
    normal_balance = serializers.ReadOnlyField()
    children_count = serializers.SerializerMethodField()

    class Meta:
        model  = Account
        fields = [
            'id', 'code', 'name', 'account_type', 'parent',
            'normal_balance', 'description', 'is_reconcilable',
            'currency', 'children_count', 'is_active'
        ]

    @extend_schema_field(serializers.IntegerField())
    def get_children_count(self, obj):
        return obj.children.count()


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Journal
        fields = ['id', 'name', 'code', 'journal_type', 'is_active']


class JournalEntryLineSerializer(serializers.ModelSerializer):
    account_name = serializers.ReadOnlyField(source='account.name')
    account_code = serializers.ReadOnlyField(source='account.code')

    class Meta:
        model  = JournalEntryLine
        fields = [
            'id', 'account', 'account_name', 'account_code',
            'debit', 'credit', 'description'
        ]


class JournalEntrySerializer(serializers.ModelSerializer):
    lines = JournalEntryLineSerializer(many=True)

    class Meta:
        model  = JournalEntry
        fields = [
            'id', 'journal', 'date', 'reference',
            'description', 'is_posted', 'lines'
        ]

    def validate(self, data):
        lines = data.get('lines', [])
        if lines:
            try:
                JournalEntry.validate_balance(lines, raise_on_error=True)
            except UnbalancedJournalEntryError as e:
                raise serializers.ValidationError({'lines': str(e)})
        return data

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        entry = JournalEntry.objects.create(**validated_data)
        for line in lines_data:
            JournalEntryLine.objects.create(entry=entry, **line)
        return entry