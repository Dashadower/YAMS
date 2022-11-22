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
    IDFlush: int


class Control:
    def __init__(self):
        self.RegDst: int = 0
        self.ALUSrc: int = 0
        self.MemtoReg: int = 0
        self.RegWrite: int = 0
        self.MemRead: int = 0
        self.MemWrite: int = 0
        self.Jump: int = 0
        self.Branch: int = 0
        self.ALUOp1: int = 0
        self.ALUOp0: int = 0
        self.IDFlush: int = 0

    def reset_signals(self):
        self.RegDst = 0
        self.ALUSrc = 0
        self.MemtoReg = 0
        self.RegWrite = 0
        self.MemRead = 0
        self.MemWrite = 0
        self.Jump = 0
        self.Branch = 0
        self.ALUOp1 = 0
        self.ALUOp0 = 0
        self.IDFlush = 0

    def decode(self, instruction: Instruction):
        if isinstance(instruction, RFormat):
            funct_field = instruction.funct