from .pipeline_component import PipelineComponent
from .opcodes import op
from .instructions import Instruction, RFormat, IFormat, JFormat
from .utils import decimal2bin, zero_extend_binary, signed_bits_to_int


class HazardDetector(PipelineComponent):
    def __init__(self):
        self.zero_control_signals = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass


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
        instruction = pipeline_c.IFID_register.instruction

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def decode(self, instruction: Instruction):
        if isinstance(instruction, RFormat):
            funct_field = instruction.funct


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

    def reset_signals(self):
        self.RegWrite = 0
        self.MemRead = 0
        self.MemWrite = 0
        self.Jump = 0
        self.Branch = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.zero_control_signals:
            self.reset_signals()
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


class ControlZeroSetOR(PipelineComponent):
    def __init__(self):
        self.value: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.IDFlush or (pipeline_c.IFID_register.instruction.funct == 0 and pipeline_c.IFID_register.instruction.opcode == 0):
            self.value = 1
        else:
            self.value = 0


class BranchPCAdder(PipelineComponent):
    def __init__(self):
        self.value: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.value = pipeline_c.IFID_register.pc + pipeline_c.ID_ImmediateSLL2.value


class ImmediateSLL2(PipelineComponent):
    def __init__(self):
        self.value: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.value = pipeline_c.ID_ImmediateSignExtender.value << 2


class ImmediateSignExtender(PipelineComponent):
    def __init__(self):
        self.value: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        # get the lower 16 bits
        immediate = pipeline_c.IFID_register.instruction.to_binary()[-16:]

        # check if instruction is arithmetic:
        instruction = pipeline_c.IFID_register.instruction.get_instruction_name()
        if instruction in ("addi", "addiu", "lbu", "lhu", "ll", "lw", "slti", "sltiu", "sb", "sc", "sh", "sw", ):
            # sign extend
            extension = "0" * 16 if immediate[0] == "0" else "1" * 16
            self.value = int(extension + immediate, 2)

        else:
            # zero extend
            self.value = int("0" * 16 + immediate, 2)


# MainRegister implemented im registers.py

class BranchEqualCMP(PipelineComponent):
    def __init__(self):
        self.value: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_MainRegister.read_value1 == pipeline_c.ID_MainRegister.read_value2:
            self.value = 1
        else:
            self.value = 0


class BranchCMPForwardAMUX(PipelineComponent):
    def __init__(self):
        self.mux_input: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass


class BranchCMPForwardBMUX(PipelineComponent):
    def __init__(self):
        self.mux_input: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass


class BranchEqualAND(PipelineComponent):
    def __init__(self):
        self.IFFlush: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_Control.Branch and pipeline_c.ID_BranchEqualCMP:
            self.IFFlush = True


class PCUpper4bitSelector(PipelineComponent):
    def __init__(self):
        self.value: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.value = int(zero_extend_binary(decimal2bin(pipeline_c.IFID_register.pc), 32)[:4], 2)


class JAddrSLL2(PipelineComponent):
    def __init__(self):
        self.value: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        immediate = pipeline_c.IFID_register.instruction.to_binary()
        # get the lower 26 bits
        self.value = int(immediate[-26:], 2) << 2


class JaddrCalc(PipelineComponent):
    def __init__(self):
        self.value: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pc_4bits = zero_extend_binary(decimal2bin(pipeline_c.ID_PCUpper4bitSelector.value), bits=4)
        jaddr = zero_extend_binary(decimal2bin(pipeline_c.ID_JAddrSLL2.value), bits=26)
        self.value = int(f"{pc_4bits}{jaddr}00", 2)
