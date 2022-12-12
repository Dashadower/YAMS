from .pipeline_component import PipelineComponent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pipeline import PipelineCoordinator

class MainMemory(PipelineComponent):
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.read_value: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.EXMEM_register.control_MemWrite:
            write_addr = pipeline_c.EXMEM_register.alu_result
            write_data = pipeline_c.EXMEM_register.read_data2
            print("stored", write_data, "to addr", hex(write_addr))
            self.memory_manager.store_word(write_addr, write_data)

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.EXMEM_register.control_MemRead:
            read_addr = pipeline_c.EXMEM_register.alu_result
            self.read_value = self.memory_manager.load_word(read_addr)
            print("read address", hex(read_addr), "value is", self.read_value)