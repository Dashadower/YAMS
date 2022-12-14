from .pipeline_component import PipelineComponent
from .opcodes import op
from .instructions import Instruction, RFormat, IFormat, JFormat
from .utils import decimal2bin, zero_extend_binary, signed_bits_to_int, int_to_signed_bits, zero_extend_hex_to_word
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pipeline import PipelineCoordinator


class HazardDetector(PipelineComponent):
    def __init__(self):
        # zero_control_signals, if set to zero will zero the control signals
        self.zero_control_signals = 1
        self.PCWrite: int = 1
        self.IFIDWrite: int = 1

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.zero_control_signals = 1
        self.PCWrite = 1
        self.IFIDWrite = 1
        if (pipeline_c.IDEX_register.control_MemRead) and \
                (pipeline_c.IDEX_register.RegisterRt == pipeline_c.IFID_register.instruction.get_rs() or
                pipeline_c.IDEX_register.RegisterRt == pipeline_c.IFID_register.instruction.get_rt()):
            # stall for memory use hazard
            self.zero_control_signals = 0
            self.PCWrite = 0
            self.IFIDWrite = 0

        # check if branch instruction immediately follows ALU instruction and causes hazard
        if pipeline_c.IDEX_register.control_RegWrite and pipeline_c.ID_Control.Branch:
            if pipeline_c.IDEX_register.control_RegDst == 0:
                write_destination = pipeline_c.IDEX_register.RegisterRt
            else:
                write_destination = pipeline_c.IDEX_register.RegisterRd
            if write_destination != 0 and \
                    (pipeline_c.IFID_register.instruction.get_rs() == write_destination or \
                    pipeline_c.IFID_register.instruction.get_rt() == write_destination):
                self.zero_control_signals = 0
                self.PCWrite = 0
                self.IFIDWrite = 0
        # check if branch instruction immediately follows load instruction and causes hazard
        # This requires an additional stall
        # Trigger condition:
        # 1. Instruction in EX/MEM is a load instruction, with destination RegisterRd
        # 2. Instruction in IF/ID is a beq, with one of its comparison arguments is load's RegisterRd
        # example:
        # lw $9, 0($8)
        # stall (first stall, handled in the above case)
        # stall (second stall, handled here)
        # beq $9, $0, label
        # if pipeline_c.EXMEM_register.control_MemRead == 1 and pipeline_c.EXMEM_register.control_RegWrite == 1 and \
        #         pipeline_c.IDEX_register.control_MemRead == 0 and \
        #         pipeline_c.IDEX_register.control_RegWrite == 0 and \
        #         pipeline_c.IDEX_register.control_MemWrite == 0:
        if pipeline_c.EXMEM_register.control_MemRead == 1 and pipeline_c.EXMEM_register.control_RegWrite == 1:
            if pipeline_c.IFID_register.instruction.get_instruction_name() == "beq" and \
                    pipeline_c.EXMEM_register.RegisterRd != 0 and \
                    (pipeline_c.IFID_register.instruction.get_rs() == pipeline_c.EXMEM_register.RegisterRd or
                     pipeline_c.IFID_register.instruction.get_rt() == pipeline_c.EXMEM_register.RegisterRd):
                self.zero_control_signals = 0
                self.PCWrite = 0
                self.IFIDWrite = 0

    def get_info(self) -> str:
        ret = f"""HazardDetector - Hazard Detection
zero_control_signals: if set to 0, zero all write control signals
PCWrite: if 0, don't update PC Counter on rising edge
IFIDWrite: if 0, don't update IF/ID Register on rising edge

Values:
zero_control_signals = {self.zero_control_signals}
PCWRite = {self.PCWrite}
IFIDWrite = {self.IFIDWrite}
"""
        return ret


