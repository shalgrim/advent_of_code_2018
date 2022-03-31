from unittest import TestCase, skip

from day23_1 import Nanobot, num_nanobots_within_range_of_strongest
from day23_2 import (
    distance_to_position_in_range_of_most_nanobots,
    main_octree,
    position_in_range_of_most_nanobots,
)
from day23_2_dfs import seeded_dfs_main


class TestDay23(TestCase):
    def test_num_nanobots_within_range_of_strongest_1(self):
        self.assertEqual(num_nanobots_within_range_of_strongest('data/test23.txt'), 7)

    def test_num_nanobots_within_range_of_strongest_2(self):
        self.assertEqual(
            num_nanobots_within_range_of_strongest('data/input23.txt'), 943
        )

    def test_common_points(self):
        n1 = Nanobot(0, 0, 0, 1)
        self.assertEqual(set([]), n1.common_points(Nanobot(1, 1, 0, 0)))
        self.assertEqual(
            set(
                [
                    (0, 0, 0),
                    (0, 0, 1),
                    (0, 0, -1),
                    (0, 1, 0),
                    (0, -1, 0),
                    (1, 0, 0),
                    (-1, 0, 0),
                ]
            ),
            n1.common_points(Nanobot(0, 0, 0, 5)),
        )

    @skip  # good test but takes 22s
    def test_position_in_range_of_most_nanobots(self):
        self.assertEqual(
            position_in_range_of_most_nanobots('data/test23_2.txt'), (12, 12, 12)
        )

    @skip  # good test but takes 22s
    def test_distance_to_position_in_range_of_most_nanobots(self):
        self.assertEqual(
            distance_to_position_in_range_of_most_nanobots('data/test23_2.txt'), 36
        )

    def test_main_octree(self):
        x, y, z, overlaps = main_octree('data/test23_2.txt')
        self.assertEqual(abs(x) + abs(y) + abs(z), 36)

    def test_dfs(self):
        (x, y, z), overlaps = seeded_dfs_main('data/test23_2.txt', 4)
        self.assertEqual(abs(x)+abs(y)+abs(z), 36)
        (x, y, z), overlaps = seeded_dfs_main('data/test23_2.txt', 5)
        self.assertEqual(abs(x)+abs(y)+abs(z), 36)

    def test_dfs_long(self):  # takes like ten seconds
        (x, y, z), overlaps = seeded_dfs_main('data/test23_2.txt')
        self.assertEqual(abs(x)+abs(y)+abs(z), 36)
