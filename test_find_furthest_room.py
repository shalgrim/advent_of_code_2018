from unittest import TestCase

from day20_1 import find_furthest_room


class TestFind_furthest_room(TestCase):
    def test_find_furthest_room_1(self):
        self.assertEqual(find_furthest_room('^WNE$'), 3)

    def test_find_furthest_room_2(self):
        self.assertEqual(find_furthest_room('^ENWWW(NEEE|SSE(EE|N))$'), 10)

    def test_find_furthest_room_3(self):
        self.assertEqual(
            find_furthest_room('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'), 18
        )

    def test_find_furthest_room_4(self):
        self.assertEqual(find_furthest_room('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'), 23)

    def test_find_furthest_room_5(self):
        self.assertEqual(find_furthest_room('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'), 31)
