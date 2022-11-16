from dataclasses import dataclass, field

@dataclass
class Instruction:
    instruction: str


@dataclass
class RFormat(Instruction):
    rs: str
    rt: str
    rd: str
    shamt: str


@dataclass
class IFormat(Instruction):
    rs: str
    rt: str
    immediate: str


@dataclass
class JFormat(Instruction):
    addr: str


rformat_instructions = [
    "add",
    "addu",
    "and",
    "jr",
    "nor",
    "or",
    "slt",
    "sltu",
    "sll",
    "srl",
    "sub",
    "subu",
    "div",
    "divu",
    "mult",
    "multu"
]

iformat_instructions = [
    "addi",
    "addiu",
    "andi",
    "beq",
    "bne",
    "lbu",
    "lhu",
    "ll",
    "lui",
    "lw",
    "ori",
    "slti",
    "sltiu",
    "sb",
    "sc",
    "sh",
    "sw",
]

jformat_instructions = [
    "j",
    "jal",
]