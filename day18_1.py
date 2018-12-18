from copy import copy

from tqdm import tqdm

OPEN_ACRE = '.'
WOODED_ACRE = '|'
LUMBERYARD = '#'


def tick_acre(acre_type, adjacent_acres):
    if acre_type == OPEN_ACRE:
        answer = (
            WOODED_ACRE
            if len([a for a in adjacent_acres if a == WOODED_ACRE]) >= 3
            else OPEN_ACRE
        )
    elif acre_type == WOODED_ACRE:
        answer = (
            LUMBERYARD
            if len([a for a in adjacent_acres if a == LUMBERYARD]) >= 3
            else WOODED_ACRE
        )
    elif acre_type == LUMBERYARD:
        answer = (
            LUMBERYARD
            if any(a == LUMBERYARD for a in adjacent_acres)
            and any(a == WOODED_ACRE for a in adjacent_acres)
            else OPEN_ACRE
        )
    return answer


class Area(object):
    def __init__(self, acres):
        self.acres = acres

    @property
    def num_lumberyards(self):
        return len([a for a in self.acres.values() if a == LUMBERYARD])

    @property
    def num_wooded(self):
        return len([a for a in self.acres.values() if a == WOODED_ACRE])

    @property
    def value(self):
        return self.num_lumberyards * self.num_wooded

    @property
    def height(self):
        return max(k[1] for k in self.acres.keys()) + 1

    @property
    def width(self):
        return max(k[0] for k in self.acres.keys()) + 1

    def __str__(self):
        lines = []
        for y in range(self.height):
            lines.append(''.join([self.acres[(x, y)] for x in range(self.width)]))
        return '\n'.join(lines)

    def get_adjacent_acre_values(self, x, y):
        answer = []
        for new_x in range(max(0, x - 1), min(x + 2, self.width)):
            for new_y in range(max(0, y - 1), min(y + 2, self.height)):
                if x == new_x and y == new_y:
                    continue
                answer.append(self.acres[(new_x, new_y)])
        return answer

    def tick(self):
        new_acres = copy(self.acres)

        for key in new_acres:
            adjacent = self.get_adjacent_acre_values(*key)
            new_acres[key] = tick_acre(self.acres[key], adjacent)

        self.acres = new_acres


def create_area_from_file(filename):
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
    return Area(
        {(x, y): char for y, line in enumerate(lines) for x, char in enumerate(line)}
    )


def calc_resource_value(filename, minutes, show_maps=True):
    area = create_area_from_file(filename)
    seen = set()
    seen.add(area.acres)

    for i in tqdm(range(minutes)):
        if i % 10 == 0:
            print(f'{i:>15d}: {area.value}')
        if show_maps:
            print(f'{area}\n\n\n')
        area.tick()

    print(area)
    return area.value


if __name__ == '__main__':
    print(calc_resource_value('data/input18.txt', 10))
