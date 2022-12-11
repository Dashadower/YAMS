from .pipeline_component import PipelineComponent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pipeline import PipelineCoordinator

class Mem2RegMUX(PipelineComponent):
    def __init__(self):
        self.value: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.MEMWB_register.control_MemtoReg == 0:
            self.value = pipeline_c.MEMWB_register.alu_result
        else:
            self.value = pipeline_c.MEMWB_register.memory_read_result
