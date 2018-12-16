from copy import copy
from operator import and_, or_


def addr(registers, A, B, C):
    output = copy(registers)
    output[C] = registers[A] + registers[B]
    return output


def addi(registers, A, B, C):
    output = copy(registers)
    output[C] = registers[A] + B
    return output


def mulr(registers, A, B, C):
    output = copy(registers)
    output[C] = registers[A] * registers[B]
    return output


def muli(registers, A, B, C):
    output = copy(registers)
    output[C] = registers[A] * B
    return output


def banr(registers, A, B, C):
    output = copy(registers)
    output[C] = and_(registers[A], registers[B])
    return output


def bani(registers, A, B, C):
    output = copy(registers)
    output[C] = and_(registers[A], B)
    return output


def borr(registers, A, B, C):
    output = copy(registers)
    output[C] = or_(registers[A], registers[B])
    return output


def bori(registers, A, B, C):
    output = copy(registers)
    output[C] = or_(registers[A], B)
    return output


def setr(registers, A, B, C):
    output = copy(registers)
    output[C] = registers[A]
    return output


def seti(registers, A, B, C):
    output = copy(registers)
    output[C] = A
    return output


def gtir(registers, A, B, C):
    output = copy(registers)
    output[C] = int(A > registers[B])
    return output


def gtri(registers, A, B, C):
    output = copy(registers)
    output[C] = int(registers[A] > B)
    return output


def gtrr(registers, A, B, C):
    output = copy(registers)
    output[C] = int(registers[A] > registers[B])
    return output


def eqir(registers, A, B, C):
    output = copy(registers)
    output[C] = int(A == registers[B])
    return output


def eqri(registers, A, B, C):
    output = copy(registers)
    output[C] = int(registers[A] == B)
    return output


def eqrr(registers, A, B, C):
    output = copy(registers)
    output[C] = int(registers[A] == registers[B])
    return output
