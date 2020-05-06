import sys
from unittest import TestCase

from day22_1 import CAVE_DEPTH, TARGET_X, TARGET_Y, build_cave, calc_risk_level
from day22_2 import PathFinder


TEST_TARGET_X = 10
TEST_TARGET_Y = 10
TEST_CAVE_DEPTH = 510


class TestDay22(TestCase):
    def setUp(self):
        self.actual_cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
        self.test_cave = build_cave(TEST_TARGET_X, TEST_TARGET_Y, TEST_CAVE_DEPTH)

    def test_part_one(self):
        self.assertEqual(calc_risk_level(TEST_TARGET_X, TEST_TARGET_Y, self.test_cave), 114)
        self.assertEqual(calc_risk_level(TARGET_X, TARGET_Y, self.actual_cave), 9659)

    def test_part_two(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        pf.find_quickest_path()
        self.assertEqual(pf.known_shortest_path, 45)
        # pf = PathFinder(self.actual_cave)
        # self.assertEqual(pf.find_quickest_path(TARGET_X, TARGET_Y), 0)  # don't have this answer yet
