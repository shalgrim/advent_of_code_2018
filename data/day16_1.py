from opcodes import (
    addi,
    addr,
    bani,
    banr,
    bori,
    borr,
    eqir,
    eqri,
    eqrr,
    gtir,
    gtri,
    gtrr,
    muli,
    mulr,
    seti,
    setr,
)


class Sample(object):
    def __init__(self, before_registers, instruction, after_registers):
        self.before = before_registers
        self.instruction = instruction
        self.after = after_registers

    def test_opcode(self, opcode):
        return opcode(self.before, *self.instruction[1:]) == self.after


def parse_input_16_1(filename):
    with open(filename) as f:
        lines = f.readlines()

    samples = []

    for i in range(0, len(lines), 4):
        if not lines[i].startswith('Before:'):
            break
        before_registers = eval(lines[i].split(' ', 1)[1])
        instruction = [int(n) for n in lines[i + 1].split()]
        after_registers = eval(lines[i + 2].split(' ', 1)[1])
        samples.append(Sample(before_registers, instruction, after_registers))

    return samples


def get_possible_opcodes(sample):
    answer = 0

    return answer


def day16_1(filename):
    samples = parse_input_16_1(filename)
    possible_opcodes = [get_possible_opcodes(sample) for sample in samples]
    return len([po for po in possible_opcodes if len(po) >= 3])


if __name__ == '__main__':
    print(day16_1('data/input16.txt'))
