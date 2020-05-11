"""Breadth First Search"""
import logging
import sys
from copy import copy, deepcopy
from logging import StreamHandler

from day22_1 import CAVE_DEPTH, TARGET_X, TARGET_Y, RegionType, build_cave
from day22_2 import POSSIBLE_EQUIPMENT, Direction, Equipment

logger = logging.getLogger('advent_of_code_2018.day22_2_2')
logging.basicConfig(
    filename='day22_2_2.log',
    level=logging.DEBUG,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


class PathState:
    def __init__(self, equipment=None, nodes=None, cost=0):
        self.equipment = equipment
        self.nodes = deepcopy(nodes) if nodes else []
        self.cost = cost

    @property
    def current_x(self):
        return self.current_pos[0]

    @property
    def current_y(self):
        return self.current_pos[1]

    @property
    def current_pos(self):
        return self.nodes[-1]

    def get_next_pos(self, direction):
        assert self.nodes, 'Initialize nodes before trying to get next position'
        if direction == Direction.UP and self.current_y > 0:
            return self.current_x, self.current_y - 1
        if direction == Direction.LEFT and self.current_x > 0:
            return self.current_x - 1, self.current_y
        if direction == Direction.DOWN:
            return self.current_x, self.current_y + 1
        if direction == Direction.RIGHT:
            return self.current_x + 1, self.current_y
        return None

    def get_next_equipment(self, from_type, to_type):
        if from_type == to_type:
            return self.equipment

        solution_equipment = POSSIBLE_EQUIPMENT[from_type].intersection(
            POSSIBLE_EQUIPMENT[to_type]
        )

        if (
            solution_equipment and self.equipment in solution_equipment
        ):  # we could change but why
            return self.equipment

        return solution_equipment.pop()  # there should be only one thing to switch to

    def get_new_paths(self, cave):
        new_paths = []

        for d in Direction:
            next_pos = self.get_next_pos(d)
            from_type = RegionType(cave[self.current_pos].tipe)
            to_type = RegionType(cave[next_pos].tipe)
            next_equipment = self.get_next_equipment(from_type, to_type)
            new_cost = 1 if next_equipment == self.equipment else 8
            new_nodes = copy(self.nodes)
            new_nodes.append(next_pos)
            new_path = PathState(
                equipment=next_equipment, nodes=new_nodes, cost=self.cost + new_cost
            )
            new_paths.append(new_path)

        return new_paths

    def uniqueify(self):
        return str(self.nodes), self.equipment


class PathFinderBFS:
    def __init__(
        self,
        cave,
        target_x,
        target_y,
        initial_x=0,
        initial_y=0,
        initial_equip=Equipment.TORCH,
    ):
        self.cave = cave
        self.target_position = target_x, target_y
        self.paths = [PathState(initial_equip, [(initial_x, initial_y)], 0)]
        self.shortest_known_path = self._calculate_baseline_path_cost(
            cave, self.paths[-1]
        )

    def reduce_paths(self):
        """Get rid of duplicate paths"""
        reduced_paths = []
        reduced_paths_uniqueifed = set()

        for path in self.paths:
            if path.cost > self.shortest_known_path:
                continue

            if path.uniqueify() not in reduced_paths_uniqueifed:
                reduced_paths.append(path)
                reduced_paths_uniqueifed.add(path.uniqueify())

        self.paths = reduced_paths

    def extract_solutions(self):
        paths_to_continue = []
        solutions = []

        for path in self.paths:
            if path.current_pos == self.target_position:
                if path.equipment != Equipment.TORCH:
                    path.cost += 7
                solutions.append(path)
            else:
                paths_to_continue.append(path)

        self.paths = paths_to_continue
        return solutions

    def find_quickest_path(self):
        solutions = self.extract_solutions()
        while self.paths:
            new_paths = []
            for path in self.paths:
                new_paths += path.get_new_paths(self.cave)

            self.paths = new_paths
            self.reduce_paths()
            solutions += self.extract_solutions()
            self.shortest_known_path = (
                min(s.cost for s in solutions)
                if solutions
                else self.shortest_known_path
            )

        return min(
            s.cost for s in solutions
        )  # current bug, sometimes there are no solutions at this point

    def _calculate_baseline_path_cost(self, cave, initial_path=None):
        cost1 = 0
        cost2 = 0
        if initial_path:
            initial_x = initial_path.current_x
            initial_y = initial_path.current_y
            initial_equipment = initial_path.equipment
        else:
            initial_x = 0
            initial_y = 0
            initial_equipment = Equipment.TORCH

        if initial_y == self.target_position[1]:
            y = initial_y
        if initial_x == self.target_position[0]:
            x = initial_x

        equipment = initial_equipment

        for x in range(initial_x, self.target_position[0]):
            move_cost, equipment = self.cave.get_move_cost(
                (x, initial_y), (x + 1, initial_y), equipment
            )
            cost1 += move_cost

        if self.target_position[1] >= initial_y:
            for y in range(initial_y, self.target_position[1]):
                move_cost, equipment = self.cave.get_move_cost(
                    (x, y), (x, y + 1), equipment
                )
                cost1 += move_cost
        else:
            for y in range(initial_y, self.target_position[1], -1):
                move_cost, equipment = self.cave.get_move_cost(
                    (x, y), (x, y + 1), equipment
                )
                cost1 += move_cost

        equipment = initial_equipment

        if self.target_position[1] >= initial_y:
            for y in range(initial_y, self.target_position[1]):
                move_cost, equipment = self.cave.get_move_cost(
                    (initial_x, y), (initial_x, y - 1), equipment
                )
                cost2 += move_cost
        else:
            for y in range(initial_y, self.target_position[1], -1):
                move_cost, equipment = self.cave.get_move_cost(
                    (initial_x, y), (initial_x, y - 1), equipment
                )
                cost2 += move_cost

        for x in range(initial_x, self.target_position[0]):
            move_cost, equipment = self.cave.get_move_cost(
                (x, y), (x + 1, y), equipment
            )
            cost2 += move_cost

        if initial_x == self.target_position[0]:
            return cost1
        elif initial_y == self.target_position[1]:
            return cost2
        else:
            return min(cost1, cost2)


def main():
    cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
    pf = PathFinderBFS()
    qp = pf.find_quickest_path()
    return qp.cost
