from copy import copy


def addr(registers, A, B, C):
    output = copy(registers)
    return output


def addi(registers, A, B, C):
    output = copy(registers)
    output[registers[C]] = registers[A] + B
    return output


def mulr(registers, A, B, C):
    output = copy(registers)
    output[registers[C]] = registers[A] * registers[B]
    return output


def muli(registers, A, B, C):
    output = copy(registers)
    return output


def banr(registers, A, B, C):
    output = copy(registers)
    return output


def bani(registers, A, B, C):
    output = copy(registers)
    return output


def borr(registers, A, B, C):
    output = copy(registers)
    return output


def bori(registers, A, B, C):
    output = copy(registers)
    return output


def setr(registers, A, B, C):
    output = copy(registers)
    return output


def seti(registers, A, B, C):
    output = copy(registers)
    output[registers[C]] = A
    return output


def gtir(registers, A, B, C):
    output = copy(registers)
    return output


def gtri(registers, A, B, C):
    output = copy(registers)
    return output


def gtrr(registers, A, B, C):
    output = copy(registers)
    return output


def eqir(registers, A, B, C):
    output = copy(registers)
    return output


def eqri(registers, A, B, C):
    output = copy(registers)
    return output


def eqrr(registers, A, B, C):
    output = copy(registers)
    return output
