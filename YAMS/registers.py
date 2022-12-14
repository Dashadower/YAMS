from dataclasses import dataclass
from typing import List
from .pipeline_component import PipelineComponent
from .instructions import Instruction, RFormat, SpecialFormat
from .utils import zero_extend_binary, zero_extend_hex_to_word, int2_signed_32bit_int, string_numeric_to_hex, int_to_signed_bits
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pipeline import PipelineCoordinator


class MainRegister(PipelineComponent):
    def __init__(self, sp:int =0, gp: int=0):
        self._register = [0] * 32
        self._register[29] = sp
        self._register[28] = gp

        self.read_value1: int = 0
        self.read_value2: int = 0

    def _write(self, register_index, value):
        """
        Internal method to write a value to a given register index. May only be called on rising edge.
        """
        self._register[register_index] = value

    def _read(self, register_index):
        return self._register[register_index]

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.MEMWB_register.control_RegWrite == 1:
            if pipeline_c.MEMWB_register.RegisterRd == 0:
                return
            self._register[pipeline_c.MEMWB_register.RegisterRd] = pipeline_c.WB_Mem2RegMUX.value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.on_rising_edge(pipeline_c)
        self.read_value1 = self._register[pipeline_c.IFID_register.instruction.get_rs()]
        self.read_value2 = self._register[pipeline_c.IFID_register.instruction.get_rt()]

    def repr_hex(self) -> str:
        ret = ""
        for index, value in enumerate(self._register):
            ret += f"0x{index}({register_names[index]}) : {zero_extend_hex_to_word(hex(int2_signed_32bit_int(value)))}\n"

        return ret

    def repr_binary(self) -> str:
        ret = ""
        for index, value in enumerate(self._register):
            ret += f"{index:2}({register_names[index]}) : {int_to_signed_bits(value, n_bits=32)}\n"

        return ret

    def __repr__(self) -> str:
        ret = ""
        for index, value in enumerate(self._register):
            ret += f"{index:2}({register_names[index]}) : {value}\n"

        return ret

    def get_info(self) -> str:
        return ""


class IFIDRegister(PipelineComponent):
    def __init__(self):
        self.pc: int = 0
        self.instruction: Instruction = SpecialFormat(0, 0)

        self.stage_write_index: int = None
        self.continue_stage = True

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.IFIDWrite:
            self.pc = pipeline_c.IF_PC4Adder.result
            self.instruction = pipeline_c.IF_InstructionMemory.current_instruction
            self.stage_write_index = pipeline_c.IF_InstructionMemory.stage_write_index
            if pipeline_c.ID_BranchEqualAND.IFFlush == 1:
                self.instruction = RFormat(opcode=0, funct=0, rs=0, rt=0, rd=0, shamt=0)
        else:  # if IF/IDWrite is 0, keep the contents of the register
            pass

    def write_stage_data(self, pipeline_c: "PipelineCoordinator") -> None:
        self.continue_stage = True
        if self.stage_write_index is not None:
            if pipeline_c.ID_HazardDetector.IFIDWrite == 0:
                pipeline_c.stage_information[self.stage_write_index].append("stall")
                self.continue_stage = False
            elif pipeline_c.ID_BranchEqualAND.IFFlush == 1:
                pipeline_c.stage_information[self.stage_write_index].append("ID(flush)")
            else:
                pipeline_c.stage_information[self.stage_write_index].append("ID")

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def __repr__(self) -> str:
        ret = ""
        ret += f"pc : {hex(self.pc)}\n"
        ret += f"Instruction : {self.instruction}\n"
        return ret

    def get_info(self) -> str:
        ret = f"""IF/ID Register

PC: {self.pc}
Instruction: {self.instruction}
Instruction binary: {self.instruction.to_binary()}
"""
        return ret


