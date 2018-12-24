from day23_1 import parse_input23


def find_position_for_transport(nanobots):
    return 0, 0, 0


def position_in_range_of_most_nanobots(filename):
    nanobots = parse_input23(filename)
    find_position_for_transport(nanobots)
    pass


if __name__ == '__main__':
    print(f'answer: {position_in_range_of_most_nanobots("data/input23.txt")}')