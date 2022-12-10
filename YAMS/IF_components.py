from .pipeline_component import PipelineComponent
from .instructions import InstructionMemoryHandler, Instruction


class PCSrcMux(PipelineComponent):
    def __init__(self):
        self.pcsrc: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        self.pcsrc = pipeline_c.EX_branch_AND.value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        # If branch is taken, change to branch target address
        if pipeline_c.ID_BranchEqualAND.value:
            self.pcsrc = pipeline_c.ID_BranchPCAdder.value

        elif pipeline_c.ID_Control.Jump:
            self.pcsrc = pipeline_c.ID_JAddrCalc

class PCCounter(PipelineComponent):
    def __init__(self):
        self.current_pc: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.PCWrite == 1:
            self.current_pc = pipeline_c.IFC_PCSrcMUX.pcsrc

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass


class PC4Adder(PipelineComponent):
    def __init__(self):
        self.result = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        self.update(pipeline_c)

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        current_pc = pipeline_c.IF_PCCounter.current_pc

        self.result = current_pc + 4


class InstructionMemory(PipelineComponent):
    def __init__(self, instruction_handler: InstructionMemoryHandler):
        self.im_handler = instruction_handler
        self.current_instruction: Instruction = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        instruction_addr = pipeline_c.IF_PCCounter.current_pc
        self.current_instruction = self.im_handler.fetch_instruction(instruction_addr)