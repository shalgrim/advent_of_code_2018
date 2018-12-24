import re

from tqdm import tqdm

LINE_PATT = re.compile(r'^pos=<(.+,.+,.+)>, r=(\d+)\n$')


class Nanobot(object):
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def produce_reachable_points(self):
        reachables = set()
        for i in range(self.radius+1):
            reachables.update(self._produce_reachables(i))
        return reachables

    def _produce_reachables(self, distance):
        reachables = set()
        for z_delta in tqdm(range(-distance, distance+1)):
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
