from unittest import TestCase

from day15_1 import parse_cave_input, run_cave_game


class TestRun_cave_game(TestCase):

    def test_run_cave_game_1(self):
        cave = parse_cave_input('data/test15_1.txt')
        self.assertEqual(run_cave_game(cave), 27730)

    def test_run_cave_game_2(self):
        cave = parse_cave_input('data/test15_2.txt')
        self.assertEqual(run_cave_game(cave), 27730)

    def test_run_cave_game_3(self):
        cave = parse_cave_input('data/test15_3.txt')
        self.assertEqual(run_cave_game(cave), 27730)

    def test_run_cave_game_4(self):
        cave = parse_cave_input('data/test15_4.txt')
        self.assertEqual(run_cave_game(cave), 27730)

    def test_run_cave_game_5(self):
        cave = parse_cave_input('data/test15_5.txt')
        self.assertEqual(run_cave_game(cave), 27730)

    def test_run_cave_game_6(self):
        cave = parse_cave_input('data/test15_6.txt')
        self.assertEqual(run_cave_game(cave), 27730)

    def test_monster_move(self):
        my_cave = parse_cave_input('data/test15_move.txt')
        elf = my_cave.elves[0]
        self.assertEqual(elf.location, (1, 1))
        my_cave.tick()
        self.assertEqual(elf.location, (2, 1))
