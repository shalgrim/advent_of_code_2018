import opcodes
import logging
import sys
from logging import StreamHandler

from day19_1 import parse_input_day19

logger = logging.getLogger('advent_of_code.2018.day19_1')
logging.basicConfig(
    filename='day19_1.log',
    level=logging.INFO,
    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger.addHandler(StreamHandler(sys.stdout))


def run_program(instructions, instruction_pointer):
    registers = [0, 1] + [0] * 4

    while 0 <= registers[instruction_pointer] < len(instructions):
        instruction = instructions[registers[instruction_pointer]]
        opcode = getattr(opcodes, instruction[0])
        # output_line = f'ip={registers[instruction_pointer]} {registers} {" ".join([str(i) for i in instruction])} '
        registers = opcode(registers, *instruction[1:])
        # output_line += str(registers)
        # logger.info(output_line)
        registers[instruction_pointer] += 1

    return registers


def main(filename):
    instruction_pointer, instructions = parse_input_day19(filename)
    registers = run_program(instructions, instruction_pointer)
    return registers[0]


if __name__ == '__main__':
    print(main('data/input19.txt'))
