import logging
import sys
from itertools import product
from logging import StreamHandler

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

    def __str__(self):
        min_x = min(coord[0] for coord in self.clay_coordinates) - 1
        max_x = max(coord[0] for coord in self.clay_coordinates) + 1
        max_y = max(coord[1] for coord in self.clay_coordinates)
        min_y = 0

        # build headers
        lines = [
            '   {}'.format(''.join([str(x // 100) for x in range(min_x, max_x + 1)])),
            '   {}'.format(
                ''.join([str(x // 10 % 10) for x in range(min_x, max_x + 1)])
            ),
            '   {}'.format(''.join([str(x % 10) for x in range(min_x, max_x + 1)])),
        ]

        # build ground level
        line = ' 0 '
        for x in range(min_x, max_x + 1):
            if (x, 0) == self.well_coordinate:
                line += '+'
            elif (x, 0) in self.clay_coordinates:
                line += '#'
            else:
                line += '.'
        lines.append(line)

        # build ground slice
        for y in range(1, max_y + 1):
            lines.append(
                '{:>2} {}'.format(
                    y,
                    ''.join(
                        [
                            '#' if (x, y) in self.clay_coordinates else '.'
                            for x in range(min_x, max_x + 1)
                        ]
                    ),
                )
            )

        return '\n'.join(lines)


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
    print(ground)
    answer = 0
    return answer


if __name__ == '__main__':
    print(f'answer: {calc_wettable_squares_from_file("data/test17.txt")}')
