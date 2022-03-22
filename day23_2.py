from __future__ import annotations

import datetime
import logging
import sys
from collections import Counter
from itertools import combinations
from logging import StreamHandler
from typing import List

from day23_1 import Nanobot, parse_input23

logger = logging.getLogger('advent_of_code.2018.day23_2')
logging.basicConfig(
    filename='day23_2.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


class Prism:
    """Represents a rectangular prism of eight points"""

    def __init__(self, minx, maxx, miny, maxy, minz, maxz):
        """Has eight points that define it, using UNW for upper northwest, LNW for lower northwest, etc."""
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz

    def __str__(self):
        return f'Prism {self.center=}, width={self.maxx - self.minx}, height={self.maxy - self.miny}, depth={self.maxz - self.minz}'

    def __hash__(self):
        answer = ''
        for dimension in [
            self.minx,
            self.maxx,
            self.miny,
            self.maxy,
            self.minz,
            self.maxz,
        ]:
            if dimension >= 0:
                answer += '0'
            else:
                answer += '1'
            answer += str(abs(dimension))
        return int(answer)

    def __eq__(self, other):
        return (
            self.minx == other.minx
            and self.maxx == other.maxx
            and self.miny == other.miny
            and self.maxy == other.maxy
            and self.minz == other.minz
            and self.maxz == other.maxz
        )

    def split(self) -> List[Prism]:
        """splits the prism into eight prisms"""
        # start with special case
        if (
            self.maxx - self.minx <= 1
            and self.maxy - self.miny <= 1
            and self.maxz - self.minz <= 1
        ):
            unw_prism = Prism(
                self.minx, self.minx, self.maxy, self.maxy, self.maxz, self.maxz
            )
            une_prism = Prism(
                self.maxx, self.maxx, self.maxy, self.maxy, self.maxz, self.maxz
            )
            usw_prism = Prism(
                self.minx, self.minx, self.miny, self.miny, self.maxz, self.maxz
            )
            use_prism = Prism(
                self.maxx, self.maxx, self.miny, self.miny, self.maxz, self.maxz
            )
            lnw_prism = Prism(
                self.minx, self.minx, self.maxy, self.maxy, self.minz, self.minz
            )
            lne_prism = Prism(
                self.maxx, self.maxx, self.maxy, self.maxy, self.minz, self.minz
            )
            lsw_prism = Prism(
                self.minx, self.minx, self.miny, self.miny, self.minz, self.minz
            )
            lse_prism = Prism(
                self.maxx, self.maxx, self.miny, self.miny, self.minz, self.minz
            )
        else:
            # Create in order UNW, UNE, USW, USE, LNW, LNE, LSW, LSE
            unw_prism = Prism(
                self.minx,
                self.center[0],
                self.center[1],
                self.maxy,
                self.center[2],
                self.maxz,
            )
            une_prism = Prism(
                self.center[0],
                self.maxx,
                self.center[1],
                self.maxy,
                self.center[2],
                self.maxz,
            )
            usw_prism = Prism(
                self.minx,
                self.center[0],
                self.miny,
                self.center[1],
                self.center[2],
                self.maxz,
            )
            use_prism = Prism(
                self.center[0],
                self.maxx,
                self.miny,
                self.center[1],
                self.center[2],
                self.maxz,
            )
            lnw_prism = Prism(
                self.minx,
                self.center[0],
                self.center[1],
                self.maxy,
                self.minz,
                self.center[2],
            )
            lne_prism = Prism(
                self.center[0],
                self.maxx,
                self.center[1],
                self.maxy,
                self.minz,
                self.center[2],
            )
            lsw_prism = Prism(
                self.minx,
                self.center[0],
                self.miny,
                self.center[1],
                self.minz,
                self.center[2],
            )
            lse_prism = Prism(
                self.center[0],
                self.maxx,
                self.miny,
                self.center[1],
                self.minz,
                self.center[2],
            )
        return [
            unw_prism,
            une_prism,
            usw_prism,
            use_prism,
            lnw_prism,
            lne_prism,
            lsw_prism,
            lse_prism,
        ]

    @property
    def UNW(self):
        return self.minx, self.maxy, self.maxz

    @property
    def UNE(self):
        return self.maxx, self.maxy, self.maxz

    @property
    def USW(self):
        return self.minx, self.miny, self.maxz

    @property
    def USE(self):
        return self.maxx, self.miny, self.maxz

    @property
    def LNW(self):
        return self.minx, self.maxy, self.minz

    @property
    def LNE(self):
        return self.maxx, self.maxy, self.minz

    @property
    def LSW(self):
        return self.minx, self.miny, self.minz

    @property
    def LSE(self):
        return self.maxx, self.miny, self.minz

    @property
    def center(self):
        return (
            (self.minx + self.maxx) // 2,
            (self.miny + self.maxy) // 2,
            (self.minz + self.maxz) // 2,
        )

    @property
    def is_point(self):
        return (
            self.minx == self.maxx and self.miny == self.maxy and self.minz == self.minz
        )

    def count_overlaps(self, nanobots):
        return sum(1 for bot in nanobots if self.overlaps(bot))

    def overlaps(self, bot: Nanobot):
        # should be a terser way to do this
        if bot.x < self.minx:
            x = self.minx
        elif bot.x > self.maxx:
            x = self.maxx
        else:
            x = bot.x

        if bot.y < self.miny:
            y = self.miny
        elif bot.y > self.maxy:
            y = self.maxy
        else:
            y = bot.y

        if bot.z < self.minz:
            z = self.minz
        elif bot.z > self.maxz:
            z = self.maxz
        else:
            z = bot.z

        return manhattan_distance((bot.x, bot.y, bot.z), (x, y, z)) <= bot.radius


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])


