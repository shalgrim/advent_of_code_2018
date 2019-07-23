FLOWING = '|'
STANDING = '~'
WELL = '+'
CLAY = '#'
SAND = '.'


class Water(object):
    def __init__(self, x, y, ground, parent):
        self.ground = ground
        self.parent = parent
        self.x = x
        self.y = y
        if not parent:
            self.left = None
            self.right = None
            self.above = None
        elif parent.x == self.x - 1 and parent.y == self.y:
            self.left = parent
            self.right = None
            self.above = None
        elif parent.x == self.x + 1 and parent.y == self.y:
            self.right = parent
            self.left = None
            self.above = None
        elif parent.y == self.y - 1 and self.x == parent.x:
            self.above = parent
            self.left = None
            self.right = None
        self.below = None
        self.ground.flowing_coordinates.add((self.x, self.y))
        print(self.ground)

    def flow(self):
        below_result = self._flow_below()
        if below_result == FLOWING:
            return FLOWING
        elif below_result in (STANDING, CLAY):
            if self.left is not self.parent:
                left_result = self._flow_left()
            if self.right is not self.parent:
                right_result = self._flow_right()
                if self.left is not self.parent:
                    if left_result == right_result == CLAY:
                        self._stand()
                        return STANDING
                else:
                    return right_result
            else:
                return left_result

    def _flow_below(self):
        if self.y == self.ground.max_y:
            return FLOWING
        below_char = self.ground.gimme_char(self.x, self.y + 1)
        if below_char in (CLAY, STANDING):
            return below_char
        else:
            assert below_char == SAND, 'bad assumption about below char'
            self.below = Water(self.x, self.y + 1, self.ground, self)
            return self.below.flow()

    def _flow_left(self):
        left_char = self.ground.gimme_char(self.x - 1, self.y)
        if left_char == CLAY:
            return left_char
        elif left_char == STANDING:
            self._stand()
            return STANDING
        else:
            assert left_char == SAND, 'bad assumption about left char'
            self.left = Water(self.x - 1, self.y, self.ground, self)
            return self.left.flow()

    def _flow_right(self):
        right_char = self.ground.gimme_char(self.x + 1, self.y)
        if right_char == CLAY:
            return right_char
        elif right_char == STANDING:
            self._stand()
        else:
            assert right_char == SAND, 'bad assumption about right char'
            self.right = Water(self.x + 1, self.y, self.ground, self)
            return self.right.flow()

    def _stand(self):
        self.ground.standing_coordinates.add((self.x, self.y))
        self.ground.flowing_coordinates.remove((self.x, self.y))
        # print(self.ground)
        if self.left and self.left is not self.parent:
            self.left._stand()
        if self.right and self.right is not self.parent:
            self.right._stand()
