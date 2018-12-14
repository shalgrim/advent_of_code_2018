from unittest import TestCase

from day14_2 import score_elves_backwards


class TestScore_elves_backwards(TestCase):
    def test_score_elves_5(self):
        self.assertEqual(score_elves_backwards('01245'), 5)

    def test_score_elves_9(self):
        self.assertEqual(score_elves_backwards('51589'), 9)

    def test_score_elves_18(self):
        self.assertEqual(score_elves_backwards('92510'), 18)

    def test_score_elves_2018(self):
        self.assertEqual(score_elves_backwards('59414'), 2018)