class Control(PipelineComponent):
    def __init__(self):
        self.RegDst: int = 0
        self.ALUSrc: int = 0
        self.MemtoReg: int = 0
        self.RegWrite: int = 0
        self.MemRead: int = 0
        self.MemWrite: int = 0
        self.Jump: int = 0
        self.Branch: int = 0
        self.ALUOp: int = 0

    def reset_signals(self):
        self.RegDst = 0
        self.ALUSrc = 0
        self.MemtoReg = 0
        self.RegWrite = 0
        self.MemRead = 0
        self.MemWrite = 0
        self.Jump = 0
        self.Branch = 0
        self.ALUOp = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        instruction = pipeline_c.IFID_register.instruction
        self.reset_signals()
        self.decode(instruction)

    def decode(self, instruction: Instruction):
        instruction_name = instruction.get_instruction_name()
        if isinstance(instruction, RFormat):
            self.RegDst = 1
            self.ALUSrc = 0
            self.MemtoReg = 0
            self.RegWrite = 1
            self.MemRead = 0
            self.MemWrite = 0
            self.Jump = 0
            self.Branch = 0
            self.ALUOp = 2
        elif instruction_name == "lw":
            self.RegDst = 0
            self.ALUSrc = 1
            self.MemtoReg = 1
            self.RegWrite = 1
            self.MemRead = 1
            self.MemWrite = 0
            self.Jump = 0
            self.Branch = 0
            self.ALUOp = 0
        elif instruction_name == "sw":
            self.RegDst = self.MemtoReg
            self.ALUSrc = 1
            self.MemtoReg = self.MemtoReg
            self.RegWrite = 0
            self.MemRead = 0
            self.MemWrite = 1
            self.Jump = 0
            self.Branch = 0
            self.ALUOp = 0
        elif instruction_name == "beq":
            self.RegDst = self.RegDst
            self.ALUSrc = 0
            self.MemtoReg = self.MemtoReg
            self.RegWrite = 0
            self.MemRead = 0
            self.MemWrite = 0
            self.Jump = 0
            self.Branch = 1
            self.ALUOp = 1
        elif isinstance(instruction, IFormat):
            self.RegDst = 0
            self.ALUSrc = 1
            self.MemtoReg = 0
            self.RegWrite = 1
            self.MemRead = 0
            self.MemWrite = 0
            self.Jump = 0
            self.Branch = 0
            if instruction_name == "addi":
                self.ALUOp = 0
            elif instruction_name == "ori":
                self.ALUOp = 3
            elif instruction_name == "andi":
                self.ALUOp = 4
            elif instruction_name == "lui":
                self.ALUOp = 0
                self.ALUSrc = 2
            else:
                raise Exception("Not implemented instruction", instruction_name)
        elif instruction_name == "j":
            self.RegDst = self.RegDst
            self.ALUSrc = self.ALUSrc
            self.MemtoReg = self.MemtoReg
            self.RegWrite = 0
            self.MemRead = self.MemRead
            self.MemWrite = 0
            self.Jump = 1
            self.Branch = 0
            self.ALUOp = self.ALUOp

    def get_info(self) -> str:
        ret = f"""Control - Decodes instruction and generates control signals

Values:
RegDst = {self.RegDst}
ALUSrc = {self.ALUSrc}
MemtoReg = {self.MemtoReg}
RegWrite = {self.RegWrite}
MemRead = {self.MemRead}
MemWrite = {self.MemWrite}
Jump = {self.Jump}
Branch = {self.Branch}
ALUOp = {self.ALUOp}
"""
        return ret


class ControlZeroMUX(PipelineComponent):
    def __init__(self):
        self.RegDst: int = 0
        self.ALUSrc: int = 0
        self.MemtoReg: int = 0
        self.RegWrite: int = 0
        self.MemRead: int = 0
        self.MemWrite: int = 0
        self.Jump: int = 0
        self.Branch: int = 0
        self.ALUOp: int = 0
        self.mux_input = 0

    def reset_signals(self):
        self.RegWrite = 0
        self.MemRead = 0
        self.MemWrite = 0
        self.Jump = 0
        self.Branch = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.zero_control_signals == 0:
            self.reset_signals()
            self.mux_input = 1
        else:
            self.RegDst = pipeline_c.ID_Control.RegDst
            self.ALUSrc = pipeline_c.ID_Control.ALUSrc
            self.MemtoReg = pipeline_c.ID_Control.MemtoReg
            self.RegWrite = pipeline_c.ID_Control.RegWrite
            self.MemRead = pipeline_c.ID_Control.MemRead
            self.MemWrite = pipeline_c.ID_Control.MemWrite
            self.Jump = pipeline_c.ID_Control.Jump
            self.Branch = pipeline_c.ID_Control.Branch
            self.ALUOp = pipeline_c.ID_Control.ALUOp
            self.mux_input = 0

    def get_info(self) -> str:
        ret = f"""ControlZeroMUX - Zeros control signals if Hazard Detector emits signal, or current instruction is NOP

Values:
mux value = {self.mux_input}
RegWrite = {self.RegWrite}
MemWrite = {self.MemWrite}
MemRead = {self.MemRead}
"""
        return ret


