from coupons import COUPONS


def apply_coupon(total, code):
    code = code.strip().lower()
    rate = COUPONS.get(code)
    if rate is None:
        return total
    return total * (1 - rate)
