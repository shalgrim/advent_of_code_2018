from unittest import TestCase

from day23_1 import num_nanobots_within_range_of_strongest
from day23_2 import position_in_range_of_most_nanobots, distance_to_position_in_range_of_most_nanobots, main_octree


class TestDay23(TestCase):
    def test_num_nanobots_within_range_of_strongest_1(self):
        self.assertEqual(num_nanobots_within_range_of_strongest('data/test23.txt'), 7)

    def test_num_nanobots_within_range_of_strongest_2(self):
        self.assertEqual(
            num_nanobots_within_range_of_strongest('data/input23.txt'), 943
        )

    def test_position_in_range_of_most_nanobots(self):
        self.assertEqual(position_in_range_of_most_nanobots('data/test23_2.txt'), (12, 12, 12))

    def test_distance_to_position_in_range_of_most_nanobots(self):
        self.assertEqual(distance_to_position_in_range_of_most_nanobots('data/test23_2.txt'), 36)

    def test_main_octree(self):
        self.assertEqual(main_octree('data/test23_2.txt'), 36)
