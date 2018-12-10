import re

# LINE_PATT = re.compile(
#     r'^position=<\s*(?P<posx>\s*-?\d+),\s*(?P<posy>-?\d+)\s*velocity<?P<velx>\s*-?\d+,\s+(?P<vely>-?\d+)>\s*\n$'
# )
#
# LINE_PATT = re.compile(r'^position=<\s*(?P<posx>-?\d+),\s*(?P<posy>-?\d+)>\s*velocity=<\s*(?P<velx>-?\d+).*\n$')
LINE_PATT = re.compile(
    r'^position=<\s*(?P<posx>-?\d+),\s*(?P<posy>-?\d+)>\s*velocity=<\s*(?P<velx>-?\d+),'
    r'\s*(?P<vely>-?\d+)>\n$'
)


class Point(object):
    def __init__(self, x, y, velx, vely):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely

    def tick(self):
        self.x += self.velx
        self.y += self.vely


class Canvas(object):
    def __init__(self, points):
        self.points = points

    def tick(self):
        for point in self.points:
            point.tick()

    def _row_string(self, row, min_x, max_x):
        covered = {p.x for p in self.points if p.y == row}
        row_string = ''
        for i in range(min_x - 2, max_x + 1 + 2):
            if i in covered:
                row_string += '#'
            else:
                row_string += '.'
        return row_string + '\n'

    def print(self):
        min_x = min(p.x for p in self.points)
        max_x = max(p.x for p in self.points)
        min_y = min(p.y for p in self.points)
        max_y = max(p.y for p in self.points)

        if max_x - min_x > 100 or max_y - min_y > 100:
            return False

        for i in range(min_y-2, max_y + 2+ 1):
            print(self._row_string(i, min_x, max_x))

        return True


def parse_line(line):
    match = LINE_PATT.match(line)
    return Point(
        int(match.group('posx')),
        int(match.group('posy')),
        int(match.group('velx')),
        int(match.group('vely')),
    )


def main(lines):
    points = [parse_line(line) for line in lines]
    canvas = Canvas(points)
    i = 0

    while True:
        if canvas.print():
            print(f'num seconds: {i}')
            print('\n\n\n')
            input('continue?\n')

        # print('pre tick')
        canvas.tick()
        i += 1
        # print('post tick')


if __name__ == '__main__':
    with open('data/input10.txt') as f:
    # with open('data/test10.txt') as f:
        lines = f.readlines()

    main(lines)
