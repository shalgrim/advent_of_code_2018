import logging
from enum import Enum, auto

logger = logging.getLogger('advent_of_code_2018.day22_1')

TARGET_X = 12
TARGET_Y = 757
CAVE_DEPTH = 3198


class RegionType(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class Equipment(Enum):
    NO = auto()
    CLIMB = auto()
    TORCH = auto()


POSSIBLE_EQUIPMENT = {
    RegionType.ROCKY: {Equipment.CLIMB, Equipment.TORCH},
    RegionType.WET: {Equipment.CLIMB, Equipment.NO},
    RegionType.NARROW: {Equipment.TORCH, Equipment.NO},
}


class Cave(object):
    def __init__(self, target_x, target_y, depth):
        self.target_x = target_x
        self.target_y = target_y
        self.depth = depth
        self.regions = {}

    def __getitem__(self, item):
        try:
            return self.regions[item]
        except KeyError:
            logger.debug(f'{item=}')
            self.regions[item] = Region(item[0], item[1], self)
            return self.regions[item]

    def __setitem__(self, key, value):
        self.regions[key] = value

    def get_move_cost(self, from_pos, to_pos, equipment):
        from_type = RegionType(self[from_pos].tipe)
        to_type = RegionType(self[to_pos].tipe)

        if from_type == to_type:
            return 1, equipment

        solution_equipment = POSSIBLE_EQUIPMENT[from_type].intersection(
            POSSIBLE_EQUIPMENT[to_type]
        )

        if equipment in solution_equipment:
            return 1, equipment

        return 8, solution_equipment.pop()


class Region(object):
    def __init__(self, x, y, cave):
        self.x = x
        self.y = y
        self.cave = cave
        self.geologic_index = 0
        self.calc_geologic_index()

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

    @property
    def erosion_level(self):
        return (self.geologic_index + self.cave.depth) % 20183

    @property
    def tipe(self):
        return RegionType(self.erosion_level % 3)


def build_cave(target_x, target_y, depth, extra_x=0, extra_y=0):
    """This build_cave was intended to narrow the cave and it runs test_part_one in 100 ms"""
    cave = Cave(target_x, target_y, depth)
    max_y = target_y + extra_y
    max_x = target_x + extra_x
    max_size = max(max_y, max_x)
    print(f'{max_size=}')

    for i in range(max_size + 1):
        print(f'{i=}')

        for x in range(min(i, max_x + 1)):
            cave[(x, i)] = Region(x, i, cave)
        # Note we assume max_x is always less than max_y otherwise this doesn't work
        if i <= max_x + 1:
            for y in range(min(i, max_y + 1)):
                cave[(i, y)] = Region(i, y, cave)

        if i <= max_x + 1 and i <= max_y + 1:
            cave[(i, i)] = Region(i, i, cave)

    return cave


# def build_cave(target_x, target_y, depth):
#     """This build_cave works and TestDay22.test_part_one passes, but it takes 1.926 s"""
#     cave = Cave(target_x, target_y, depth)
#     max_size = max(target_x, target_y)
#     for i in range(max_size + 1):
#         for x in range(i):
#             cave[(x, i)] = Region(x, i, cave)
#         for y in range(i):
#             cave[(i, y)] = Region(i, y, cave)
#         cave[(i, i)] = Region(i, i, cave)
#     return cave


def calc_risk_level(target_x, target_y, cave):
    risk_level = 0
    for x in range(target_x + 1):
        for y in range(target_y + 1):
            risk_level += cave[(x, y)].tipe
    return risk_level


if __name__ == '__main__':
    cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
    print(f'answer: {calc_risk_level(TARGET_X, TARGET_Y, cave)}')
