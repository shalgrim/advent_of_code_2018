from day23_1 import parse_input23
from day23_2 import Prism, distance_to_origin, prism_from_nanobots


class DFSSolver:
    def __init__(self, nanobots, overlap_seed=0, too_close_point_seed=(0, 0, 0)):
        self.nanobots = nanobots
        self.max_overlaps_found = overlap_seed
        self.best_point = None

    def prism_further_than_best_point(self, prism: Prism):
        return distance_to_origin(self.best_point) < distance_to_origin(
            prism.point_closest_to_origin
        )

    def solve(self, incoming_prism=None):
        prism = incoming_prism if incoming_prism else prism_from_nanobots(self.nanobots)
        if (overlaps := prism.count_overlaps(self.nanobots)) < self.max_overlaps_found:
            return
        elif (
            overlaps == self.max_overlaps_found
            and self.best_point
            and self.prism_further_than_best_point(prism)
        ):
            return

        if prism.is_point:
            if overlaps > self.max_overlaps_found:
                self.max_overlaps_found = overlaps
                self.best_point = prism.minx, prism.miny, prism.minz
                print('===')
                print(
                    f'more overlaps found with {self.max_overlaps_found=} at {self.best_point=}',
                    end='\n\n',
                )
            elif overlaps == self.max_overlaps_found:
                prism_point = prism.minx, prism.miny, prism.minz
                if self.best_point is None:
                    self.best_point = prism_point
                else:
                    if distance_to_origin(prism_point) < distance_to_origin(
                        self.best_point
                    ):
                        self.best_point = prism_point
                        print('===')
                        print(
                            f'found new best point with {self.max_overlaps_found=} at {self.best_point}, {distance_to_origin(self.best_point)} from origin',
                            end='\n\n',
                        )
            else:
                return
        else:
            # TODO: ignore anything where prism is all closer than too_close_point_seed
            sub_prisms = prism.split()
            for sub_prism in sub_prisms:
                self.solve(sub_prism)


def seeded_dfs_main(filename, overlap_seed=0, too_close_point_seed=(0, 0, 0)):
    nanobots = parse_input23(filename)
    solver = DFSSolver(nanobots, overlap_seed, too_close_point_seed)
    solver.solve()
    return solver.best_point, solver.max_overlaps_found


if __name__ == '__main__':
    (x, y, z), overlaps = seeded_dfs_main('data/input23.txt', 950)
    print(x, y, z, overlaps)
