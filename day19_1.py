import opcodes
import logging
import sys
from logging import StreamHandler

logger = logging.getLogger('advent_of_code.2018.day19_1')
logger.addHandler(StreamHandler(sys.stdout))


def parse_input_day19(filename):
    with open(filename) as f:
        rawlines = f.readlines()

    instruction_pointer = int(rawlines[0].strip().split()[1])
    otherlines = [line.split('#')[0].strip() for line in rawlines[1:]]  # strip comments

    instructions = []
    for line in otherlines:
        opcode = line.split()[0]
        instructions.append([opcode] + [int(c) for c in line.strip().split()[1:]])

    return instruction_pointer, instructions


def run_program(instructions, instruction_pointer):
    registers = [0] * 6

    while 0 <= registers[instruction_pointer] < len(instructions):
        instruction = instructions[registers[instruction_pointer]]
        opcode = getattr(opcodes, instruction[0])
        output_line = f'ip={registers[instruction_pointer]} {registers} {" ".join([str(i) for i in instruction])} '
        registers = opcode(registers, *instruction[1:])
        output_line += str(registers)
        logger.info(output_line)
        registers[instruction_pointer] += 1

    return registers


def main(filename):
    instruction_pointer, instructions = parse_input_day19(filename)
    registers = run_program(instructions, instruction_pointer)
    return registers[0]


if __name__ == '__main__':
    logging.basicConfig(
        filename='day19_1.log',
        level=logging.WARNING,
        format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    print(main('data/input19.txt'))
