from unittest import TestCase

from day13_1 import parse_input
from day13_2 import locate_last_cart


class TestLocate_last_cart(TestCase):
    def setUp(self):
        self.game = parse_input('data/test13_3.txt')

    def test_locate_last_cart(self):
        self.assertEqual(locate_last_cart(self.game), (6, 4))
