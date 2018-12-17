from unittest import TestCase

from day17_1 import calc_wettable_squares_from_file


class TestDay17(TestCase):
    def test_calc_wettable_squares_from_file(self):
        self.assertEqual(calc_wettable_squares_from_file('data/test17.txt'), 57)
