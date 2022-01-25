import itertools
import re

from tqdm import tqdm

LINE_PATT = re.compile(r'^pos=<(.+,.+,.+)>, r=(\d+)\n$')


class Nanobot(object):
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

    def contains(self, x, y, z):
        """True if x, y, z falls within this nanobot's range"""
        return abs(self.x - x) + abs(self.y - y) + abs(self.z - z) <= self.radius

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def midpoints(self, other):
        xs = self._midpoint_calculator(self.x, other.x)
        ys = self._midpoint_calculator(self.y, other.y)
        zs = self._midpoint_calculator(self.z, other.z)

        return itertools.product(xs, ys, zs)

    def intersect(self, other):
        """True if this nanobot has any points in common with other"""
        return any(self.contains(*point) and other.contains(*point) for point in self.midpoints(other))

    def common_points(self, other):
        """Returns points self and other share in common"""
        if not self.intersect(other):
            return set()
        points_to_explore = []
        for midpoint in self.midpoints(other):
            if self.contains(*midpoint) and other.contains(*midpoint):
                points_to_explore.append(midpoint)

        contained_points = set(points_to_explore)
        points_to_explore = set(points_to_explore)
        explored_points = set()
        while points_to_explore:
            print(f'{len(points_to_explore)=}')
            explore_point = points_to_explore.pop()
            explored_points.add(explore_point)
            left = explore_point[0] - 1, explore_point[1], explore_point[2]
            right = explore_point[0] + 1, explore_point[1], explore_point[2]
            up = explore_point[0], explore_point[1] - 1, explore_point[2]
            down = explore_point[0], explore_point[1] + 1, explore_point[2]
            inn = explore_point[0], explore_point[1], explore_point[2] - 1
            out = explore_point[0], explore_point[1], explore_point[2] + 1

            for point in [left, right, up, down, inn, out]:
                if point in points_to_explore.union(explored_points):
                    continue
                if self.contains(*point) and self.contains(*point):
                    contained_points.add(point)
                    points_to_explore.add(point)

        return contained_points

    def _midpoint_calculator(self, val1, val2):
        lower = min([val1, val2])
        higher = max([val1, val2])
        distance = higher - lower
        if distance % 2 == 0:
            return [lower + distance//2]
        else:
            return [lower + distance // 2, lower + distance // 2 + 1]

    def produce_reachable_points(self):
        reachables = set()
        for i in range(self.radius+1):
            reachables.update(self._produce_reachables(i))
        return reachables

    def _produce_reachables(self, distance):
        reachables = set()
        # for z_delta in tqdm(range(-distance, distance+1)):
        for z_delta in range(-distance, distance + 1):
            z = self.z + z_delta
            first_remainder = distance - abs(z_delta)
            for y_delta in range(-first_remainder, first_remainder+1):
                y = self.y + y_delta
                x_delta = first_remainder - abs(y_delta)
                reachables.add((self.x - x_delta, y, z))
                reachables.add((self.x + x_delta, y, z))
        return reachables


def parse_input23(filename):
    with open(filename) as f:
        lines = f.readlines()

    nanobots = []
    for line in lines:
        match = LINE_PATT.match(line)
        x, y, z = [int(s) for s in match.groups()[0].split(',')]
        radius = int(match.groups()[1])
        nanobots.append(Nanobot(x, y, z, radius))

    return nanobots


def nanobots_within_range(nanobot, nanobots):
    answer = sum(1 for n in nanobots if nanobot.manhattan_distance(n) <= nanobot.radius)
    return answer


def num_nanobots_within_range_of_strongest(filename):
    nanobots = parse_input23(filename)
    strongest_nanobot = sorted(nanobots, key=lambda x: x.radius, reverse=True)[0]
    return nanobots_within_range(strongest_nanobot, nanobots)


if __name__ == '__main__':
    print(f'answer: {num_nanobots_within_range_of_strongest("data/input23.txt")}')
