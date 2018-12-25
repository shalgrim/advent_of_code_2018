from copy import copy


def identify_open_squares_in_range_of_targets(cave, targets):
    open_squares_adjacent_to_targets = set()
    for target in targets:
        tx, ty = target.location
        squares_to_check = [(tx + 1, ty), (tx - 1, ty), (tx, ty + 1), (tx, ty - 1)]
        for square in squares_to_check:
            if cave.is_open_square(*square):
                open_squares_adjacent_to_targets.add(square)
    return open_squares_adjacent_to_targets


class Monster(object):
    def __init__(self, x, y, cave):
        self.hp = 100
        self.x = x
        self.y = y
        self.cave = cave

    @property
    def alive(self):
        return self.hp > 0

    @property
    def location(self):
        return self.x, self.y

    def identify_targets(self):
        return [m for m in self.cave.monsters if not isinstance(m, type(self))]

    def move_toward_square(self, target_location):
        all_paths = self.cave.find_all_paths(self.location, target_location)
        sorted_paths = sorted(all_paths, key=lambda x: len(x))
        shortest_distance = len(sorted_paths)[0]
        shortest_paths = [path for path in sorted_paths if len(path) == shortest_distance]
        sorted_next_steps = sorted([p[0] for p in shortest_paths], key=reading_order)
        next_step = sorted_next_steps[0]
        self.x = next_step[0]
        self.y = next_step[1]

    def move(self, squares):
        reachable_squares = self.cave.determine_reachable_target_squares(
            (self.x, self.y), squares
        )
        sorted_reachable_squares = sorted(reachable_squares.items(), key=lambda x: x[1])
        shortest_distance = sorted_reachable_squares[0][1]
        closest_reachable_squares = [square for square in sorted_reachable_squares if square[1] == shortest_distance]
        sorted_closest_squares = sorted(closest_reachable_squares, key=reading_order)
        if not sorted_reachable_squares:
            return
        target_square = sorted_reachable_squares[0]
        self.move_toward_square(target_square[0])

    def take_turn(self):
        targets = self.identify_targets()
        squares = identify_open_squares_in_range_of_targets(self.cave, targets)
        if (self.x, self.y) in squares:
            pass  # don't move, you're already next to target
        else:
            self.move(squares)


class Elf(Monster):
    def __init__(self, x, y, cave):
        super().__init__(x, y)

    def __str__(self):
        return f'E({self.hp})'


class Goblin(Monster):
    def __init__(self, x, y, cave):
        super().__init__(x, y)

    def __str__(self):
        return f'G({self.hp})'


def reading_order(monster):
    return monster.y, monster.x


class Cave(object):
    def __init__(self):
        self.elves = []
        self.goblins = []
        self.walls = set()
        self.floors = set()

    def is_open_square(self, x, y):
        if (x, y) not in self.floors:
            return False
        if any([g.x == x and g.y == y for g in self.goblins]):
            return False
        if any([e.x == x and e.y == y for e in self.elves]):
            return False
        return True

    def tick(self):
        monsters = sorted(self.monsters, key=reading_order)
        for monster in monsters:
            monster.take_turn()

    def __str__(self):
        max_y = max(w[1] for w in self.walls)
        max_x = max(w[0] for w in self.walls)

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
            monsters = [g for g in self.goblins if g.y == y]
            monsters += [e for e in self.elves if e.y == y]
            monsters.sort(key=lambda m: m.x)
            if monsters:
                line += '   '
                line += ', '.join(str(m) for m in monsters)
            lines.append(line)
        return '\n'.join(lines) + '\n\n\n'

    def determine_all_reachable_squares(self, start_loc, num_steps=0, visited=None):
        if visited and start_loc in visited and visited[start_loc] <= num_steps:
            return visited

        if visited:
            visited[start_loc] = num_steps
        else:
            visited = {start_loc: num_steps}

        for point in [
            (start_loc.x, start_loc.y + 1),
            (start_loc.x + 1, start_loc.y),
            (start_loc.x, start_loc.y - 1),
            (start_loc.x - 1, start_loc.y),
        ]:
            if self.is_open_square(*point):
                visited = self.determine_all_reachable_squares(point, num_steps + 1, visited)

        return visited

    def determine_reachable_target_squares(self, start_loc, squares):
        """
        Determines which squares can be reached from start_loc
        :param start_loc: x, y tuple of starting location
        :param squares: set of (x, y) tuples we'd like to try to reach
        :return: dict of squares in squares reachable from start_loc with shortest path taken to them
        """
        all_reachable_squares = self.determine_all_reachable_squares(start_loc)
        answer = {k: v for k, v in all_reachable_squares.items() if k in squares}
        return answer

    def find_all_paths(self, start_loc, target_loc, path=None):
        if not path:
            path = []

        if start_loc == target_loc:
            return path

        startx, starty = start_loc
        paths = []
        for point in [(startx, starty+1), (startx+1, starty), (startx, starty-1), (startx-1, starty)]:
            if point in path:
                continue
            elif self.is_open_square(point):
                newpath = copy(path)
                newpath.append(point)
                paths += self.find_all_paths(point, target_loc, path)
            else:
                continue
        return paths


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
                cave.goblins.append(Goblin(x, y))
            elif char == 'E':
                cave.floors.add((x, y))
                cave.elves.append(Elf(x, y))

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
