from unittest import TestCase

import day19_1


class TestDay19(TestCase):
    def test_main_day19_1(self):
        self.assertEqual(day19_1.main('data/test19.txt'), 0)
