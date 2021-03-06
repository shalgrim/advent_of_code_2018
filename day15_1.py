from copy import copy

from tqdm import tqdm


def identify_open_squares_in_range_of_targets(cave, targets, who_wants_to_know=None):
    open_squares_adjacent_to_targets = set()
    for target in targets:
        tx, ty = target.location
        squares_to_check = [(tx + 1, ty), (tx - 1, ty), (tx, ty + 1), (tx, ty - 1)]
        for square in squares_to_check:
            if cave.is_open_square(*square) or (
                who_wants_to_know and who_wants_to_know.location == square
            ):
                open_squares_adjacent_to_targets.add(square)
    return open_squares_adjacent_to_targets


class Monster(object):
    def __init__(self, x, y, cave):
        self.hp = 200
        self.power = 3
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
        if isinstance(self, Elf):
            return [g for g in self.cave.goblins if g.hp > 0]
        else:
            return [e for e in self.cave.elves if e.hp > 0]

    def move_toward_square(
        self, target_location, shortest_distance, all_reachable_squares
    ):
        """
        Take a step on the shortest path toward target_location
        :param target_location: location you want to get to
        :param shortest_distance: known shortest path from here to target_location
        :param all_reachable_squares: map of every reachable square in map and shortest distance to it
        :return: None
        """
        points_to_try = [
            (self.x, self.y - 1),
            (self.x - 1, self.y),
            (self.x + 1, self.y),
            (self.x, self.y + 1),
        ]

        for point in points_to_try:
            if point not in all_reachable_squares or all_reachable_squares[point] > 1:
                continue
            would_be_reachables = self.cave.determine_all_reachable_squares(point)
            if (
                target_location in would_be_reachables
                and would_be_reachables[target_location] == shortest_distance - 1
            ):
                self.x = point[0]
                self.y = point[1]
                break

    def move(self, squares):
        all_reachable_squares = self.cave.determine_all_reachable_squares(
            (self.x, self.y)
        )
        reachable_target_squares = {
            k: v for k, v in all_reachable_squares.items() if k in squares
        }
        sorted_reachable_target_squares = sorted(
            reachable_target_squares.items(), key=lambda x: x[1]
        )
        if not sorted_reachable_target_squares:
            return
        shortest_distance = sorted_reachable_target_squares[0][1]
        closest_reachable_squares = [
            square[0]
            for square in sorted_reachable_target_squares
            if square[1] == shortest_distance
        ]
        sorted_closest_squares = sorted(
            closest_reachable_squares, key=lambda x: (x[1], x[0])
        )
        if not sorted_closest_squares:
            return
        target_square = sorted_closest_squares[0]
        self.move_toward_square(target_square, shortest_distance, all_reachable_squares)

    def attack(self):
        if self.hp <= 0:  # if you died before you got a chance to attack this turn
            return
        adjacent_points = [
            (self.x + 1, self.y),
            (self.x - 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1),
        ]
        if isinstance(self, Elf):
            attackables = [
                g
                for g in self.cave.goblins
                if g.location in adjacent_points and g.hp > 0
            ]
        else:
            attackables = [
                e for e in self.cave.elves if e.location in adjacent_points and e.hp > 0
            ]

        second_key_sorted = sorted(attackables, key=reading_order)
        sorted_attackables = sorted(second_key_sorted, key=lambda x: x.hp)

        if not sorted_attackables:
            return
        to_attack = sorted_attackables[0]
        to_attack.hp -= self.power

        if to_attack.hp <= 0:
            pass

    def take_turn(self):
        if self.hp <= 0:  # if you died this round before your turn
            return True
        targets = self.identify_targets()
        if not targets:
            return False
        squares = identify_open_squares_in_range_of_targets(self.cave, targets, self)
        if (self.x, self.y) in squares:
            pass  # don't move, you're already next to target
        else:
            self.move(squares)
        self.attack()
        return True


class Elf(Monster):
    def __init__(self, x, y, cave):
        super().__init__(x, y, cave)

    def __str__(self):
        return f'E({self.hp})'


