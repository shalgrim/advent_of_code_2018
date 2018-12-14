import sys


def parse_pot_string(line):
    return [True if c == '#' else False for c in line]


class State(object):
    def __init__(self, initial_state_line):
        self.pots = parse_pot_string(initial_state_line)
        self.zero_index = 0

    def apply_rules(self, rules):
        buffered_pots = [False] * 5 + self.pots + [False] * 5
        buffered_zero_index = self.zero_index + 5
        matching_rules = [
            rules.find_match(buffered_pots, i) for i in range(len(buffered_pots))
        ]
        new_state_buffered = [
            rule.rhs if rule else False for i, rule in enumerate(matching_rules)
        ]

        leftmost_plant_index = new_state_buffered.index(True)
        rightmost_plant_index = (
            len(new_state_buffered)
            - 1
            - sorted(new_state_buffered, reverse=True).index(True)
        )
        new_state = new_state_buffered[leftmost_plant_index : rightmost_plant_index + 1]
        self.pots = new_state
        self.zero_index = buffered_zero_index - leftmost_plant_index

    def sum_planty_pot_numbers(self):
        return sum([i - self.zero_index for i, pot in enumerate(self.pots) if pot])

    def __str__(self):
        return ''.join(['#' if pot else '.' for pot in self.pots])


class Rule(object):
    def __init__(self, rule_line):
        lhs, rhs = [side.strip() for side in rule_line.split('=>')]
        self.lhs = parse_pot_string(lhs)
        self.rhs = True if rhs == '#' else False


class RuleSet(object):
    def __init__(self, rules_lines):
        self.rules = [Rule(line) for line in rules_lines]

    def find_match(self, pots, pot_index):
        pot_context = pots[pot_index - 2 : pot_index + 3]

        for rule in self.rules:
            if rule.lhs == pot_context:
                return rule
        return None


def parse_input(fn):
    with open(fn) as f:
        lines = f.readlines()

    state = State(lines[0].split(':')[1].strip())
    rules = RuleSet([line.strip() for line in lines[2:]])
    return state, rules


def main(input_file, num_ticks):
    state, rules = parse_input(input_file)
    num_ticks = int(num_ticks)

    for tick in range(num_ticks):
        print(f'{tick:>2}: {state}')
        state.apply_rules(rules)

    print(f'{tick:>2}: {state}')
    print(f'zero_index: {state.zero_index}')
    print(f'sum of pot numbers with plants: {state.sum_planty_pot_numbers()}')


if __name__ == '__main__':
    main(*sys.argv[1:])
