from unittest import TestCase

from day21_alternate import calc_first_loop, calc_loops


class TestDay21Alternate(TestCase):
    def test_calc_first_loop(self):
        self.assertEqual(calc_first_loop(), 4_682_012)

    def test_calc_loops(self):
        self.assertEqual(calc_loops(1), 4_682_012)