def find_position_for_transport(nanobots):
    point_reachability = Counter()

    for i, n in enumerate(nanobots):
        logger.info(f'producing points for nanobot {i+1} with radius {n.radius}')
        for point in n.produce_reachable_points():
            point_reachability[point] += 1

    logger.info("getting most common")
    most_common = point_reachability.most_common()
    most_reachable_point_distance = most_common[0][1]
    most_reachable_points = [
        mc[0] for mc in most_common if mc[1] == most_reachable_point_distance
    ]
    logger.info(f'{len(most_reachable_points)} points tied for most reachable')

    closest_to_me = sorted(
        most_reachable_points, key=lambda x: manhattan_distance(x, (0, 0, 0))
    )[0]
    return closest_to_me


def position_in_range_of_most_nanobots(filename):
    nanobots = parse_input23(filename)
    return find_position_for_transport(nanobots)


def distance_to_position_in_range_of_most_nanobots(filename):
    position = position_in_range_of_most_nanobots(filename)
    answer = manhattan_distance(position, (0, 0, 0))
    return answer


def find_center(nanobots):
    min_x = min(bot.x for bot in nanobots)
    min_y = min(bot.y for bot in nanobots)
    min_z = min(bot.y for bot in nanobots)
    max_x = max(bot.x for bot in nanobots)
    max_y = max(bot.y for bot in nanobots)
    max_z = max(bot.y for bot in nanobots)

    return (min_x + max_x) / 2, (min_y + max_y) / 2, (min_z + max_z) / 2


def prism_from_nanobots(nanobots) -> Prism:
    return Prism(
        min(bot.x for bot in nanobots),
        max(bot.x for bot in nanobots),
        min(bot.y for bot in nanobots),
        max(bot.y for bot in nanobots),
        min(bot.z for bot in nanobots),
        max(bot.z for bot in nanobots),
    )


class OctreeSolver:
    """Uses DFS to maintain state to search"""

    def __init__(self, nanobots, prism=None):
        self.nanobots = nanobots
        self.max_solution = 0
        self.best_point_for_max_solution = None

    def solve(self):
        prism = prism_from_nanobots(self.nanobots)
        self._solve(prism)
        return self.max_solution, self.best_point_for_max_solution

    def _solve(self, prism):
        if prism.is_point:
            point_overlaps = prism.count_overlaps(self.nanobots)
            if point_overlaps > self.max_solution:
                logger.info(f'best solution found so far: {point_overlaps}')
                self.max_solution = point_overlaps
                self.best_point_for_max_solution = prism.minx, prism.miny, prism.minz
            elif point_overlaps and point_overlaps == self.max_solution:
                if abs(prism.minx) + abs(prism.maxy) + abs(prism.minz) < abs(
                    self.best_point_for_max_solution[0]
                ) + abs(self.best_point_for_max_solution[1]) + abs(
                    self.best_point_for_max_solution[2]
                ):
                    self.best_point_for_max_solution = (
                        prism.minx,
                        prism.miny,
                        prism.minz,
                    )
        else:
            octoprisms = prism.split()
            for sub_prism in octoprisms:
                if sub_prism.count_overlaps(self.nanobots) >= self.max_solution:
                    self._solve(sub_prism)


def main_octree(filename):
    nanobots = parse_input23(filename)
    best_prism = octree_solver(nanobots)
    return (
        best_prism.minx,
        best_prism.miny,
        best_prism.minz,
        best_prism.count_overlaps(nanobots),
    )


def octree_solver(nanobots):
    prisms_under_consideration = [prism_from_nanobots(nanobots)]
    max_overlaps = 0

    while not all(prism.is_point for prism in prisms_under_consideration):
        print(f'=== {datetime.datetime.now()} ===')
        print(f'{len(prisms_under_consideration)=}, {max_overlaps=}')
        print(list(prisms_under_consideration)[0], end='\n\n')

        max_overlaps = 0
        new_prisms_under_consideration = []
        for prism in prisms_under_consideration:
            prisms = prism.split()
            for sub_prism in prisms:
                num_overlaps = sub_prism.count_overlaps(nanobots)
                if num_overlaps > max_overlaps:
                    max_overlaps = num_overlaps
                    new_prisms_under_consideration = [sub_prism]
                elif num_overlaps and num_overlaps == max_overlaps:
                    new_prisms_under_consideration.append(sub_prism)

        prisms_under_consideration = set(new_prisms_under_consideration)

    final_prisms = sorted(
        [
            (abs(p.minx) + abs(p.miny) + abs(p.minz), p)
            for p in prisms_under_consideration
        ]
    )

    return final_prisms[0][1]


if __name__ == '__main__':
    x, y, z, overlaps = main_octree("data/input23.txt")
    print(f'{overlaps=} at {x=}, {y=}, {z=}')
    print(
        f'answer: {abs(x) + abs(y) + abs(z)}'
    )  # 71_406_282 is too low (comes from overlaps=856 at x=24211378, y=19620241, z=27574663)
