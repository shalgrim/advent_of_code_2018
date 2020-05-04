from day22_1 import CAVE_DEPTH, TARGET_X, TARGET_Y, build_cave


class PathFinder:
    def __init__(self, cave):
        self.cave = cave
        self.shortest_paths = {}  # (from_x, from_y, to_x, to_y, equipment) -> int
        self.current_path_length = 0

    def find_quickest_path(self, target_x, target_y, from_x=0, from_y=0):
        raise NotImplementedError


def main():
    cave = build_cave(TARGET_X, TARGET_Y, CAVE_DEPTH)
    pf = PathFinder(cave)
    return pf.find_quickest_path(TARGET_X, TARGET_Y)


if __name__ == '__main__':
    print(main())
