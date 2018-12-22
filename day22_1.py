from enum import Enum


class Type(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class Cave(object):
    def __init__(self, target_x, target_y, depth):
        self.target_x = target_x
        self.target_y = target_y
        self.depth = depth
        self.regions = {}

    def __getitem__(self, item):
        return self.regions[item]

    def __setitem__(self, key, value):
        self.regions[key] = value


class Region(object):
    def __init__(self, x, y, cave):
        self.x = x
        self.y = y
        self.cave = cave
        self.geologic_index = 0
        self.calc_geologic_index()
        self.erosion_level = 0
        self.calc_erosion_level()
        self.type = -1
        self.determine_type()

    def calc_geologic_index(self):
        if self.x == 0 and self.y == 0:
            self.geologic_index = 0
        elif self.x == self.cave.target_x and self.y == self.cave.target_y:
            self.geologic_index = 0
        elif self.y == 0:
            self.geologic_index = self.x * 16807
        elif self.x == 0:
            self.geologic_index = self.y * 48271
        else:
            self.geologic_index = (
                self.cave[(self.x - 1, self.y)].erosion_level
                * self.cave[(self.x, self.y - 1)].erosion_level
            )
        return self.geologic_index

    def calc_erosion_level(self):
        self.erosion_level = (self.geologic_index + self.cave.depth) % 20183
        return self.erosion_level

    def determine_type(self):
        self.type = self.erosion_level % 3
        return self.type


def build_cave(target_x, target_y, depth):
    cave = Cave(target_x, target_y, depth)
    max_size = max(target_x, target_y)
    for i in range(max_size + 1):
        for x in range(min(i, target_x)):
            cave[(x, i)] = Region(x, i, cave)
        for y in range(min(i, target_y)):
            cave[(i, y)] = Region(i, y, cave)
        cave[(min(i, target_x), min(i, target_y))] = Region(
            min(i, target_x), min(i, target_y), cave
        )
    return cave


def calc_risk_level(target_x, target_y, cave):
    risk_level = 0
    for x in range(target_x + 1):
        for y in range(target_y + 1):
            risk_level += cave[(x, y)].type
    return risk_level


if __name__ == '__main__':
    target_x = 12
    target_y = 757
    cave_depth = 3198
    cave = build_cave(target_x, target_y, cave_depth)
    print(f'answer: {calc_risk_level(target_x, target_y, cave)}')
