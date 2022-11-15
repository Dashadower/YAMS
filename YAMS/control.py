from dataclasses import dataclass, field
from .opcodes import op
from .instructions import Instruction, RFormat, IFormat, JFormat

@dataclass
class ControlSignalEmit:
    """
    This class is a structure in which the Instruction Decoder returns given input
    """
    RegDst: int
    ALUSrc: int
    MemtoReg: int
    RegWrite: int
    MemRead: int
    MemWrite: int
    Branch: int
    ALUOp1: int
    ALUOp0: int


class Control:
    def __init__(self):
        pass

    def decode(self, instruction: Instruction):
        if isinstance(instruction, RFormat):
            return ControlSignalEmit(RegDst=1, ALUSrc=0, MemtoReg=0, RegWrite=1, MemRead=0, MemWrite=0, Branch=0, ALUOp1=1, ALUOp0=0)