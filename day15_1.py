class Monster(object):
    def __init__(self):
        self.hp = 100

    @property
    def alive(self):
        return self.hp > 0


class Elf(Monster):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'E({self.hp})'


class Goblin(Monster):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f'G({self.hp})'


class Cave(object):
    def __init__(self):
        self.elves = []
        self.goblins = []
        self.walls = set()
        self.floors = set()

    def tick(self):
        pass

    def __str__(self):
        max_y = max(w.y for w in self.walls)
        max_x = max(w.x for w in self.walls)

        lines = []
        for y in range(max_y + 1):
            line_chars = []
            for x in range(max_x + 1):
                if (x, y) in self.walls:
                    line_chars.append('#')
                elif (x, y) in self.elves:
                    line_chars.append('E')
                elif (x, y) in self.goblins:
                    line_chars.append('G')
                else:
                    line_chars.append('.')

            line = ''.join(line_chars)
            monsters = [g for p, g in self.goblins.items() if p[1] == y]
            monsters += [e for p, e in self.elves.items() if p[1] == y]
            monsters.sort(key=lambda m: m.x)
            if monsters:
                line += '   '
                line += ', '.join(str(m) for m in monsters)
            lines.append(line)
        return '\n'.join(lines) + '\n\n\n'


def parse_cave_input(filename):
    with open(filename) as f:
        lines = f.readlines()

    cave = Cave()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                cave.walls.add((x, y))
            elif char == '.':
                cave.floors.add((x, y))
            elif char == 'G':
                cave.floors.add((x, y))
                cave.goblins.append(Goblin())
            elif char == 'E':
                cave.floors.add((x, y))
                cave.elves.append(Elf())

    return cave


def calculate_cave_outcome(cave, completed_rounds):
    pass


def run_cave_game(cave):
    completed_rounds = 0
    while any(elf.alive for elf in cave.elves) and any(
        goblin.alive for goblin in cave.goblins
    ):
        print(cave)
        cave.tick()
        completed_rounds += 1

    return calculate_cave_outcome(cave, completed_rounds)


if __name__ == '__main__':
    cave = parse_cave_input('data/input15.txt')
    outcome = run_cave_game(cave)
    print(outcome)
