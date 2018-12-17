from unittest import TestCase

from day17_1 import calc_wettable_squares_from_file, parse_coordinates


class TestDay17(TestCase):
    def test_calc_wettable_squares_from_file(self):
        self.assertEqual(calc_wettable_squares_from_file('data/test17.txt'), 57)

    def test_parse_coordinates(self):
        self.assertEqual(
            parse_coordinates(['x=495', 'y=2..7'], False),
            [(495, 2), (495, 3), (495, 4), (495, 5), (495, 6), (495, 7)],
        )

        self.assertEqual(
            parse_coordinates(['y=7', 'x=495..501'], True),
            [(495, 7), (496, 7), (497, 7), (498, 7), (499, 7), (500, 7), (501, 7)],
        )
