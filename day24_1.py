import re

UNIT_LINE = (
    r'^(?P<num_units>\d+) units each with (?P<hit_points>\d+) hit points (?P<weak_immune>\(.+\) )?with an attack '
    r'that does (?P<damage_amount>\d+) (?P<damage_type>\S+) damage at initiative (?P<initiative>\d+)$'
)
UNIT_PATT = re.compile(UNIT_LINE)


class Group(object):
    def __init__(self, unit, number):
        self.unit = unit
        self.number = number

class Unit(object):
    def __init__(self, hit_points, damage_amount, damage_type, initiative, weaknesses=None, immunities=None):
        self.hp = hit_points
        self.damage_amount = damage_amount
        self.damage_type = damage_type
        self.initiative = initiative
        self.weaknesses = weaknesses if weaknesses else []
        self.immunities = immunities if immunities else []


class Army(object):
    def __init__(self):
        self.groups = []


def parse_weak_immune(parenthetical):
    content = parenthetical.strip()[1:-1]
    if content.startswith('weak to '):
        semicolon = content.find(';')
        if semicolon > 0:
            weak_content = content[8:semicolon]
            immune_content = content[semicolon+12:]
        else:
            weak_content = content[8:]
            immune_content = None
    elif content.startswith('immune to'):
        semicolon = content.find(';')
        if semicolon > 0:
            immune_content = content[10:semicolon]
            weak_content = content[semicolon + 10:]
        else:
            immune_content = content[10:]
            weak_content = None
    else:
        raise Exception(f'unexpected input {parenthetical}')

    weaknesses = weak_content.split(',') if weak_content else []
    immunities = immune_content.split(',') if immune_content else []
    return weaknesses, immunities


def parse_input_24(filename):
    with open(filename) as f:
        lines = f.readlines()

    armies = {}

    for line in lines:
        match = UNIT_PATT.match(line.strip())
        if match:
            hp = int(match.group('hit_points'))
            damage = match.group('damage_amount')
            damage_type = match.group('damage_type')
            initiative = int(match.group('initiative'))
            weak, immune = parse_weak_immune(match.group('weak_immune'))
            unit = Unit(hp, damage, damage_type, initiative)
            army.groups.append(Group(unit, int(match.group('num_units'))))
        elif line.strip() == 'Immune System:':
            army = Army()
            armies['immune_system'] = army
        elif line.strip() == 'Infection:':
            army = Army()
            armies['infection'] = army
        elif not line.strip():
            pass
        else:
            raise Exception(f'unrecognized line: {line}')


def day24_1(filename):
    armies = parse_input_24(filename)


if __name__ == '__main__':
    day24_1('data/input24.txt')
