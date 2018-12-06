import logging
import sys
from logging import StreamHandler

from day06_1 import INPUT_PATTERN, Point

logger = logging.getLogger('advent_of_code.2018.day06_2')
logging.basicConfig(filename='day06_2.log',
                    level=logging.INFO,
                    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
logger.addHandler(StreamHandler(sys.stdout))

# SAFE_ZONE = 32
SAFE_ZONE = 10000


def main(lines):
    coordinates = [
        Point(*[int(g) for g in INPUT_PATTERN.match(line).groups()]) for line in lines
    ]
    max_x = max(c.x for c in coordinates)
    max_y = max(c.y for c in coordinates)
    in_region = set()
    for j in range(max_x + 1):
        for k in range(max_y + 1):
            point = Point(j, k)
            total_distance = sum(point.manhattan_distance(c) for c in coordinates)
            if total_distance < SAFE_ZONE:
                in_region.add(point)
    print(f'I found {len(in_region)} points in the region')
    

if __name__ == '__main__':
    # with open('data/test06.txt') as f:
    with open('data/input06.txt') as f:
        lines = f.readlines()

    main(lines)
