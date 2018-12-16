from unittest import TestCase

from data.day16_1 import Sample
from opcodes import seti, mulr, addi


class TestSample(TestCase):
    def setUp(self):
        self.before_registers = [3, 2, 1, 1]
        self.instruction = [9, 2, 1, 2]
        self.after_registers = [3, 2, 2, 1]
        self.sample = Sample(
            self.before_registers, self.instruction, self.after_registers
        )

    def test_addi(self):
        self.assertEqual(
            self.after_registers, addi(self.before_registers, *self.instruction[1:])
        )

    def test_mulr(self):
        self.assertEqual(
            self.after_registers, mulr(self.before_registers, *self.instruction[1:])
        )

    def test_seti(self):
        self.assertEqual(
            self.after_registers, seti(self.before_registers, *self.instruction[1:])
        )

    def test_test_opcode(self):
        self.assertTrue(self.sample.test_opcode(addi))
        self.assertTrue(self.sample.test_opcode(mulr))
        self.assertTrue(self.sample.test_opcode(seti))
