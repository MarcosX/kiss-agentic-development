from utils import format_price


def test_format_price():
    assert format_price(1234.5) == "$1234.50"