from unittest import TestCase

from day22_1 import calc_risk_level


class TestCalc_risk_level(TestCase):
    def test_calc_risk_level(self):
        self.assertEqual(calc_risk_level(10, 10, 510), 141)
