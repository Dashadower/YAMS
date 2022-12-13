from dataclasses import dataclass, field
from typing import Dict, List, TYPE_CHECKING
from .opcodes import instruction2opcode_funct, op, op0_funct
from .utils import string_numeric_to_decimal, decimal2bin, zero_extend_binary, int_to_signed_bits
import re

if TYPE_CHECKING:
    from .parser import TextSegment, TextEntry

@dataclass
class Instruction:
    opcode: int
    funct: int
    name: str = field(default="nop", init=False)
    original_instruction: str = field(default="nop", init=False)

    def __post_init__(self):
        self.name = self.get_instruction_name()

    def to_binary(self) -> str:
        raise NotImplementedError()

    def get_instruction_name(self) -> str:
        op_index = op[self.opcode]
        if isinstance(op_index, str):
            return op_index

        assert self.opcode == 0, "For funct field evaluation, opcode must be zero"
        return op0_funct[self.funct]

    def get_opcode(self) -> int:
        return self.opcode

    def get_rs(self) -> int:
        rs = self.to_binary()[6:11]
        return int(rs, 2)

    def get_rt(self) -> int:
        rt = self.to_binary()[11:16]
        return int(rt, 2)

    def get_rd(self) -> int:
        rd = self.to_binary()[16:21]
        return int(rd, 2)

@dataclass
class RFormat(Instruction):
    rs: int
    rt: int
    rd: int
    shamt: int

    def to_binary(self) -> str:
        return (zero_extend_binary(decimal2bin(self.opcode), 6) +
        zero_extend_binary(decimal2bin(self.rs), 5) +
        zero_extend_binary(decimal2bin(self.rt), 5) +
        zero_extend_binary(decimal2bin(self.rd), 5) +
        zero_extend_binary(decimal2bin(self.shamt), 5) +
        zero_extend_binary(decimal2bin(self.funct), 6))


@dataclass
class IFormat(Instruction):
    rs: int
    rt: int
    immediate: int

    def to_binary(self) -> str:
        is_logical_instruction = self.get_instruction_name() in ("andi", "ori")
        return (zero_extend_binary(decimal2bin(self.opcode), 6) +
                zero_extend_binary(decimal2bin(self.rs), 5) +
                zero_extend_binary(decimal2bin(self.rt), 5) +
                (zero_extend_binary(decimal2bin(self.immediate), 16) if is_logical_instruction else int_to_signed_bits(self.immediate, 16)))


@dataclass
class JFormat(Instruction):
    addr: int

    def to_binary(self) -> str:
        return (zero_extend_binary(decimal2bin(self.opcode), 6) +
                zero_extend_binary(decimal2bin(self.addr), 26))


@dataclass
class SpecialFormat(Instruction):
    def to_binary(self) -> str:
        return "0" * 32


class InstructionMemoryHandler:
    def __init__(self):
        self.starting_addr: int = 0
        self._instruction_memory: Dict[int, Instruction] = {}

        # These patterns are used to match offset syntax in certain iformat instructions (lw, sw, etc)
        # For example, lw $2, 3($4)
        # iformat_offset_pattern will match '3'
        # iformat_offset_rs_register_pattern will match '4'
        self.iformat_offset_pattern = re.compile(r"(-?[\dx]+)(?=\()")
        self.iformat_offset_rs_register_pattern = re.compile(r"(?!\(\$)\d+(?=\))")

    def load_instructions(self, text_segment: "TextSegment"):
        self.starting_addr = text_segment.starting_address
        current_addr = self.starting_addr
        for entry in text_segment.iter_entries():
            self._instruction_memory[current_addr] = self._create_instruction(entry)
            current_addr += 4

    def _create_instruction(self, entry: "TextEntry"):
        opcode, funct = instruction2opcode_funct[entry.instruction]
        if entry.instruction in rformat_instructions:
            # Rformat: instruction rd, rs, rt
            if entry.instruction == "sll":
                # sll rs register always defaults to 0
                rd = int(entry.arguments[0][1:])
                rt = int(entry.arguments[1][1:])
                rs = 0
                shamt = string_numeric_to_decimal(entry.arguments[2])
            else:
                rd, rs, rt = [int(arg[1:]) for arg in entry.arguments]
                shamt = 0
            ret = RFormat(opcode=opcode, rs=rs, rt=rt, rd=rd, shamt=shamt, funct=funct)

        elif entry.instruction in iformat_instructions:
            # IFormat: instruction rt, rs, imm
            if entry.instruction in offset_iformat_instructions:
                # These are instructions of the format `lw rt, offset(rs)`
                rt = int(entry.arguments[0][1:])

                # parse out offset($rs) format
                immediate = string_numeric_to_decimal(self.iformat_offset_pattern.findall(entry.arguments[1])[0])
                rs = int(self.iformat_offset_rs_register_pattern.findall(entry.arguments[1])[0])
            elif entry.instruction == "lui":
                # rs source register of lui is always zero
                rs = 0
                rt = int(entry.arguments[0][1:])
                immediate = string_numeric_to_decimal(entry.arguments[1])
            elif entry.instruction == "beq":
                # beq has the syntax beq rs, rt, label
                rs = int(entry.arguments[0][1:])
                rt = int(entry.arguments[1][1:])
                immediate = string_numeric_to_decimal(entry.arguments[2])
            else:
                rt = int(entry.arguments[0][1:])
                rs = int(entry.arguments[1][1:])
                immediate = string_numeric_to_decimal(entry.arguments[2])

            ret = IFormat(opcode=opcode, funct=funct, rs=rs, rt=rt, immediate=immediate)

        elif entry.instruction in jformat_instructions:
            # Jformat: instruction imm
            addr = string_numeric_to_decimal(entry.arguments[0])
            ret = JFormat(opcode=opcode, funct=funct, addr=addr)

        elif entry.instruction in special_format_instructions:
            ret = SpecialFormat(opcode=opcode, funct=funct)

        else:
            raise Exception(f"Failed to parse {entry.original_text}: Unknown instruction {entry.instruction}")

        ret.original_instruction = entry.original_text
        return ret


    def fetch_instruction(self, addr: int) -> Instruction:
        try:
            return self._instruction_memory[addr]
        except KeyError:
            return SpecialFormat(0, 0)

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

# These are iformat instructions that allow offset syntax
# eg: lw $4, 4($2)
offset_iformat_instructions = [
    "lbu",
    "lhu",
    "ll",
    "lw",
    "sb",
    "sc",
    "sh",
    "sw",
]

jformat_instructions = [
    "j",
    "jal",
]

special_format_instructions = [
    "syscall"
]