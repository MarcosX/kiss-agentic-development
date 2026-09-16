from products import total_price


def test_total_price():
    assert total_price([{"price": 10}, {"price": 32}]) == 42