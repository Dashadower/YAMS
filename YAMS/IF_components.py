from .pipeline_component import PipelineComponent
from .instructions import InstructionMemoryHandler, Instruction, SpecialFormat
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pipeline import PipelineCoordinator

class PCSrcMux(PipelineComponent):
    def __init__(self):
        self.pc_out: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        # If branch is taken, change to branch target address
        if pipeline_c.ID_BranchEqualAND.value:
            self.pc_out = pipeline_c.ID_BranchPCAdder.value

        # If jump, jump to targe address
        elif pipeline_c.ID_Control.Jump:
            self.pc_out = pipeline_c.ID_JaddrCalc.value

        else:
            self.pc_out = pipeline_c.IF_PC4Adder.result


class PCCounter(PipelineComponent):
    def __init__(self):
        self.current_pc: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.PCWrite == 1:
            self.current_pc = pipeline_c.IF_PCSrcMUX.pc_out

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass


class PC4Adder(PipelineComponent):
    def __init__(self):
        self.result: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        #self.update(pipeline_c)
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        current_pc = pipeline_c.IF_PCCounter.current_pc

        self.result = current_pc + 4


class InstructionMemory(PipelineComponent):
    def __init__(self, instruction_handler: InstructionMemoryHandler):
        self.im_handler = instruction_handler
        self.current_instruction: Instruction = SpecialFormat(opcode=0, funct=0)

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        instruction_addr = pipeline_c.IF_PCCounter.current_pc
        self.current_instruction = self.im_handler.fetch_instruction(instruction_addr)
        #self.update(pipeline_c)

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass
