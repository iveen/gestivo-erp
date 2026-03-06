import pytest
from decimal import Decimal
from apps.finance.models import JournalEntry
from apps.finance.exceptions import UnbalancedJournalEntryError


@pytest.mark.unit
def test_balanced_entry_is_valid():
    lines = [
        {'debit': Decimal('1000.00'), 'credit': Decimal('0.00')},
        {'debit': Decimal('0.00'),    'credit': Decimal('1000.00')},
    ]
    assert JournalEntry.validate_balance(lines) is True


@pytest.mark.unit
def test_unbalanced_entry_raises_error():
    lines = [
        {'debit': Decimal('1000.00'), 'credit': Decimal('0.00')},
        {'debit': Decimal('0.00'),    'credit': Decimal('999.99')},
    ]
    with pytest.raises(UnbalancedJournalEntryError):
        JournalEntry.validate_balance(lines, raise_on_error=True)


@pytest.mark.unit
def test_balance_within_tolerance():
    lines = [
        {'debit': Decimal('1000.0000'), 'credit': Decimal('0.0000')},
        {'debit': Decimal('0.0000'),    'credit': Decimal('1000.0001')},
    ]
    assert JournalEntry.validate_balance(lines) is True


@pytest.mark.unit
def test_unbalanced_entry_returns_false_without_raising():
    lines = [
        {'debit': Decimal('500.00'), 'credit': Decimal('0.00')},
        {'debit': Decimal('0.00'),   'credit': Decimal('400.00')},
    ]
    assert JournalEntry.validate_balance(lines) is False