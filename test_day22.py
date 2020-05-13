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

    def test_part_two_base_case_07(self):
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=6,
            initial_y=11,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 14)

    def test_part_two_base_case_08(self):
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=5,
            initial_y=11,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 15)

    def test_part_two_base_case_09(self):
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=5,
            initial_y=10,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 16)

    def test_part_two_base_case_11(self):  # 49s counting ticks vs 2s with culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=5,
            initial_y=8,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 18)

    def test_part_two_base_case_12(self):  # 1m 47s vs 1m 27s counting ticks vs 3s with culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=4,
            initial_y=8,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 19)

    def test_part_two_base_case_13(self):  # 2m 27s vs 2m 8s counting ticks vs 4s with culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=4,
            initial_y=7,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 20)

    def test_part_two_base_case_14(self):  # 3m 22s vs 5s culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=4,
            initial_y=6,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 21)

    def test_part_two_base_case_15(self):
        # 8m 9s vs 9s culling here we go with the jumps...I wonder what happens at this case?
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=4,
            initial_y=5,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 22)

    def test_part_two_base_case_16(self):  # 17m 26s...quite the big jump vs 18s with culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=4,
            initial_y=4,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 23)

    def test_part_two_base_case_19(self):  # takes over 20 minutes in exhaustive BFS? ... 60s with culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=4,
            initial_y=1,
            initial_equip=Equipment.CLIMB,
        )
        self.assertEqual(pf.find_quickest_path(), 26)

    def test_part_two_base_case_19_plus_switch(self):  # 1m 49s culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=4,
            initial_y=1,
            initial_equip=Equipment.NO,
        )
        self.assertEqual(pf.find_quickest_path(), 33)

    def test_part_two_base_case_20(self):  # 2m 47s with culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=3,
            initial_y=1,
            initial_equip=Equipment.NO,
        )
        self.assertEqual(pf.find_quickest_path(), 34)

    def test_part_two_base_case_22(self):  # 6m 30s with culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=1,
            initial_y=1,
            initial_equip=Equipment.NO,
        )
        self.assertEqual(pf.find_quickest_path(), 36)

    def test_part_two_base_case_22_plus_switch(self):  # 7m 15s with culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=1,
            initial_y=1,
            initial_equip=Equipment.TORCH,
        )
        self.assertEqual(pf.find_quickest_path(), 43)

    def test_part_two_base_case_23(self):  # 9m 3s with culling (one more tick added almost two minutes :sadface:)
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=0,
            initial_y=1,
            initial_equip=Equipment.TORCH,
        )
        self.assertEqual(pf.find_quickest_path(), 44)

    def test_part_two_final(self):  # 10m 8s with culling
        pf = PathFinderBFS(
            self.test_cave,
            TEST_TARGET_X,
            TEST_TARGET_Y,
            initial_x=0,
            initial_y=0,
            initial_equip=Equipment.TORCH,
        )
        self.assertEqual(pf.find_quickest_path(), 45)


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

    # @skip("not ready")
    def test_part_two(self):
        pf = PathFinder(self.test_cave, TEST_TARGET_X, TEST_TARGET_Y)
        pf.find_quickest_path()
        self.assertEqual(pf.known_shortest_path, 45)
        # pf = PathFinder(self.actual_cave)
        # self.assertEqual(pf.find_quickest_path(TARGET_X, TARGET_Y), 0)  # don't have this answer yet
