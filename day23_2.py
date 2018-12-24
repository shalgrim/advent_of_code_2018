from collections import Counter

from day23_1 import parse_input23


def find_position_for_transport(nanobots):
    point_reachability = Counter()

    for n in nanobots:
        for point in n.produce_reachable_points():
            point_reachability[point] += 1

    return point_reachability.most_common()[0][0]


def position_in_range_of_most_nanobots(filename):
    nanobots = parse_input23(filename)
    return find_position_for_transport(nanobots)


if __name__ == '__main__':
    print(f'answer: {position_in_range_of_most_nanobots("data/input23.txt")}')
