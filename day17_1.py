import logging
import sys
from itertools import product
from logging import StreamHandler

from water import CLAY, FLOWING, SAND, STANDING, WELL, Water

logger = logging.getLogger('avent_of_code.2018.day17_1')
logging.basicConfig(
    filename='day17_1.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


class Ground(object):
    def __init__(self, clay_coordinates):
        self.clay_coordinates = clay_coordinates
        self.well_coordinate = (500, 0)
        self.flowing_coordinates = set()
        self.standing_coordinates = set()
        self.water = None

    def gimme_char(self, x, y):
        if (x, y) in self.standing_coordinates:
            return STANDING
        elif (x, y) in self.flowing_coordinates:
            return FLOWING
        elif (x, y) in self.clay_coordinates:
            return CLAY
        else:
            return SAND

    @property
    def max_y(self):
        return max(coord[1] for coord in self.clay_coordinates)

    def __str__(self):
        min_x = min(coord[0] for coord in self.clay_coordinates) - 1
        max_x = max(coord[0] for coord in self.clay_coordinates) + 1
        min_y = 0

        # build headers
        lines = [
            '     {}'.format(''.join([str(x // 100) for x in range(min_x, max_x + 1)])),
            '     {}'.format(
                ''.join([str(x // 10 % 10) for x in range(min_x, max_x + 1)])
            ),
            '     {}'.format(''.join([str(x % 10) for x in range(min_x, max_x + 1)])),
        ]

        # build ground level
        line = '   0 '
        for x in range(min_x, max_x + 1):
            if (x, 0) == self.well_coordinate:
                line += WELL
            elif (x, 0) in self.clay_coordinates:
                line += CLAY
            else:
                line += SAND
        lines.append(line)

        # build ground slice
        for y in range(1, self.max_y + 1):
            lines.append(
                '{:>4} {}'.format(
                    y, ''.join([self.gimme_char(x, y) for x in range(min_x, max_x + 1)])
                )
            )

        lines = [''] + lines + ['']

        return '\n'.join(lines)

    @property
    def wet_squares(self):
        return len(self.flowing_coordinates) + len(self.standing_coordinates)

    @property
    def flowing_squares(self):
        return len(self.flowing_coordinates)

    @property
    def standing_squares(self):
        return len(self.standing_coordinates)

    def tick(self):
        if self.water:
            self.water = self.water.flow(self)
        else:
            self.water = Water(self, None)
            self.water.x = self.well_coordinate[0]
            self.water.y = self.well_coordinate[1] + 1

        return True


def parse_coordinates(raw_coords, reverse):
    ranges = []
    for coord in raw_coords:
        coord_representation = coord.split('=')[1]
        if '..' in coord_representation:
            start, stop = [int(c) for c in coord_representation.split('..')]
        else:
            start = int(coord_representation)
            stop = int(coord_representation)
        ranges.append(range(start, stop + 1))

    ranges = ranges[::-1] if reverse else ranges
    return sorted(product(*ranges))


def create_ground_slice(filename):
    with open(filename) as f:
        lines = f.readlines()

    clay_coords = []

    for line in lines:
        raw_coords = line.strip().split(', ')
        clay_coords.extend(parse_coordinates(raw_coords, reverse=line[0] == 'y'))
        if line[0] == 'x':
            ordering = (0, 1)
        else:
            ordering = (1, 0)

    return Ground(clay_coords)


def calc_wettable_squares_from_file(filename):
    ground = create_ground_slice(filename)
    wet_squares = -1
    flowing_squares = -1
    standing_squares = -1
    water = Water(ground.well_coordinate[0], ground.well_coordinate[1], ground, None)
    water.flow()
    return ground.wet_squares


if __name__ == '__main__':
    print(f'answer: {calc_wettable_squares_from_file("data/input17.txt")}')
