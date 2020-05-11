"""
This ran overnight and came up with a best of like 52 (it was still running)
I think what's next is to start recording what the best cost is from each point so we're not re-doing these where we
know it can't get better
"""

import logging
import sys
from collections import defaultdict
from copy import deepcopy
from enum import Enum, auto
from logging import StreamHandler

from day22_1 import CAVE_DEPTH, TARGET_X, TARGET_Y, Equipment, RegionType, build_cave

logger = logging.getLogger('advent_of_code_2018.day22_2')
logging.basicConfig(
    filename='day22_2.log',
    level=logging.DEBUG,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


BREAK_STATES = [
    (0, 0),
    (0, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (4, 2),
    (4, 3),
    (4, 4),
    (4, 5),
    (4, 6),
    (4, 7),
    (4, 8),
    (5, 8),
    (5, 9),
    (5, 10),
    (5, 11),
    (6, 11),
    (6, 12),
    (7, 12),
    (8, 12),
    (9, 12),
    (10, 12),
    (10, 11),
    (10, 10),
]

HAPPY_PATH_STATES = [
    '(0, 0),Equipment.TORCH',
    '(0, 1),Equipment.TORCH',
    '(1, 1),Equipment.TORCH',
    '(1, 1),Equipment.NO',  # *switch, not recorded
    '(2, 1),Equipment.NO',
    '(3, 1),Equipment.NO',
    '(4, 1),Equipment.NO',
    '(4, 1),Equipment.CLIMB',  # *switch, not recorded
    '(4, 2),Equipment.CLIMB',
    '(4, 3),Equipment.CLIMB',
    '(4, 4),Equipment.CLIMB',
    '(4, 5),Equipment.CLIMB',
    '(4, 6),Equipment.CLIMB',
    '(4, 7),Equipment.CLIMB',
    '(4, 8),Equipment.CLIMB',
    '(5, 8),Equipment.CLIMB',
    '(5, 9),Equipment.CLIMB',
    '(5, 10),Equipment.CLIMB',
    '(5, 11),Equipment.CLIMB',
    '(6, 11),Equipment.CLIMB',
    '(6, 12),Equipment.CLIMB',
    '(7, 12),Equipment.CLIMB',
    '(8, 12),Equipment.CLIMB',
    '(9, 12),Equipment.CLIMB',
    '(10, 12),Equipment.CLIMB',
    '(10, 11),Equipment.CLIMB',
    '(10, 10),Equipment.CLIMB',
    '(10, 10),Equipment.TORCH',  # *switch, but a weird one
]


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


class KnownShortestTracker:
    def __init__(self):
        self.data = defaultdict(dict)

    def get_known_shortest(self, state):
        """returns best known lowest cost and incoming cost"""
        return self.data[state.position].get(state.equipment)

    def set_known_shortest(self, state, cost):
        if self.data[state.position].get(state.equipment):
            best_known, recorded_at = self.data[state.position].get(state.equipment)
            if recorded_at > state.cost and cost < best_known:
                self.data[state.position][state.equipment] = (cost, state.cost)
        else:
            self.data[state.position][state.equipment] = (cost, state.cost)


class State:
    def __init__(self, position, equipment, visited, cost):
        self.position = position
        self.equipment = equipment
        self.visited = visited
        self.cost = cost

    def __str__(self):
        return f'{self.position},{self.equipment}'

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

        return next_position  # if next_position not in self.visited else False


class PathFinder:
    def __init__(self, cave, target_x, target_y):
        self.cave = cave
        self.target_position = target_x, target_y
        self.known_shortest_path = None
        self._set_baseline_shortest_path()
        self.shortest_froms = KnownShortestTracker()

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

    def get_direction_order(self, state):
        fromx, fromy = state.position
        tox, toy = self.target_position

        horizontal = (
            [Direction.RIGHT, Direction.LEFT]
            if tox - fromx > 0
            else [Direction.LEFT, Direction.RIGHT]
        )
        vertical = (
            [Direction.DOWN, Direction.UP]
            if toy - fromy > 0
            else [Direction.UP, Direction.DOWN]
        )
        answer = []

        if abs(tox - fromx) > abs(
            toy - fromy
        ):  # further on x-axis so put horizontal in first
            answer = [horizontal[0], vertical[0], vertical[1], horizontal[1]]
        else:
            answer = [vertical[0], horizontal[0], horizontal[1], vertical[1]]

        return answer

    def find_quickest_path(self, state=None):
        state = (
            State(position=(0, 0), equipment=Equipment.TORCH, visited=[(0, 0)], cost=0)
            if state is None
            else state
        )

        if state.position == self.target_position:
            final_switch_cost = 0 if state.equipment == Equipment.TORCH else 7
            final_cost = final_switch_cost + state.cost
            if final_cost < self.known_shortest_path:
                self.known_shortest_path = final_cost

            return final_switch_cost

        if self.shortest_froms.get_known_shortest(state):
            known_best, recorded_at = self.shortest_froms.get_known_shortest(state)
        else:
            known_best, recorded_at = None, None

        if recorded_at and state.cost >= recorded_at:
            if state.cost + known_best < self.known_shortest_path:
                self.known_shortest_path = state.cost + known_best
            return known_best
        # implied else...if we're at a shorter incoming cost then we might get an even shorter one so keep going

        if state.cost >= self.known_shortest_path:
            return

        distances = []

        for d in self.get_direction_order(state):
            next_position = state.get_next_position(d)
            if not next_position:
                continue

            nextstate = self.get_move_state(state, next_position)
            total_cost_for_next = self.find_quickest_path(nextstate)

            if total_cost_for_next is not None:
                quickest = self.find_quickest_path(nextstate)
                step_cost = 1 if state.equipment == nextstate.equipment else 8
                distances.append(quickest + step_cost)

        if distances:
            shortest = min(distances)
            self.shortest_froms.set_known_shortest(state, shortest)
            return shortest
        else:
            return

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
