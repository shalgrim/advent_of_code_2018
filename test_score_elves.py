from unittest import TestCase

from day14_1 import score_elves


class TestScore_elves(TestCase):
    def test_score_elves_5(self):
        self.assertEqual(score_elves(5), 124515891)

    def test_score_elves_9(self):
        self.assertEqual(score_elves(9), 5158916779)

    def test_score_elves_18(self):
        self.assertEqual(score_elves(18), 9251071085)

    def test_score_elves_2018(self):
        self.assertEqual(score_elves(2018), 5941429882)
