import logging
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
    prev_halter = None
    halters = set()
    ctr = 0

    while 0 <= registers[instruction_pointer] < len(instructions):
        instruction = instructions[registers[instruction_pointer]]
        opcode = getattr(opcodes, instruction[0])
        registers = opcode(registers, *instruction[1:])
        if registers[instruction_pointer] == 28:  # and registers[1] < 10345242:
            if ctr % 10 == 0:
                print(ctr)
            ctr += 1
            # print(registers[1])
            if registers[1] in halters:
                print(prev_halter)
                break
            prev_halter = registers[1]
            halters.add(registers[1])

        registers[instruction_pointer] += 1
    print('ending')


if __name__ == '__main__':
    main21_1('data/input21.txt')
    # 7282971 is incorrect =(
    # 16485525 is too high
    # 10345242 is too high
    # so it has to be somewhere 10_345_242
    # 438 is incorrect