class IDEXREgister(PipelineComponent):
    def __init__(self):
        # WB control signals
        self.control_MemtoReg: int = 0
        self.control_RegWrite: int = 0

        # MEM control signals
        self.control_Branch: int = 0
        self.control_MemRead: int = 0
        self.control_MemWrite: int = 0

        # EX control signals
        self.control_RegDst: int = 0
        self.control_ALUOp: int = 0
        self.control_ALUSrc: int = 0

        self.pc: int = 0
        self.read_data1: int = 0
        self.read_data2: int = 0
        self.immediate: str = "0"
        self.ImmediateSLL16: str = "0"

        self.RegisterRs: int = 0
        self.RegisterRt: int = 0
        self.RegisterRd: int = 0

        self.instruction: Instruction = SpecialFormat(0, 0)
        self.stage_write_index: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:

        control_out = pipeline_c.ID_ControlZeroMUX

        # WB control signals
        self.control_MemtoReg = control_out.MemtoReg
        self.control_RegWrite = control_out.RegWrite

        # MEM control signals
        self.control_Branch = control_out.Branch
        self.control_MemRead = control_out.MemRead
        self.control_MemWrite = control_out.MemWrite

        # EX control signals
        self.control_RegDst = control_out.RegDst
        self.control_ALUOp = control_out.ALUOp
        self.control_ALUSrc = control_out.ALUSrc

        self.pc = pipeline_c.IFID_register.pc
        self.read_data1 = pipeline_c.ID_MainRegister.read_value1
        self.read_data2 = pipeline_c.ID_MainRegister.read_value2

        self.immediate = pipeline_c.ID_ImmediateSignExtender.value
        self.ImmediateSLL16 = pipeline_c.ID_ImmediateSLL16.value

        self.RegisterRs = pipeline_c.IFID_register.instruction.get_rs()
        self.RegisterRt = pipeline_c.IFID_register.instruction.get_rt()
        self.RegisterRd = pipeline_c.IFID_register.instruction.get_rd()

        self.instruction = pipeline_c.IFID_register.instruction
        if pipeline_c.IFID_register.continue_stage:
            self.stage_write_index = pipeline_c.IFID_register.stage_write_index
        else:
            self.stage_write_index = None

    def write_stage_data(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.stage_write_index is not None:
            pipeline_c.stage_information[self.stage_write_index].append("EX")


    def __repr__(self) -> str:
        ret = ""
        ret += f"control_MemtoReg : {self.control_MemtoReg}\n"
        ret += f"control_RegWrite : {self.control_RegWrite}\n"
        ret += f"control_Branch : {self.control_Branch}\n"
        ret += f"control_MemRead : {self.control_MemRead}\n"
        ret += f"control_MemWrite : {self.control_MemWrite}\n"
        ret += f"control_RegDst : {self.control_RegDst}\n"
        ret += f"control_ALUOp : {self.control_ALUOp}\n"
        ret += f"control_ALUSrc : {self.control_ALUSrc}\n"
        ret += f"pc : {self.pc}\n"
        ret += f"read_data1 : {self.read_data1}\n"
        ret += f"read_data2 : {self.read_data2}\n"
        ret += f"immediate : {self.immediate}\n"
        ret += f"ImmediateSLL16 : {self.ImmediateSLL16}\n"
        ret += f"RegisterRs : {self.RegisterRs}\n"
        ret += f"RegisterRt : {self.RegisterRt}\n"
        ret += f"RegisterRd : {self.RegisterRd}\n"
        return ret

    def get_info(self) -> str:
        ret = f"""ID/EX Register

PC = {self.pc}

RegWrite = {self.control_RegWrite}
MemWrite = {self.control_MemWrite}
MemRead = {self.control_MemRead}
MemtoReg = {self.control_MemtoReg}
RedDst = {self.control_RegDst}
ALUOp = {self.control_ALUOp}
ALUSrc = {self.control_ALUSrc}

Register read data 1 = {self.read_data1}
Register read data 2 = {self.read_data2}

Rs: {self.RegisterRs}
Rt: {self.RegisterRt}
Rd: {self.RegisterRd}
Immediate: {self.immediate}
ImmediateSLL16: {self.ImmediateSLL16}
"""
        return ret


class EXMEMRegister(PipelineComponent):
    def __init__(self):
        # WB control signals
        self.control_MemtoReg: int = 0
        self.control_RegWrite: int = 0

        # MEM control signals
        self.control_MemRead: int = 0
        self.control_MemWrite: int = 0

        self.alu_zero: int = 0
        self.alu_result: int = 0
        self.read_data2: int = 0

        self.immediate: str = "0"
        self.ImmediateSLL16: str = "0"

        self.RegisterRd: int = 0

        self.instruction: Instruction = SpecialFormat(0, 0)
        self.stage_write_index: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        # WB control signals
        self.control_MemtoReg = pipeline_c.IDEX_register.control_MemtoReg
        self.control_RegWrite = pipeline_c.IDEX_register.control_RegWrite

        # MEM control signals
        self.control_MemRead = pipeline_c.IDEX_register.control_MemRead
        self.control_MemWrite = pipeline_c.IDEX_register.control_MemWrite

        # ALU results
        self.alu_zero = pipeline_c.EX_ALU.zero
        self.alu_result = pipeline_c.EX_ALU.result

        # Register read data
        # With forwarding, this should be the result of ForwardB's output
        #self.read_data2 = pipeline_c.IDEX_register.read_data2
        self.read_data2 = pipeline_c.EX_ForwardBMUX.value

        self.immediate = pipeline_c.IDEX_register.immediate
        self.ImmediateSLL16 = pipeline_c.IDEX_register.ImmediateSLL16

        self.RegisterRd = pipeline_c.EX_RegDstMUX.RegisterRd

        self.instruction = pipeline_c.IDEX_register.instruction
        self.stage_write_index = pipeline_c.IDEX_register.stage_write_index

    def write_stage_data(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.stage_write_index is not None:
            pipeline_c.stage_information[self.stage_write_index].append("MEM")

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def __repr__(self) -> str:
        ret = ""
        ret += f"control_MemtoReg : {self.control_MemtoReg}\n"
        ret += f"control_RegWrite : {self.control_RegWrite}\n"
        ret += f"control_MemRead : {self.control_MemRead}\n"
        ret += f"control_MemWrite : {self.control_MemWrite}\n"
        ret += f"alu_zero : {self.alu_zero}\n"
        ret += f"alu_result : {self.alu_result}\n"
        ret += f"read_data2 : {self.read_data2}\n"
        ret += f"immediate : {self.immediate}\n"
        ret += f"ImmediateSLL16: {self.ImmediateSLL16}\n"
        ret += f"RegisterRd : {self.RegisterRd}\n"
        return ret

    def get_info(self) -> str:
        ret = f"""EX/MEM Register

RegWrite = {self.control_RegWrite}
MemWrite = {self.control_MemWrite}
MemRead = {self.control_MemRead}
MemtoReg = {self.control_MemtoReg}

ALU zero = {self.alu_zero}
ALU result = {self.alu_result}

Register read data 2 = {self.read_data2}

Immediate: {self.immediate}
ImmediateSLL16: {self.ImmediateSLL16}
Rd: {self.RegisterRd}
"""
        return ret


class MEMWBRegister(PipelineComponent):
    def __init__(self):
        self.control_MemtoReg: int = 0
        self.control_RegWrite: int = 0

        self.memory_read_result: int = 0
        self.alu_result: int = 0

        self.immediate: str = "0"
        self.ImmediateSLL16: str = "0"
        self.RegisterRd: int = 0

        self.instruction: Instruction = SpecialFormat(0, 0)
        self.stage_write_index: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        self.control_MemtoReg = pipeline_c.EXMEM_register.control_MemtoReg
        self.control_RegWrite = pipeline_c.EXMEM_register.control_RegWrite

        self.memory_read_result = pipeline_c.MEM_Memory.read_value
        self.alu_result = pipeline_c.EXMEM_register.alu_result

        self.immediate = pipeline_c.EXMEM_register.immediate
        self.ImmediateSLL16 = pipeline_c.EXMEM_register.ImmediateSLL16
        self.RegisterRd = pipeline_c.EXMEM_register.RegisterRd

        self.instruction = pipeline_c.EXMEM_register.instruction
        self.stage_write_index = pipeline_c.EXMEM_register.stage_write_index

    def write_stage_data(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.stage_write_index is not None:
            pipeline_c.stage_information[self.stage_write_index].append("WB")
            self.stage_write_index = None

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def __repr__(self) -> str:
        ret = ""
        ret += f"control_MemtoReg : {self.control_MemtoReg}\n"
        ret += f"control_RegWrite : {self.control_RegWrite}\n"
        ret += f"memory_read_result : {self.memory_read_result}\n"
        ret += f"alu_result : {self.alu_result}\n"
        ret += f"immediate : {self.immediate}\n"
        ret += f"ImmediateSLL16 : {self.ImmediateSLL16}\n"
        ret += f"RegisterRd : {self.RegisterRd}\n"
        return ret

    def get_info(self) -> str:
        ret = f"""MEM/WB Register

RegWrite = {self.control_RegWrite}
MemtoReg = {self.control_MemtoReg}

Memory read result = {self.memory_read_result}

Immediate: {self.immediate}
ImmediateSLL16: {self.ImmediateSLL16}
Rd: {self.RegisterRd}
"""
        return ret


register_names = [
    "$zero",
    "$at",
    "$v0",
    "$v1",
    "$a0",
    "$a1",
    "$a2",
    "$a3",
    "$t0",
    "$t1",
    "$t2",
    "$t3",
    "$t4",
    "$t5",
    "$t6",
    "$t7",
    "$s0",
    "$s1",
    "$s2",
    "$s3",
    "$s4",
    "$s5",
    "$s6",
    "$s7",
    "$t8",
    "$t9",
    "$k0",
    "$k1",
    "$gp",
    "$sp",
    "$fp",
    "$ra"
]