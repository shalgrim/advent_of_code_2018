import opcodes
import logging
import sys
from logging import StreamHandler

from day19_1 import parse_input_day19

logger = logging.getLogger('advent_of_code.2018.day19_2')
logging.basicConfig(
    filename='day19_2.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


def run_program(instructions, instruction_pointer, starting_registers=None):
    if not starting_registers:
        registers = [1] + [0] * 5
    else:
        registers = starting_registers

    digit = False
    while 0 <= registers[instruction_pointer] < len(instructions):
        instruction = instructions[registers[instruction_pointer]]
        opcode = getattr(opcodes, instruction[0])
        if registers[instruction_pointer] == 13:
            output_line = f'ip={registers[instruction_pointer]} {registers} {" ".join([str(i) for i in instruction])} '
            digit = True
        registers = opcode(registers, *instruction[1:])
        if digit:
            output_line += str(registers)
            logger.info(output_line)
            digit = False
        registers[instruction_pointer] += 1

    return registers


def main(filename):
    instruction_pointer, instructions = parse_input_day19(filename)
    starting_registers = [6, 10551289, 13, 10551288, 4, 1]
    # registers = run_program(instructions, instruction_pointer, starting_registers)
    registers = run_program(instructions, instruction_pointer)
    return registers[0]


if __name__ == '__main__':
    print(main('data/input19.txt'))
    # 2280 is too low
    # 55664833953828 is too high
    # 55664844505116 is also too high obviously but i guessed it anyway
