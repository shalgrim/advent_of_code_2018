import logging
import sys
from collections import Counter
from logging import StreamHandler

from day23_1 import parse_input23

logger = logging.getLogger('advent_of_code.2018.day23_2')
logging.basicConfig(
    filename='day23_2.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def find_position_for_transport(nanobots):
    point_reachability = Counter()

    for i, n in enumerate(nanobots):
        logger.info(f'producing points for nanobot {i+1} with radius {n.radius}')
        for point in n.produce_reachable_points():
            point_reachability[point] += 1

    most_common = point_reachability.most_common()
    most_reachable_point_distance = most_common[0][1]
    most_reachable_points = [
        mc[0] for mc in most_common if mc[1] == most_reachable_point_distance
    ]

    closest_to_me = sorted(
        most_reachable_points, key=lambda x: manhattan_distance(x, (0, 0, 0))
    )[0]
    return closest_to_me


def position_in_range_of_most_nanobots(filename):
    nanobots = parse_input23(filename)
    return find_position_for_transport(nanobots)


def distance_to_position_in_range_of_most_nanobots(filename):
    position = position_in_range_of_most_nanobots(filename)
    answer = manhattan_distance(position, (0, 0, 0))
    return answer


if __name__ == '__main__':
    print(f'answer: {position_in_range_of_most_nanobots("data/input23.txt")}')