class ControlZeroSetOR(PipelineComponent):
    def __init__(self):
        self.value: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.zero_control_signals == 0 or (pipeline_c.IFID_register.instruction.funct == 0 and pipeline_c.IFID_register.instruction.opcode == 0):
            self.value = 1
        else:
            self.value = 0

    def get_info(self) -> str:
        ret = f"""ControlZeroSetOR

Values:
result = {self.value}
"""
        return ret


class BranchPCAdder(PipelineComponent):
    def __init__(self):
        self.value: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.value = pipeline_c.IFID_register.pc + signed_bits_to_int(pipeline_c.ID_ImmediateSLL2.value)

    def get_info(self) -> str:
        ret = f"""BranchPCAdder

Values:
result = {zero_extend_hex_to_word(hex(self.value))}
"""
        return ret


class ImmediateSLL2(PipelineComponent):
    def __init__(self):
        self.value: str = "0"

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.value = pipeline_c.ID_ImmediateSignExtender.value[2:] + "00"

    def get_info(self) -> str:
        ret = f"""ImmediateSLL2 - Shift left immediate field

Values:
result = {self.value}
"""
        return ret


class ImmediateSLL16(PipelineComponent):
    def __init__(self):
        self.value: str = "0"

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        immediate = pipeline_c.IFID_register.instruction.to_binary()[-16:]
        self.value = immediate + "0" * 16

    def get_info(self) -> str:
        ret = f"""ImmediateSLL16 - Shift left immediate field 16 bits for lui instruction

Values:
result = {self.value}
"""
        return ret


class ImmediateSignExtender(PipelineComponent):
    def __init__(self):
        self.value: str = "0"

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        # get the lower 16 bits
        immediate = pipeline_c.IFID_register.instruction.to_binary()[-16:]

        # check if instruction is arithmetic:
        instruction = pipeline_c.IFID_register.instruction.get_instruction_name()
        if instruction in ("addi", "addiu", "lbu", "lhu", "ll", "lw", "slti", "sltiu", "sb", "sc", "sh", "sw", "beq"):
            # sign extend
            extension = "0" * 16 if immediate[0] == "0" else "1" * 16
            self.value = extension + immediate

        else:
            # zero extend
            self.value = "0" * 16 + immediate

    def get_info(self) -> str:
        ret = f"""ImmediateSignExtender - Sign/Zero extend immediate field

Values:
result = {self.value}
"""
        return ret

# MainRegister implemented im registers.py


class BranchEqualCMP(PipelineComponent):
    def __init__(self):
        self.value: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        # if pipeline_c.ID_MainRegister.read_value1 == pipeline_c.ID_MainRegister.read_value2:
        #     self.value = 1
        # else:
        #     self.value = 0
        if pipeline_c.ID_BranchCMPForwardAMUX.value == pipeline_c.ID_BranchCMPForwardBMUX.value:
            self.value = 1
        else:
            self.value = 0

    def get_info(self) -> str:
        ret = f"""BranchEqualCMP

Values:
result = {self.value}
"""
        return ret


class BranchCMPForwardAMUX(PipelineComponent):
    def __init__(self):
        self.value: int = 0
        self.mux_input: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def set_mux_input(self, value: int):
        self.mux_input = value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.mux_input == 0:  # main register read value rs
            self.value = pipeline_c.ID_MainRegister.read_value1
        elif self.mux_input == 1:  # memory read/previous ALU value
            self.value = pipeline_c.WB_Mem2RegMUX.value
        elif self.mux_input == 2:  # alu result
            self.value = pipeline_c.EXMEM_register.alu_result

    def get_info(self) -> str:
        ret = f"""BranchCMPForwardAMUX

Values:
mux value = {self.mux_input}
output = {self.value}
"""
        return ret


class BranchCMPForwardBMUX(PipelineComponent):
    def __init__(self):
        self.value: int = 0
        self.mux_input: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def set_mux_input(self, value: int):
        self.mux_input = value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.mux_input == 0:  # main register read value rt
            self.value = pipeline_c.ID_MainRegister.read_value2
        elif self.mux_input == 1:  # memory read/previous ALU value
            self.value = pipeline_c.WB_Mem2RegMUX.value
        elif self.mux_input == 2:  # alu result
            self.value = pipeline_c.EXMEM_register.alu_result

    def get_info(self) -> str:
        ret = f"""BranchCMPForwardBMUX

Values:
mux value = {self.mux_input}
output = {self.value}
"""
        return ret


