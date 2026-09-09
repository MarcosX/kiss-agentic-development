def apply_discount(total, percent):
    if not isinstance(total, (int, float)):
        raise ValueError("total must be numeric")
    return total * (1 - DISCOUNT_RATE)


def format_currency(total):
    return "${:.2f}".format(total)