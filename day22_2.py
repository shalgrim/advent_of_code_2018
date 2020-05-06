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
        self.known_shortest_path = None
        self._set_baseline_shortest_path()

    def get_possible_equipment(self, x, y):
        region_type = self.cave[(x, y)].tipe
        return POSSIBLE_EQUIPMENT[RegionType(region_type)]

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
        else:
            raise Exception('should not be here')

    def move(self, direction):
        next_position = self._get_next_position(direction)

        if not next_position:
            return False
        current_region_type = self.cave[self.current_position].tipe
        next_region_type = self.cave[next_position].tipe
        possible_equipment = self.get_possible_equipment(
            *self.current_position
        ).intersection((self.get_possible_equipment(*next_position)))
        if self.current_equipment in possible_equipment:
            move_cost = 1
        else:
            self.current_equipment = possible_equipment.pop()
            move_cost = 8

        self.current_position = next_position

        return move_cost

    def find_quickest_path(self, cost=0):
        if self.current_position == self.target_position:
            final_cost = cost if self.current_equipment == Equipment.TORCH else cost + 7
            if final_cost < self.known_shortest_path:
                self.known_shortest_path = final_cost
            return final_cost

        if cost >= self.known_shortest_path:
            return

        for d in Direction:
            move_cost = self.move(d)
            if move_cost:
                self.find_quickest_path(cost + move_cost)

    def _set_baseline_shortest_path(self):
        """go straight there, down then right"""
        cost = 0
        while self.current_position[0] < self.target_position[0]:
            cost += self.move(Direction.RIGHT)
        while self.current_position[1] < self.target_position[1]:
            cost += self.move(Direction.DOWN)

        self.current_position = 0, 0

        self.known_shortest_path = cost


def main():
    cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
    pf = PathFinder(cave, TARGET_X, TARGET_Y)
    pf.find_quickest_path()
    return pf.known_shortest_path


if __name__ == '__main__':
    print(main())
