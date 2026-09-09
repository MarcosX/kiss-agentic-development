import pytest

from app import apply_discount


def test_discount_removes_percent_of_total():
    assert apply_discount(100, 10) == 90


def test_discount_rejects_non_numeric_total():
    with pytest.raises(ValueError):
        apply_discount("100", 10)