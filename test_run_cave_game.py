from unittest import TestCase

from day15_1 import parse_cave_input, run_cave_game


class TestRun_cave_game(TestCase):
    def setUp(self):
        self.cave = parse_cave_input('data/test15.txt')

    def test_run_cave_game(self):
        self.assertEqual(run_cave_game(self.cave), 18740)
