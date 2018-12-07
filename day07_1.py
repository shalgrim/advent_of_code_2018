import logging
import re
import sys
from collections import defaultdict
from logging import StreamHandler

logger = logging.getLogger('advent_of_code.2018.day07_1')
logging.basicConfig(
    filename='day07_1.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))

INPUT_PATTERN = re.compile(r'^Step (.) must be finished before step (.) can begin\.\n$')


def parse_lines(lines):
    tuples = [INPUT_PATTERN.match(line).groups() for line in lines]
    return tuples


def main(lines):
    data = parse_lines(lines)
    steps_to_do = set(d[0] for d in data).union(set(d[1] for d in data))

    predecessors = defaultdict(set)
    for datum in data:
        predecessors[datum[1]].add(datum[0])

    steps_done = []

    while steps_to_do:
        possible_next_steps = set(
            s for s in steps_to_do if s not in predecessors or not predecessors[s]
        )
        next_step = min(possible_next_steps)
        steps_done.append(next_step)

        for v in predecessors.values():
            if next_step in v:
                v.remove(next_step)

        steps_to_do.remove(next_step)

    print(''.join(steps_done))


if __name__ == '__main__':
    with open('data/input07.txt') as f:
        lines = f.readlines()

    main(lines)
