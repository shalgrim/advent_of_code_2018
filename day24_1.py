import re

UNIT_LINE = (
    r'^(?P<num_units>\d+) units each with (?P<hit_points>\d+) hit points (?P<weak_immune>\(.+\) )?with an attack '
    r'that does (?P<damage_amount>\d+) (?P<damage_type>\S+) damage at initiative (?P<initiative>\d+)$'
)
UNIT_PATT = re.compile(UNIT_LINE)


class Group(object):
    def __init__(self, unit, number, army):
        self.unit = unit
        self.number = number
        self.army = army
        self.selected_attack_group = None
        self.selected_to_be_attacked = False

    @property
    def effective_power(self):
        return self.number * self.unit.damage_amount

    def calculate_damage(self, opposing_group):
        if self.unit.damage_type in opposing_group.unit.immunities:
            answer = 0
        elif self.unit.damage_type in opposing_group.unit.weaknesses:
            answer = 2 * self.effective_power
        else:
            answer = self.effective_power
        return answer

    def select_group_to_attack(self, *groups):
        highest_damage = 0
        group_to_attack = None

        for group in groups:
            damage = self.calculate_damage(group)
            if damage > highest_damage:
                highest_damage = damage
                group_to_attack = group

        if group_to_attack:
            self.selected_attack_group = group_to_attack
            group_to_attack.selected_to_be_attacked = True

    def attack(self):
        if not self.selected_attack_group:
            return
        damage = self.calculate_damage(self.selected_attack_group)
        self.selected_attack_group.deal_damage(damage)

    def deal_damage(self, amount):
        units_to_lose = amount // self.unit.hp
        self.number = max(0, self.number - units_to_lose)

    @property
    def initiative(self):
        return self.unit.initiative


class Unit(object):
    def __init__(
        self,
        hit_points,
        damage_amount,
        damage_type,
        initiative,
        weaknesses=None,
        immunities=None,
    ):
        self.hp = hit_points
        self.damage_amount = damage_amount
        self.damage_type = damage_type
        self.initiative = initiative
        self.weaknesses = weaknesses if weaknesses else []
        self.immunities = immunities if immunities else []


class Army(object):
    def __init__(self):
        self.groups = []

    def select_groups_to_attack(self, opposing_army):
        for group in self.groups:
            group.select_group_to_attack(*opposing_army.groups)

    @property
    def has_units(self):
        return any(group.number > 0 for group in self.groups)


def parse_weak_immune(parenthetical):
    if not parenthetical:
        return [], []
    content = parenthetical.strip()[1:-1]
    if content.startswith('weak to '):
        semicolon = content.find(';')
        if semicolon > 0:
            weak_content = content[8:semicolon]
            immune_content = content[semicolon + 12 :]
        else:
            weak_content = content[8:]
            immune_content = None
    elif content.startswith('immune to'):
        semicolon = content.find(';')
        if semicolon > 0:
            immune_content = content[10:semicolon]
            weak_content = content[semicolon + 10 :]
        else:
            immune_content = content[10:]
            weak_content = None
    else:
        raise Exception(f'unexpected input {parenthetical}')

    weaknesses = [wc.strip() for wc in weak_content.split(',')] if weak_content else []
    immunities = [ic.strip() for ic in immune_content.split(',')] if immune_content else []
    return weaknesses, immunities


def parse_input_24(filename):
    with open(filename) as f:
        lines = f.readlines()

    armies = {}

    for line in lines:
        match = UNIT_PATT.match(line.strip())
        if match:
            hp = int(match.group('hit_points'))
            damage = int(match.group('damage_amount'))
            damage_type = match.group('damage_type')
            initiative = int(match.group('initiative'))
            weak, immune = parse_weak_immune(match.group('weak_immune'))
            unit = Unit(hp, damage, damage_type, initiative, weak, immune)
            army.groups.append(Group(unit, int(match.group('num_units')), army))
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
    return armies


def army_attack(army1, army2):
    attacking_groups = sorted(
        army1.groups + army2.groups, key=lambda x: x.initiative, reverse=True
    )
    for ag in attacking_groups:
        ag.attack()


def army_target_selection(army1, army2):
    all_groups = army1.groups + army2.groups
    second_key_sorted = sorted(all_groups, key=lambda x: x.initiative, reverse=True)
    sorted_groups = sorted(second_key_sorted, key=lambda x: x.effective_power, reverse=True)
    for sg in sorted_groups:
        sg.select_group_to_attack(
            *[
                g
                for g in all_groups
                if g.army is not sg.army and g.number > 0 and not g.selected_to_be_attacked
            ]
        )


def day24_1(filename):
    armies = parse_input_24(filename)
    army_immune = armies['immune_system']
    army_infection = armies['infection']

    while army_immune.has_units and army_infection.has_units:
        army_target_selection(army_immune, army_infection)
        army_attack(army_immune, army_infection)
        for group in army_immune.groups + army_infection.groups:
            group.selected_attack_group = None
            group.selected_to_be_attacked = False

    winning_army = [a for a in armies.values() if a.has_units][0]
    num_remaining_units = sum(g.number for g in winning_army.groups)
    return num_remaining_units


if __name__ == '__main__':
    print(f'answer: {day24_1("data/input24.txt")}')
    # 9684 is too low
    # my next best guess is something is wrong with my parsing or my sorting so let's look at everything that gets
    # parsed first then maybe consider some tricky sorts
