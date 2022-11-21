from .pipeline_component import PipelineComponent


class PCSrcMux(PipelineComponent):
    pcsrc: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        self.pcsrc = pipeline_c.EX_branch_AND.value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

class PCCounter(PipelineComponent):
