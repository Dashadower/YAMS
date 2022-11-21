from .pipeline_component import PipelineComponent


class PCSrcMux(PipelineComponent):
    def __init__(self):
        self.pcsrc: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        self.pcsrc = pipeline_c.EX_branch_AND.value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

class PCCounter(PipelineComponent):
    def __init__(self):
        self.current_pc: int = None
        self.PCWrite: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.PCWrite:
            self.current_pc = pipeline_c.IF

    def set_PCWrite(self, value: int):
        self.PCWrite = value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass