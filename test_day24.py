from unittest import TestCase

from day24_1 import day24_1


class TestDay24(TestCase):
    def test_day24_1(self):
        self.assertEqual(day24_1('data/test24.txt'), 5216)
