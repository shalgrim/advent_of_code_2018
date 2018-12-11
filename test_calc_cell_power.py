from unittest import TestCase
from day11_1 import calc_cell_power


class TestCalc_cell_power(TestCase):
    def test_calc_cell_power_1(self):
        self.assertEqual(calc_cell_power(3, 5, 8), 4)

    def test_calc_cell_power_2(self):
        self.assertEqual(calc_cell_power(122, 79, 57), -5)

    def test_calc_cell_power_3(self):
        self.assertEqual(calc_cell_power(217, 196, 39), 0)

    def test_calc_cell_power_4(self):
        self.assertEqual(calc_cell_power(101, 153, 71), 4)
