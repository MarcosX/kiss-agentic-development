from app import format_currency


def test_currency_formatting_unchanged():
    assert format_currency(1234.5) == "$1234.50"