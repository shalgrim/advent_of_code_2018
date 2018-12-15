from enum import unique, Enum

CRASHED = 'CRASHED'
TRACK_NORTH_SOUTH = '|'
TRACK_EAST_WEST = '-'
TRACK_SLASH = '/'
TRACK_BACKSLASH = '\\'
TRACK_INTERSECTION = '+'
CART_WEST = '<'
CART_EAST = '>'
CART_NORTH = '^'
CART_SOUTH = 'v'

TRACK_CHARS = ''.join(
    [
        TRACK_NORTH_SOUTH,
        TRACK_EAST_WEST,
        TRACK_SLASH,
        TRACK_BACKSLASH,
        TRACK_INTERSECTION,
    ]
)
TURN_CHARS = ''.join([TRACK_SLASH, TRACK_BACKSLASH, TRACK_INTERSECTION])
CART_CHARS = ''.join([CART_NORTH, CART_SOUTH, CART_EAST, CART_WEST])


@unique
class TurnType(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2


class Game(object):
    def __init__(self, tracks, carts):
        self.tracks = tracks
        self.carts = carts
        self.crashes = []

    def __str__(self):
        max_y = max(max(c.y for c in self.carts), max(t[1] for t in self.tracks))
        max_x = max(max(c.x for c in self.carts), max(t[0] for t in self.tracks))

        lines = []
        for y in range(max_y + 1):
            line_chars = []
            for x in range(max_x + 1):
                if (x, y) in self.crashes:
                    line_chars.append('X')
                else:
                    carts_here = [c for c in self.carts if c.x == x and c.y == y]
                    if carts_here:
                        line_chars.append(carts_here[0].direction)
                    elif (x, y) in self.tracks:
                        line_chars.append(self.tracks[x, y].track_type)
                    else:
                        line_chars.append(' ')
            lines.append(''.join(line_chars))
        return '\n'.join(lines) + '\n\n\n'

    def tick(self, remove_crashed_carts=False):
        if remove_crashed_carts:
            carts_to_move = [
                cart
                for cart in sorted(self.carts, key=lambda z: (z.y, z.x))
                if cart.active
            ]
        else:
            carts_to_move = sorted(self.carts, key=lambda z: (z.y, z.x))

        for cart in carts_to_move:
            if cart.move(self.tracks, self.carts) == CRASHED:
                self.crashes.append((cart.x, cart.y))
                for other_cart in self.carts:
                    if other_cart.x == cart.x and other_cart.y == cart.y:
                        other_cart.active = False


class Track(object):
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.track_type = char


class Cart(object):
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.direction = char
        self.intersection_turn = 0

    def move(self, tracks, carts):
        if self.direction == CART_NORTH:
            self.y -= 1
        elif self.direction == CART_SOUTH:
            self.y += 1
        elif self.direction == CART_EAST:
            self.x += 1
        elif self.direction == CART_WEST:
            self.x -= 1
        self._turn_if_necessary(tracks)
        return CRASHED if self.detect_crash(carts) else None

    def _turn_if_necessary(self, tracks):
        if tracks[(self.x, self.y)].track_type in TURN_CHARS:
            self._update_direction(tracks[(self.x, self.y)].track_type)

    def _update_direction(self, track_type):
        if track_type == TRACK_SLASH:
            if self.direction == CART_NORTH:
                self.direction = CART_EAST
            elif self.direction == CART_WEST:
                self.direction = CART_SOUTH
            elif self.direction == CART_EAST:
                self.direction = CART_NORTH
            elif self.direction == CART_SOUTH:
                self.direction = CART_WEST
        elif track_type == TRACK_BACKSLASH:
            if self.direction == CART_NORTH:
                self.direction = CART_WEST
            elif self.direction == CART_WEST:
                self.direction = CART_NORTH
            elif self.direction == CART_EAST:
                self.direction = CART_SOUTH
            elif self.direction == CART_SOUTH:
                self.direction = CART_EAST
        elif track_type == TRACK_INTERSECTION:
            self._intersection_turn()

    def detect_crash(self, carts):
        if any(c for c in carts if c is not self and c.x == self.x and c.y == self.y):
            return True
        return False

    def _intersection_turn(self):
        if self.intersection_turn == TurnType.LEFT.value:
            if self.direction == CART_NORTH:
                self.direction = CART_WEST
            elif self.direction == CART_WEST:
                self.direction = CART_SOUTH
            elif self.direction == CART_SOUTH:
                self.direction = CART_EAST
            else:
                self.direction = CART_NORTH
        elif self.intersection_turn == TurnType.RIGHT.value:
            if self.direction == CART_NORTH:
                self.direction = CART_EAST
            elif self.direction == CART_WEST:
                self.direction = CART_NORTH
            elif self.direction == CART_SOUTH:
                self.direction = CART_WEST
            else:
                self.direction = CART_SOUTH

        self.intersection_turn = (self.intersection_turn + 1) % 3


def parse_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    tracks = {}
    carts = []

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in TRACK_CHARS:
                tracks[(x, y)] = Track(x, y, char)
            elif char in CART_CHARS:
                carts.append(Cart(x, y, char))
                tracks[(x, y)] = Track(x, y, track_type_from_cart_char(char))

    return Game(tracks, carts)


def track_type_from_cart_char(cart_char):
    if cart_char in '<>':
        track_type = TRACK_EAST_WEST
    else:
        track_type = TRACK_NORTH_SOUTH
    return track_type


def get_first_crash_location(game):
    while not game.crashes:
        game.tick()

    print(game)

    return sorted(game.crashes)[0]


def main(filename):
    game = parse_input(filename)
    answer = get_first_crash_location(game)
    return answer


if __name__ == '__main__':
    answer = main('data/input13.txt')
    print(answer)
