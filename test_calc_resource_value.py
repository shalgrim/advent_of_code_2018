from unittest import TestCase

from day18_1 import calc_resource_value


class TestCalc_resource_value(TestCase):
    def test_calc_resource_value_test(self):
        self.assertEqual(
            calc_resource_value('data/test18.txt', 10, show_maps=False), 1147
        )

    def test_calc_resource_value_input(self):
        self.assertEqual(
            calc_resource_value('data/input18.txt', 10, show_maps=False), 560091
        )
