from unittest import TestCase
from day13_1 import main


class TestMain(TestCase):
    def test_main_1(self):
        self.assertEqual(main('data/test13_1.txt'), (0, 3))

    def test_main_2(self):
        self.assertEqual(main('data/test13_2.txt'), (7, 3))
