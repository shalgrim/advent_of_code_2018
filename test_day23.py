from unittest import TestCase, skip

from day23_1 import num_nanobots_within_range_of_strongest, Nanobot
from day23_2 import (
    position_in_range_of_most_nanobots,
    distance_to_position_in_range_of_most_nanobots,
)


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
