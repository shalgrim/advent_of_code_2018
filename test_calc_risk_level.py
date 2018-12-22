from unittest import TestCase

from day22_1 import calc_risk_level, build_cave


class TestCalc_risk_level(TestCase):
    def test_calc_risk_level(self):
        cave = build_cave(10, 10, 510)
        self.assertEqual(calc_risk_level(10, 10, cave), 114)
