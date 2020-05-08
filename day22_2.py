import logging
import sys
from copy import deepcopy
from enum import Enum, auto
from logging import StreamHandler

from day22_1 import CAVE_DEPTH, TARGET_X, TARGET_Y, RegionType, build_cave

logger = logging.getLogger('advent_of_code_2018.day22_2')
logging.basicConfig(
    filename='day22_2.log',
    level=logging.DEBUG,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


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


class State:
    def __init__(self, position, equipment, visited, cost):
        self.position = position
        self.equipment = equipment
        self.visited = visited
        self.cost = cost

    def get_next_position(self, direction):
        if direction == Direction.UP:
            if self.position[1] == 0:
                return False
            next_position = self.position[0], self.position[1] - 1
        elif direction == Direction.RIGHT:
            next_position = self.position[0] + 1, self.position[1]
        elif direction == Direction.DOWN:
            next_position = self.position[0], self.position[1] + 1
        elif direction == Direction.LEFT:
            if self.position[0] == 0:
                return False
            next_position = self.position[0] - 1, self.position[1]
        else:
            raise Exception('should not be here')

        return next_position if next_position not in self.visited else False


class PathFinder:
    def __init__(self, cave, target_x, target_y):
        self.cave = cave
        self.target_position = target_x, target_y
        self.known_shortest_path = None
        self._set_baseline_shortest_path()

    def get_possible_equipment(self, x, y):
        region_type = self.cave[(x, y)].tipe
        return POSSIBLE_EQUIPMENT[RegionType(region_type)]

    def get_move_equipment(self, state, to_position):
        assert (
            state.position[0] == to_position[0]
            and abs(state.position[1] - to_position[1]) == 1
        ) or (
            state.position[1] == to_position[1]
            and abs(state.position[0] - to_position[0]) == 1
        ), f"can't move from {state.position=} to {to_position=}"

        from_type = RegionType(self.cave[state.position].tipe)
        to_type = RegionType(self.cave[to_position].tipe)

        if from_type == to_type:
            return state.equipment

        solution_equipment = POSSIBLE_EQUIPMENT[from_type].intersection(
            POSSIBLE_EQUIPMENT[to_type]
        )
        if solution_equipment and state.equipment in solution_equipment:
            return state.equipment

        return solution_equipment.pop()

    def get_move_state(self, existing_state, next_position):
        next_equipment = self.get_move_equipment(existing_state, next_position)
        next_cost = 1 if next_equipment == existing_state.equipment else 8

        nextstate = deepcopy(existing_state)
        nextstate.position = next_position
        nextstate.equipment = next_equipment
        nextstate.cost += next_cost
        nextstate.visited.append(next_position)

        return nextstate

    def find_quickest_path(self, state=None):
        state = (
            State(position=(0, 0), equipment=Equipment.TORCH, visited=[(0, 0)], cost=0)
            if state is None
            else state
        )
        logger.debug(f'{state.position=} {state.cost=}')

        if state.position == self.target_position:
            final_cost = (
                state.cost if state.equipment == Equipment.TORCH else state.cost + 7
            )
            if final_cost < self.known_shortest_path:
                self.known_shortest_path = final_cost

        if state.cost >= self.known_shortest_path:
            return

        for d in Direction:
            next_position = state.get_next_position(d)
            if not next_position:
                continue

            nextstate = self.get_move_state(state, next_position)
            self.find_quickest_path(nextstate)

    def _set_baseline_shortest_path(self):
        """go straight there, down then right"""
        state = State(
            position=(0, 0), equipment=Equipment.TORCH, visited=[(0, 0)], cost=0
        )

        while state.position[0] < self.target_position[0]:
            state = self.get_move_state(
                state, (state.position[0] + 1, state.position[1])
            )

        while state.position[1] < self.target_position[1]:
            state = self.get_move_state(
                state, (state.position[0], state.position[1] + 1)
            )

        self.known_shortest_path = state.cost


def main():
    cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
    pf = PathFinder(cave, TARGET_X, TARGET_Y)
    pf.find_quickest_path()
    return pf.known_shortest_path


if __name__ == '__main__':
    print(main())
