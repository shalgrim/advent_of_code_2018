class Cave(object):
    def __init__(self):
        self.elves = []
        self.goblins = []

    def tick(self):
        pass


def parse_cave_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    cave = Cave()
    for line in lines:
        pass
    return cave


def run_cave_game(cave):
    completed_rounds = 0
    while any(elf.alive for elf in cave.elves) and any(
        goblin.alive for goblin in cave.goblins
    ):
        cave.tick()
        completed_rounds += 1
    pass


if __name__ == '__main__':
    cave = parse_cave_input('data/input15.txt')
    outcome = run_cave_game(cave)
    print(outcome)
