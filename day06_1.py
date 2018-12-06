import logging
import math
import re
import sys
from collections import Counter, defaultdict
from logging import StreamHandler

logger = logging.getLogger('advent_of_code.2018.day06_1')
logging.basicConfig(
    filename='day06_1.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))

INPUT_PATTERN = re.compile(r'^(\d+), (\d+)\n$')


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return str(self)


def find_closest_coordinate(point, coordinates):
    closest_distance = math.inf
    closest_coordinate = None

    for c in coordinates:
        distance = point.manhattan_distance(c)

        if distance < closest_distance:
            closest_distance = distance
            closest_coordinate = c

            if closest_distance == 0:
                break

        elif distance == closest_distance:
            closest_coordinate = None  # a tie means no point claims it

    return closest_coordinate


def find_infinite_coordinate_indexes(coordinates):
    infinite_coordinates = find_infinite_coordinates(coordinates)
    infinite_coordinate_indexes = [coordinates.index(c) for c in infinite_coordinates]
    return infinite_coordinate_indexes


def find_infinite_coordinates(coordinates):
    max_x = max(c.x for c in coordinates)
    max_y = max(c.y for c in coordinates)
    infinite_coordinates = set()

    for i in range(max_x + 1):
        infinite_coordinates.add(find_closest_coordinate(Point(i, 0), coordinates))
        infinite_coordinates.add(find_closest_coordinate(Point(i, max_y), coordinates))

    for i in range(max_y + 1):
        infinite_coordinates.add(find_closest_coordinate(Point(0, i), coordinates))
        infinite_coordinates.add(find_closest_coordinate(Point(max_x, i), coordinates))

    return infinite_coordinates


def main(lines):
    coordinates = [
        Point(*[int(g) for g in INPUT_PATTERN.match(line).groups()]) for line in lines
    ]
    infinite_coordinates = [c for c in find_infinite_coordinates(coordinates) if c]
    logger.info(
        f'found {len(infinite_coordinates)} infinite coordinates out of {len(coordinates)} total'
    )

    area_tracker = Counter()
    max_x = max(c.x for c in coordinates)
    max_y = max(c.y for c in coordinates)

    for j in range(max_x + 1):
        for k in range(max_y + 1):
            logger.debug(f'({j}, {k})')
            area_tracker[
                str(find_closest_coordinate(Point(j, k), coordinates))
            ] += 1

    # results = sorted(area_tracker, key=lambda x: x[1], reverse=True)
    for ic in infinite_coordinates:
        del area_tracker[str(ic)]
    biggest = area_tracker.most_common(1)
    logger.info(f'{biggest[0][0]} has the largest area of {biggest[0][1]}')
    # 35,541 is too high
    # 5929 is too high


if __name__ == '__main__':
    # with open('data/test06.txt') as f:
    with open('data/input06.txt') as f:
        lines = f.readlines()

    main(lines)
