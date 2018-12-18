from unittest import TestCase

from day18_1 import calc_resource_value


class TestCalc_resource_value(TestCase):
    def test_calc_resource_value(self):
        self.assertEqual(calc_resource_value('data/test18.txt', 10), 1147)
