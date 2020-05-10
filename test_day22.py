from unittest import TestCase, skip

from day22_1 import CAVE_DEPTH, TARGET_X, TARGET_Y, build_cave, calc_risk_level
from day22_2 import Equipment, PathFinder, State

TEST_TARGET_X = 10
TEST_TARGET_Y = 10
TEST_CAVE_DEPTH = 510


class TestDay22(TestCase):
    def setUp(self):
        self.actual_cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
        self.test_cave = build_cave(TEST_TARGET_X, TEST_TARGET_Y, TEST_CAVE_DEPTH)

    @skip
    def test_part_one(self):
        self.assertEqual(
            calc_risk_level(TEST_TARGET_X, TEST_TARGET_Y, self.test_cave), 114
        )
        self.assertEqual(calc_risk_level(TARGET_X, TARGET_Y, self.actual_cave), 9659)

    def test_part_two_base_case(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(10, 10), equipment=Equipment.TORCH, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 0)

    def test_part_two_base_case_plus_switch(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(10, 10), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 7)

    def test_base_case_minus_1(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(10, 11), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 8)

    def test_base_case_minus_2(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(10, 12), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 9)

    def test_base_case_minus_3(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(9, 12), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 10)

    def test_base_case_minus_4(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(8, 12), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 11)

    def test_base_case_minus_6(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(6, 12), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 13)

    def test_base_case_minus_7(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(6, 11), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 14)

    def test_base_case_minus_8(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(5, 11), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 15)

    @skip("not ready")
    def test_part_two(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        pf.find_quickest_path()
        self.assertEqual(pf.known_shortest_path, 45)
        # pf = PathFinder(self.actual_cave)
        # self.assertEqual(pf.find_quickest_path(TARGET_X, TARGET_Y), 0)  # don't have this answer yet
