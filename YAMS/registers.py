from dataclasses import dataclass
from typing import List
from .pipeline_component import PipelineComponent

class MainRegister(PipelineComponent):
    def __init__(self):
        self._register = [0] * 32

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
        self.pc = pipeline_c.IF_pc
        self.instruction = pipeline_c.IF_instruction_memory

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

class IDEXREgister(PipelineComponent):
    def __init__(self):
        # WB control signals
        self.control_memtoreg = None
        self.control_regwrite = None

        # MEM control signals
        self.control_branch = None
        self.control_memread = None
        self.control_memwrite = None

        # EX control signals
        self.control_regdst = None
        self.control_aluop = None
        self.control_alusrc = None

        self.pc = None
        self.read_data1 = None
        self.read_data2 = None
        self.immediate = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:

        control_out = pipeline_c.ID_control

        self.pc = pipeline_c.IFID_register.pc
        self.read_data1 = pipeline_c.ID_main_register.readdata_1
        self.read_data2 = pipeline_c.ID_main_register.readdata_2

        self.immediate = pipeline_c.ID_sign_extender.value



class EXMEMRegister(PipelineComponent):
    def __init__(self):
        # WB control signals
        self.control_memtoreg = None
        self.control_regwrite = None

        # MEM control signals
        self.control_branch = None
        self.control_memread = None
        self.control_memwrite = None

        self.pc = None
        self.alu_zero = None
        self.alu_result = None
        self.read_data2 = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        self.pc = None
        self.alu_zero = pipeline_c.EX_ALU.zero
        self.alu_result = pipeline_c.EX_ALU.result
        self.read_data2 = pipeline_c.IDEX_register.read_data2

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass


class MEMWBRegister:
    def __init__(self):
        self.control_memtoreg = None
        self.control_regwrite = None
        self.alu_result = None
        self.writeback_reg_dst = None
