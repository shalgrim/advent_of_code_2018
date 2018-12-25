from unittest import TestCase

from day25_1 import day25_1


class TestDay25_1(TestCase):
    def test_day25_1(self):
        self.assertEqual(day25_1('data/test25_1.txt'), 2)

    def test_day25_2(self):
        self.assertEqual(day25_1('data/test25_2.txt'), 4)

    def test_day25_3(self):
        self.assertEqual(day25_1('data/test25_3.txt'), 3)

    def test_day25_4(self):
        self.assertEqual(day25_1('data/test25_4.txt'), 8)
