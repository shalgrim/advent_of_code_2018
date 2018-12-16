import logging
import sys
from collections import defaultdict
from logging import StreamHandler

from day16_1 import get_possible_opcodes, parse_input_16_1

logger = logging.getLogger('advent_of_code.2018.day16_2')
logging.basicConfig(
    filename='day16_2.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


def parse_input_16_2(filename):
    with open(filename) as f:
        text = f.read()

    samples_end = text.index('\n' * 4)
    program = text[samples_end + 4:]
    program_lines = program.split('\n')
    instructions = [[int(i) for i in pl.split()] for pl in program_lines if pl.strip()]

    return instructions


def determine_opcode_numbers(samples):
    possible_opcodes = defaultdict(set)

    for sample in samples:
        opcode_number = sample.instruction[0]
        possible_opcodes[opcode_number].update(get_possible_opcodes(sample))

    while any(len(v) > 1 for v in possible_opcodes.values()):
        determined_opcodes = {list(v)[0] for k, v in possible_opcodes.items() if len(v) == 1}

        for po_set in possible_opcodes.values():
            if len(po_set) == 1:
                continue
            for do in determined_opcodes:
                po_set.discard(do)

    return [list(v)[0] for k, v in sorted(possible_opcodes.items())]


def run_program(instructions, ordered_opcodes):
    registers = [0] * 4

    for instruction in instructions:
        opcode_index = instruction[0]
        registers = ordered_opcodes[opcode_index](registers, *instruction[1:])

    return registers


def day16_2(filename):
    samples = parse_input_16_1(filename)
    ordered_opcodes = determine_opcode_numbers(samples)
    program = parse_input_16_2(filename)
    registers = run_program(program, ordered_opcodes)

    return registers[0]


if __name__ == '__main__':
    print(day16_2('data/input16.txt'))
