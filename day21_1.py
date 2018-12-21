import logging
import math
import sys
from copy import copy
from logging import StreamHandler

import opcodes
from day19_1 import parse_input_day19

logger = logging.getLogger('advent_of_code.2018.day21_1')
logging.basicConfig(
    filename='day21_1.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


def main21_1(program_filename):
    instruction_pointer, instructions = parse_input_day19(program_filename)

    smallest_count = math.inf
    smallest_zero_register = None

    for i in range(5):
        logger.info(f'setting initial_register to {i}')
        instruction_count = count_instructions(
            instructions, instruction_pointer, [i, 0, 0, 0, 0, 0], True
        )
        if instruction_count < smallest_count:
            smallest_count = instruction_count
            smallest_zero_register = i

    print(f'answer: {i}')


def count_instructions(
    instructions, instruction_pointer, initial_registers, verbose=False
):
    registers = copy(initial_registers)
    instructions_executed = 0

    while 0 <= registers[instruction_pointer] < len(instructions):
        instruction = instructions[registers[instruction_pointer]]
        opcode = getattr(opcodes, instruction[0])
        if verbose and registers[instruction_pointer] == 28:
            output_line = f'ip={registers[instruction_pointer]} {registers} {" ".join([str(i) for i in instruction])} '
        registers = opcode(registers, *instruction[1:])
        instructions_executed += 1
        if verbose and registers[instruction_pointer] == 28:
            output_line += str(registers)
            logger.info(output_line)
        registers[instruction_pointer] += 1

    return instructions_executed


if __name__ == '__main__':
    main21_1('data/input21.txt')
