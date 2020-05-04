from unittest import TestCase

from day22_1 import CAVE_DEPTH, TARGET_X, TARGET_Y, build_cave, calc_risk_level


class TestDay22(TestCase):
    def setUp(self):
        self.cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)

    def test_part_one(self):
        self.assertEqual(calc_risk_level(TARGET_X, TARGET_Y, self.cave), 9659)
