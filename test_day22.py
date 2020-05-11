from unittest import TestCase, skip

from day22_1 import (
    CAVE_DEPTH,
    TARGET_X,
    TARGET_Y,
    Equipment,
    build_cave,
    calc_risk_level,
)
from day22_2 import PathFinder, State
from day22_2_2 import PathFinderBFS

TEST_TARGET_X = 10
TEST_TARGET_Y = 10
TEST_CAVE_DEPTH = 510


class TestDay22BFS(TestCase):
    def setUp(self):
        self.actual_cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
        self.test_cave = build_cave(TEST_TARGET_X, TEST_TARGET_Y, TEST_CAVE_DEPTH)

    def test_part_two_base_case_00(self):
        pf = PathFinderBFS(
            self.test_cave, TEST_TARGET_X, TEST_TARGET_Y, initial_x=10, initial_y=10
        )
        self.assertEqual(pf.find_quickest_path(), 0)

    def test_part_two_base_case_00_plus_switch(self):
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=10,
            initial_y=10,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 7)

    def test_part_two_base_case_01(self):
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=10,
            initial_y=11,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 8)

    def test_part_two_base_case_02(self):
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=10,
            initial_y=12,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 9)

    def test_part_two_base_case_03(self):
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=9,
            initial_y=12,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 10)

    def test_part_two_base_case_04(self):
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=8,
            initial_y=12,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 11)

    def test_part_two_base_case_06(self):
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=6,
            initial_y=12,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 13)

class TestDay22(TestCase):
    def setUp(self):
        self.actual_cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
        self.test_cave = build_cave(TEST_TARGET_X, TEST_TARGET_Y, TEST_CAVE_DEPTH)

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

    def test_base_case_minus_01(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(10, 11), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 8)

    def test_base_case_minus_02(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(10, 12), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 9)

    def test_base_case_minus_03(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(9, 12), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 10)

    def test_base_case_minus_04(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(8, 12), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 11)

    def test_base_case_minus_06(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(6, 12), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 13)

    def test_base_case_minus_07(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(6, 11), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 14)

    def test_base_case_minus_08(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(5, 11), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 15)

    def test_base_case_minus_09(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(4, 11), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 16)

    def test_base_case_minus_10(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        state = State(position=(4, 10), equipment=Equipment.CLIMB, visited=[], cost=0)
        pf.find_quickest_path(state)
        self.assertEqual(pf.known_shortest_path, 17)

    # @skip("not ready")
    def test_part_two(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        pf.find_quickest_path()
        self.assertEqual(pf.known_shortest_path, 45)
        # pf = PathFinder(self.actual_cave)
        # self.assertEqual(pf.find_quickest_path(TARGET_X, TARGET_Y), 0)  # don't have this answer yet
