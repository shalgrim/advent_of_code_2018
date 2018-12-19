import opcodes


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

    while registers[0] <= len(instructions):
        instruction = (
            registers[0] - 1
        )  # the first instruction is number one at index zero
        opcode = getattr(opcodes, instruction[0])
        registers = opcode(registers, *instruction[1:4])
        registers[0] += 1

    return registers


def main(filename):
    instruction_pointer, instructions = parse_input_day19('data/input19.txt')
    registers = run_program(instructions, instruction_pointer)
    return registers[0]


if __name__ == '__main__':
    print(main('data/input19.txt'))