class Goblin(Monster):
    def __init__(self, x, y, cave):
        super().__init__(x, y, cave)

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
        if any([m.location == (x, y) and m.hp > 0 for m in self.goblins + self.elves]):
            return False
        return True

    def tick(self):
        monsters = sorted(self.elves + self.goblins, key=reading_order)
        complete_turn = True
        # for monster in tqdm(monsters):
        for monster in monsters:
            if monster.hp > 0:  # check to see if they died before their turn
                had_targets = monster.take_turn()
                if not had_targets:
                    complete_turn = False

        # clear out monsters that have died
        self.goblins = [g for g in self.goblins if g.hp > 0]
        self.elves = [e for e in self.elves if e.hp > 0]
        return complete_turn

    def __str__(self):
        max_y = max(w[1] for w in self.walls)
        max_x = max(w[0] for w in self.walls)

        lines = []
        for y in range(max_y + 1):
            line_chars = []
            for x in range(max_x + 1):
                if (x, y) in self.walls:
                    line_chars.append('#')
                elif (x, y) in [e.location for e in self.elves if e.hp > 0]:
                    line_chars.append('E')
                elif (x, y) in [g.location for g in self.goblins if g.hp > 0]:
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
            (start_loc[0], start_loc[1] + 1),
            (start_loc[0] + 1, start_loc[1]),
            (start_loc[0], start_loc[1] - 1),
            (start_loc[0] - 1, start_loc[1]),
        ]:
            if self.is_open_square(*point):
                visited = self.determine_all_reachable_squares(
                    point, num_steps + 1, visited
                )

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

    def find_all_paths(self, start_loc, target_loc, depth=0, path=None, visited=None):
        if not path:
            path = []

        if not visited:
            visited = {}

        if start_loc in visited and visited[start_loc] < depth:
            return []
        else:
            visited[start_loc] = depth

        if start_loc == target_loc:
            return [path]

        startx, starty = start_loc
        paths = []
        found_paths = []
        for point in generate_potential_next_steps(start_loc, target_loc):
            if point in path:
                continue
            elif self.is_open_square(*point) and (
                not found_paths or depth <= min(len(fp) for fp in found_paths)
            ):
                newpath = copy(path)
                newpath.append(point)
                found_paths = self.find_all_paths(
                    point, target_loc, depth + 1, newpath, visited
                )
                paths += found_paths
            else:
                continue
        return paths


def generate_potential_next_steps(start_loc, end_loc):
    if start_loc == end_loc:
        return []
    x_direction = (
        0
        if start_loc[0] == end_loc[0]
        else (end_loc[0] - start_loc[0]) / abs(end_loc[0] - start_loc[0])
    )
    y_direction = (
        0
        if start_loc[1] == end_loc[1]
        else (end_loc[1] - start_loc[1]) / abs(end_loc[1] - start_loc[1])
    )
    if x_direction == 0:
        next_steps = [
            (start_loc[0], start_loc[1] + y_direction),
            (start_loc[0], start_loc[1] - y_direction),
            (start_loc[0] + 1, start_loc[1]),
            (start_loc[0] - 1, start_loc[1]),
        ]
    elif y_direction == 0:
        next_steps = [
            (start_loc[0] + x_direction, start_loc[1]),
            (start_loc[0] - x_direction, start_loc[1]),
            (start_loc[0], start_loc[1] + 1),
            (start_loc[0], start_loc[1] - 1),
        ]
    elif abs(end_loc[0] - start_loc[0]) < abs(end_loc[1] - end_loc[1]):
        next_steps = [
            (start_loc[0] + x_direction, start_loc[1]),
            (start_loc[0] - x_direction, start_loc[1]),
            (start_loc[0], start_loc[1] + y_direction),
            (start_loc[0], start_loc[1] - y_direction),
        ]
    else:
        next_steps = [
            (start_loc[0], start_loc[1] + y_direction),
            (start_loc[0], start_loc[1] - y_direction),
            (start_loc[0] + x_direction, start_loc[1]),
            (start_loc[0] - x_direction, start_loc[1]),
        ]

    return next_steps


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
                cave.goblins.append(Goblin(x, y, cave))
            elif char == 'E':
                cave.floors.add((x, y))
                cave.elves.append(Elf(x, y, cave))

    return cave


def calculate_cave_outcome(cave, completed_rounds):
    winning_team = cave.goblins if any(g.hp > 0 for g in cave.goblins) else cave.elves
    remaining_hp = sum(wt.hp for wt in winning_team)
    answer = remaining_hp * completed_rounds
    return answer


def run_cave_game(cave, **kwargs):
    completed_rounds = 0
    num_elves = len(cave.elves)
    while any(elf.alive for elf in cave.elves) and any(
        goblin.alive for goblin in cave.goblins
    ):
        if (
            'abort_on_elf_death' in kwargs
            and kwargs['abort_on_elf_death']
            and len(cave.elves) != num_elves
        ):
            print('elf died, aborting')
            return -1

        print(f'After {completed_rounds} rounds:')
        print(cave)
        completed = cave.tick()
        if completed:
            completed_rounds += 1

    print(f'After {completed_rounds} rounds:')
    print(cave)

    return calculate_cave_outcome(cave, completed_rounds)


if __name__ == '__main__':
    cave = parse_cave_input('data/input15.txt')
    outcome = run_cave_game(cave)
    print(outcome)
