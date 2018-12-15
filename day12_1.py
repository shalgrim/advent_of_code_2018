import logging
import sys
from collections import defaultdict
from functools import lru_cache
from logging import StreamHandler

from tqdm import tqdm

logger = logging.getLogger('advent_of_code.2018.day12_1')
logging.basicConfig(
    filename='day12_1.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


def parse_pot_string(line):
    return ''.join(['1' if c == '#' else '0' for c in line])
    # return [True if c == '#' else False for c in line]


# @lru_cache(maxsize=32)
# def lhs_as_binary(five_pots):
#     return int(''.join(['1' if pot else '0' for pot in five_pots]), 2)


class State(object):
    def __init__(self, initial_state_line):
        self.pots = parse_pot_string(initial_state_line)
        self.zero_index = 0

    def apply_rules(self, rules):
        buffered_pots = '0' * 5 + self.pots + '0' * 5
        buffered_zero_index = self.zero_index + 3
        matching_rules = (
            [None, None]
            + [
                rules.rule_dict[buffered_pots[i : i + 5]]
                for i in range(2, len(buffered_pots) - 2)
            ]
            + [None, None]
        )
        new_state_buffered = ''.join(
            [rule.rhs if rule else '0' for i, rule in enumerate(matching_rules)]
        )

        leftmost_plant_index = new_state_buffered.index('1')
        rightmost_plant_index = new_state_buffered.rindex('1')
        new_state = new_state_buffered[leftmost_plant_index : rightmost_plant_index + 1]
        self.pots = new_state
        self.zero_index = buffered_zero_index - leftmost_plant_index

    def sum_planty_pot_numbers(self):
        return sum(
            [i - self.zero_index for i, pot in enumerate(self.pots) if pot == '1']
        )

    def __str__(self):
        return ''.join(['#' if pot == '1' else '.' for pot in self.pots])


class Rule(object):
    def __init__(self, rule_line):
        lhs, rhs = [side.strip() for side in rule_line.split('=>')]
        self.lhs = parse_pot_string(lhs)
        self.rhs = '1' if rhs == '#' else '0'


class RuleDuck(object):
    def __init__(self):
        self.lhs = None
        self.rhs = '0'


class RuleSet(object):
    def __init__(self, rules_lines):
        self.rules = [Rule(line) for line in rules_lines]
        self.rule_dict = defaultdict(lambda: RuleDuck())
        for rule in self.rules:
            self.rule_dict[rule.lhs] = rule


def parse_input(fn):
    with open(fn) as f:
        lines = f.readlines()

    state = State(lines[0].split(':')[1].strip())
    rules = RuleSet([line.strip() for line in lines[2:]])
    return state, rules


def main(input_file, num_ticks):
    state, rules = parse_input(input_file)
    num_ticks = int(num_ticks)
    visited_states = set([f'{state}{state.zero_index}'])

    for tick in tqdm(range(num_ticks)):
        state.apply_rules(rules)
        this_state = f'{state}{state.zero_index}'
        if this_state in visited_states:
            print(f'we revisited {state} with zero_index {state.zero_index} after tick {tick}')
        else:
            visited_states.add(this_state)

    print(f'{tick+1:>2}: {state}')
    print(f'zero_index: {state.zero_index}')
    print(f'sum of pot numbers with plants: {state.sum_planty_pot_numbers()}')


if __name__ == '__main__':
    main(*sys.argv[1:])
