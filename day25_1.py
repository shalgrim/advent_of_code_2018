def parse_input_25(filename):
    with open(filename) as f:
        lines = f.readlines()
    points = [tuple([int(i) for i in line.strip().split(',')]) for line in lines]
    return points


def manhattan_distance(cpoint, point):
    return (
        abs(cpoint[0] - point[0])
        + abs(cpoint[1] - point[1])
        + abs(cpoint[2] - point[2])
        + abs(cpoint[3] - point[3])
    )


def point_belongs_to_constellation(point, constellation):
    for cpoint in constellation:
        if manhattan_distance(cpoint, point) <= 3:
            return True
    return False


def create_constellation(unassigned_points):
    constellation = set()
    constellation.add(unassigned_points.pop())
    constellation_size = 0
    while len(constellation) > constellation_size:
        constellation_size = len(constellation)
        points_to_add = set()
        for point in unassigned_points:
            if point_belongs_to_constellation(point, constellation):
                points_to_add.add(point)

        constellation.update(points_to_add)
        unassigned_points = unassigned_points.difference(constellation)
    return constellation, unassigned_points


def group_into_constellations(points):
    unassigned_points = set(points)
    constellations = []
    while unassigned_points:
        constellation, unassigned_points = create_constellation(unassigned_points)
        constellations.append(constellation)
    return constellations


def day25_1(filename):
    points = parse_input_25(filename)
    constellations = group_into_constellations(points)
    return len(constellations)


if __name__ == '__main__':
    print(f'answer: {day25_1("data/input25.txt")}')
