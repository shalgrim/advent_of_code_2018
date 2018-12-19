import opcodes
import logging
import sys
from logging import StreamHandler

logger = logging.getLogger('advent_of_code.2018.day19_1')
logging.basicConfig(filename='day19_1.log',
                    level=logging.INFO,
                    format='%(levelname) -10s %(asctime)s %(module)s at line %(lineno)d: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S")
# logger.addHandler(StreamHandler(sys.stdout))


def parse_input_day19(filename):
    with open(filename) as f:
        lines = f.readlines()

    instruction_pointer = int(lines[0].strip().split()[1])
    instructions = []
    for line in lines[1:]:
        opcode = line.split()[0]
        instructions.append([opcode] + [int(c) for c in line.strip().split()[1:]])

    return instruction_pointer, instructions


def run_program(instructions, instruction_pointer):
    registers = [instruction_pointer] + [0] * 5

    while registers[0] < len(instructions):
        instruction = instructions[registers[0]]
        opcode = getattr(opcodes, instruction[0])
        output_line = (
            f'ip={registers[0]} {registers} {" ".join([str(i) for i in instruction])} '
        )
        registers = opcode(registers, *instruction[1:])
        output_line += str(registers)
        logger.info(output_line)
        registers[0] += 1

    return registers


def main(filename):
    instruction_pointer, instructions = parse_input_day19(filename)
    registers = run_program(instructions, instruction_pointer)
    return registers[0]


if __name__ == '__main__':
    print(main('data/input19.txt'))
