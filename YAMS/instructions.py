from dataclasses import dataclass, field

@dataclass
class Instruction:
    pass


class RFormat(Instruction):
    op: int
    rs: int
    rt: int
    rd: int
    shamt: int
    funct: int


class IFormat(Instruction):
    op: int
    rs: int
    rt: int
    immediate: int


class JFormat(Instruction):
    op: int
    addr: int
