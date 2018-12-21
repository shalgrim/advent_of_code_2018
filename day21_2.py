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
    run_program(instructions, instruction_pointer, [0, 0, 0, 0, 0, 0])


def run_program(instructions, instruction_pointer, initial_registers):
    registers = copy(initial_registers)
    largest_reg1 = -math.inf

    while 0 <= registers[instruction_pointer] < len(instructions):
        instruction = instructions[registers[instruction_pointer]]
        opcode = getattr(opcodes, instruction[0])
        registers = opcode(registers, *instruction[1:])
        if registers[instruction_pointer] == 28 and registers[1] > largest_reg1:
            largest_reg1 = registers[1]
            print(largest_reg1)
        registers[instruction_pointer] += 1
    print('ending')


if __name__ == '__main__':
    main21_1('data/input21.txt')
    # 16485525 is too high
    """
    so if I'm thinking about this right then left to try is
    7282971
    10345242
    16137946
    16380319
    """
