from enum import Enum, auto

from day22_1 import CAVE_DEPTH, TARGET_X, TARGET_Y, RegionType, build_cave


class Equipment(Enum):
    NO = auto()
    CLIMB = auto()
    TORCH = auto()


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


POSSIBLE_EQUIPMENT = {
    RegionType.ROCKY: set([Equipment.CLIMB, Equipment.TORCH]),
    RegionType.WET: set([Equipment.CLIMB, Equipment.NO]),
    RegionType.NARROW: set([Equipment.TORCH, Equipment.NO]),
}


class PathFinder:
    def __init__(self, cave, target_x, target_y):
        self.cave = cave
        self.current_path_length = 0
        self.current_position = 0, 0
        self.target_position = target_x, target_y
        self.current_equipment = Equipment.TORCH

        # BASELINE: assume you can go straight there but have to change at every step
        self.known_shortest_path = target_y + target_x + 7 * (target_y + target_x)

    def get_possible_equipment(self, x, y):
        region_type = self.cave[(x, y)].tipe

    def _get_next_position(self, direction):
        if direction == Direction.UP:
            if self.current_position[1] == 0:
                return False
            return self.current_position[0], self.current_position[1] - 1
        elif direction == Direction.RIGHT:
            return self.current_position[0] + 1, self.current_position[1]
        elif direction == Direction.DOWN:
            return self.current_position[0], self.current_position[1] + 1
        elif direction == Direction.LEFT:
            if self.current_position[0] == 0:
                return False
            return self.current_position[0] - 1, self.current_position[1]

    def move(self, direction):
        next_position = self._get_next_position(direction)

        if not next_position:
            return False
        current_region_type = self.cave[self.current_position].tipe

    def find_quickest_path(self, cost=0):
        if self.current_position == self.target_position:
            final_cost = cost if self.current_equipment == Equipment.TORCH else cost + 7
            if final_cost < self.known_shortest_path:
                self.known_shortest_path = final_cost
            return final_cost

        for d in Direction:
            move_cost = self.move(d)
            if move_cost:
                self.find_quickest_path(cost + move_cost)


def main():
    cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
    pf = PathFinder(cave, TARGET_X, TARGET_Y)
    pf.find_quickest_path()
    return pf.known_shortest_path


if __name__ == '__main__':
    print(main())
