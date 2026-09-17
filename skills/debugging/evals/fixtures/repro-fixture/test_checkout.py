import pytest

from checkout import Cart


def test_total_applies_discount_before_tax():
    cart = Cart()
    cart.add_item("widget", 100, 1)
    assert cart.total(discount=0.2) == 88.0


@pytest.mark.parametrize(
    "prices,qty,total",
    [
        ([100], 1, 110.0),
        ([10, 20, 5], 1, 38.5),
        ([10], 3, 33.0),
    ],
)
def test_total_without_discount(prices, qty, total):
    cart = Cart()
    for p in prices:
        cart.add_item("item", p, qty)
    assert cart.total() == total


def test_receipt_line_count():
    cart = Cart()
    cart.add_item("a", 1)
    cart.add_item("b", 2)
    cart.add_item("c", 3)
    assert len(cart._items) == 3