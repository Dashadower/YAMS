from .pipeline_component import PipelineComponent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pipeline import PipelineCoordinator

class Mem2RegMUX(PipelineComponent):
    def __init__(self):
        self.value: int = 0
        self.mux_value: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.MEMWB_register.control_MemtoReg == 0:
            self.mux_value = 0
            self.value = pipeline_c.MEMWB_register.alu_result
        else:
            self.mux_value = 1
            self.value = pipeline_c.MEMWB_register.memory_read_result

    def get_info(self) -> str:
        ret = f"""Mem2RegMUX
Register write value comes from ALU result(0) or memory read result(1)

Values:
mux value = {self.mux_value}
output = {self.value}
"""
        return ret