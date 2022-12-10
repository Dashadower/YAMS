from dataclasses import dataclass
from typing import List
from .pipeline_component import PipelineComponent

class MainRegister(PipelineComponent):
    def __init__(self):
        self._register = [0] * 32

        self.read_value1 = None
        self.read_value2 = None

    def _write(self, register_index, value):
        """
        Internal method to write a value to a given register index. May only be called on rising edge.
        """
        self._register[register_index] = value

    def _read(self, register_index):
        return self._register[register_index]

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.MEMWB_register.control_regwrite == 1:
            # do writeback here
            pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        # Components that hold data (memory, registers) cannot do anything in  update()
        pass


class IFIDRegister(PipelineComponent):
    def __init__(self):
        self.pc = None
        self.instruction = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.IFIDWrite:
            self.pc = pipeline_c.IF_PC4Adder.result
            self.instruction = pipeline_c.IF_instruction_memory
        else:  # if IF/IDWrite is 0, keep the contents of the register
            pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

class IDEXREgister(PipelineComponent):
    def __init__(self):
        # WB control signals
        self.control_MemtoReg = None
        self.control_RegWrite = None

        # MEM control signals
        self.control_Branch = None
        self.control_MemRead = None
        self.control_MemWrite = None

        # EX control signals
        self.control_RegDst = None
        self.control_ALUOp = None
        self.control_ALUSrc = None

        self.pc = None
        self.read_data1 = None
        self.read_data2 = None
        self.immediate = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:

        control_out = pipeline_c.ID_control

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
        self.read_data1 = pipeline_c.ID_main_register.readdata_1
        self.read_data2 = pipeline_c.ID_main_register.readdata_2

        self.immediate = pipeline_c.ID_sign_extender.value



class EXMEMRegister(PipelineComponent):
    def __init__(self):
        # WB control signals
        self.control_MemtoReg = None
        self.control_RegWrite = None

        # MEM control signals
        self.control_MemRead = None
        self.control_MemWrite = None

        self.alu_zero = None
        self.alu_result = None
        self.read_data2 = None

        self.immediate = None

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

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass


class MEMWBRegister(PipelineComponent):
    def __init__(self):
        self.control_MemtoReg = None
        self.control_RegWrite = None

        self.memory_read_result = None
        self.alu_result = None

        self.immediate = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        self.control_MemtoReg = pipeline_c.EXMEM_register.control_MemtoReg
        self.control_RegWrite = pipeline_c.EXMEM_register.control_RegWrite

        self.memory_read_result = pipeline_c.MEM_Memory.read_value
        self.alu_result = pipeline_c.EXMEM_register.alu_result

        self.immediate = pipeline_c.EXMEM_register.immediate

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass
