from unittest import TestCase
from day09_1 import play_marble_game


class TestPlay_marble_game(TestCase):
    def test_play_marble_game(self):
        winning_score = play_marble_game(9, 25)
        self.assertEqual(winning_score, 32)

    def test_play_marble_game_2(self):
        winning_score = play_marble_game(10, 1618)
        self.assertEqual(winning_score, 8317)

    def test_play_marble_game_3(self):
        winning_score = play_marble_game(13, 7999)
        self.assertEqual(winning_score, 146373)

    def test_play_marble_game_4(self):
        winning_score = play_marble_game(17, 1104)
        self.assertEqual(winning_score, 2764)

    def test_play_marble_game_5(self):
        winning_score = play_marble_game(21, 6111)
        self.assertEqual(winning_score, 54718)

    def test_play_marble_game_6(self):
        winning_score = play_marble_game(30, 5807)
        self.assertEqual(winning_score, 37305)