class BranchForwardingUnit(PipelineComponent):
    """
    BranchCMPForwardAMUX becomes input of BranchEqualCMP
    00: The first comparison operand comes from the register
    01: The first comparison operand comes from the data memory or an earlier ALU result (MemtoReg MUX of MEM/WB register)
    10: The first comparison operand comes from the prior ALU result (EX/MEM Register)

    BranchCMPForwardBMUX becomes input of BranchEqualCMP
    00: The second comparison operand comes from the ID/EX register
    01: The second comparison operand comes from the data memory or an earlier ALU result (MemtoReg MUX of MEM/WB register)
    10: The second comparison operand comes from the prior ALU result (EX/MEM Register)
    """
    def __init__(self):
        self.ForwardA: int = 0
        self.ForwardB: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.ForwardA = 0
        self.ForwardB = 0
        # ForwardA: MEM stage hazard
        if pipeline_c.MEMWB_register.control_RegWrite and pipeline_c.MEMWB_register.RegisterRd != 0 and \
                pipeline_c.MEMWB_register.RegisterRd == pipeline_c.IFID_register.instruction.get_rs():
            self.ForwardA = 1

        # ForwardA: EX stage hazard
        if pipeline_c.EXMEM_register.control_RegWrite and pipeline_c.EXMEM_register.RegisterRd != 0 and \
                pipeline_c.EXMEM_register.RegisterRd == pipeline_c.IFID_register.instruction.get_rs():
            self.ForwardA = 2

        # ForwardB: MEM stage hazard
        if pipeline_c.MEMWB_register.control_RegWrite and pipeline_c.MEMWB_register.RegisterRd != 0 and \
                pipeline_c.MEMWB_register.RegisterRd == pipeline_c.IFID_register.instruction.get_rt():
            self.ForwardB = 1

        # ForwardB: EX stage hazard
        if pipeline_c.EXMEM_register.control_RegWrite and pipeline_c.EXMEM_register.RegisterRd != 0 and \
                pipeline_c.EXMEM_register.RegisterRd == pipeline_c.IFID_register.instruction.get_rt():
            self.ForwardB = 2

        pipeline_c.ID_BranchCMPForwardAMUX.set_mux_input(self.ForwardA)
        pipeline_c.ID_BranchCMPForwardBMUX.set_mux_input(self.ForwardB)

    def get_info(self) -> str:
        ret = f"""BranchForwardingUnit - Forwarding Unit for Branch equal comparer

Values:
ForwardA = {self.ForwardA}
ForwardB = {self.ForwardB}
"""
        return ret


class BranchEqualAND(PipelineComponent):
    def __init__(self):
        self.value = 0
        self.IFFlush: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_Control.Branch and pipeline_c.ID_BranchEqualCMP.value:
            self.value = 1
            self.IFFlush = 1
        elif pipeline_c.ID_Control.Jump:
            self.value = 0
            self.IFFlush = 1
        else:
            self.value = 0
            self.IFFlush = 0

    def get_info(self) -> str:
        ret = f"""BranchEqualAND

Values:
IFFlush = {self.IFFlush}
"""
        return ret


class PCUpper4bitSelector(PipelineComponent):
    def __init__(self):
        self.value: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.value = int(zero_extend_binary(decimal2bin(pipeline_c.IFID_register.pc), 32)[:4], 2)

    def get_info(self) -> str:
        ret = f"""PCUpper4bitsSelector - Select upper 4 bits of PC

Values:
output = {self.value}
"""
        return ret


class JAddrSLL2(PipelineComponent):
    def __init__(self):
        self.value: str = "0"

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        # get the lower 26 bits
        immediate = pipeline_c.IFID_register.instruction.to_binary()[-26:]
        self.value = immediate + "00"

    def get_info(self) -> str:
        ret = f"""JAddrSLL2 - shift left 2 immediate field for jump target address calculation

Values:
output = {self.value}
"""
        return ret


class JaddrCalc(PipelineComponent):
    def __init__(self):
        self.value: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pc_4bits = zero_extend_binary(decimal2bin(pipeline_c.ID_PCUpper4bitSelector.value), bits=4)
        jaddr = zero_extend_binary(pipeline_c.ID_JAddrSLL2.value, bits=26)
        self.value = int(f"{pc_4bits}{jaddr}", 2)

    def get_info(self) -> str:
        ret = f"""JaddrCalc - calculate jump target address

Values:
output = {zero_extend_hex_to_word(hex(self.value))}
"""
        return ret
