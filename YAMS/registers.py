from dataclasses import dataclass
from typing import List


class MainRegister:
    def __init__(self):
        self._register = [0] * 32

    def _write(self, register_index, value):
        """
        Internal method to write a value to a given register index. May only be called on rising edge.
        """
        self._register = value

    def _read(self, register_index):
        return self._register[register_index]


class IFIDRegister:
    def __init__(self):
        self.pc = None
        self.operation = None


class IDEXREgister:
    def __init__(self):
        self.control_wb = None
        self.control_m = None
        self.control_ex = None
        self.pc = None
        self.read_data1 = None
        self.read_data2 = None
        self.immediate = None


class EXMEMRegister:
    def __init__(self):
        self.control_wb = None
        self.control_m = None
        self.pc = None
        self.alu_zero = None
        self.alu_result = None
        self.read_data2 = None


class MEMWBRegister:
    def __init__(self):
        self.control_wb = None
        self.memory_read_data = None
        self.alu_result = None
        self.writeback_reg_dst = None
