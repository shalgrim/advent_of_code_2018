from unittest import TestCase

from day23_1 import num_nanobots_within_range_of_strongest


class TestNum_nanobots_within_range_of_strongest(TestCase):
    def test_num_nanobots_within_range_of_strongest(self):
        self.assertEqual(num_nanobots_within_range_of_strongest('data/test23.txt'), 7)
