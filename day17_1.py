import logging
import sys
from itertools import product
from logging import StreamHandler

from ground import Ground
from water import Water

logger = logging.getLogger('avent_of_code.2018.day17_1')
logging.basicConfig(
    filename='day17_1.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


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
    wx = ground.well_coordinate[0]
    wy = ground.well_coordinate[1] + 1
    water = Water(wx, wy, ground, None)
    squares_to_check = [(wx, wy)]

    while squares_to_check:
        # print(f'{len(squares_to_check)} squares to check')
        new_squares_to_check = ground.check_square(squares_to_check.pop())
        squares_to_check.extend(new_squares_to_check)

    # water.flow()
    return ground.wet_squares


if __name__ == '__main__':
    print(f'answer: {calc_wettable_squares_from_file("data/input17.txt")}')
    # print(f'answer: {calc_wettable_squares_from_file("data/test17.txt")}')
