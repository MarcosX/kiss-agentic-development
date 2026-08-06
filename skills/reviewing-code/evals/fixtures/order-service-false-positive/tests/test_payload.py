import unittest

from parser import parse_payload
from producer import build_payload


class PayloadTest(unittest.TestCase):
    def test_producer_rejects_unknown_event(self):
        with self.assertRaises(ValueError):
            build_payload({"type": "hack", "data": {}})

    def test_producer_rejects_non_object_data(self):
        with self.assertRaises(ValueError):
            build_payload({"type": "click", "data": "nope"})

    def test_parse_payload_parses_valid(self):
        self.assertEqual(parse_payload('{"type": "click"}'), {"type": "click"})


if __name__ == "__main__":
    unittest.main()
