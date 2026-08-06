import unittest

from orders import apply_coupon


class CouponTest(unittest.TestCase):
    def test_valid_coupon_discounts(self):
        self.assertEqual(apply_coupon(100.0, "SUMMER10"), 90.0)

    def test_unknown_coupon_unchanged(self):
        self.assertEqual(apply_coupon(100.0, "NOPE"), 100.0)


if __name__ == "__main__":
    unittest.main()
