from .pipeline_component import PipelineComponent

class ForwardingUnit(PipelineComponent):
    """
    ForwardA MUX becomes input of ALUSrc_1
    00: The first ALU Operand comes from the ID/EX register
    01: The first ALU Operand comes from the data memory or an earlier ALU result (MemtoReg MUX of MEM/WB register)
    10: The first ALU Operand comes from the prior ALU result (EX/MEM Register)

    ForwardB MUX becomes input of ALUSrc_2
    00: The second ALU Operand comes from the ID/EX register
    01: The second ALU Operand comes from the data memory or an earlier ALU result (MemtoReg MUX of MEM/WB register)
    10: The second ALU Operand comes from the prior ALU result (EX/MEM Register)
    """
    def __init__(self):
        pass

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass


class ForwardAMUX(PipelineComponent):
    def __init__(self):
        self.value: int = None
        self.mux_input: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def set_mux_input(self, value: int):
        self.mux_input = value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.mux_input == 0:  # main register read value
            self.value = pipeline_c.IDEX_register.read_data1
        elif self.mux_input == 1:  # memory read value
            self.value = pipeline_c.MEMWB_register.memory_read_result
        elif self.mux_input == 2:  # alu result
            self.value = pipeline_c.EXMEM_register.alu_result


class ForwardBMUX(PipelineComponent):
    def __init__(self):
        self.value: int = None
        self.mux_input: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def set_mux_input(self, value: int):
        self.mux_input = value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.mux_input == 0:  # main register read value
            self.value = pipeline_c.IDEX_register.read_data2
        elif self.mux_input == 1:  # memory read value
            self.value = pipeline_c.MEMWB_register.memory_read_result
        elif self.mux_input == 2:  # alu result
            self.value = pipeline_c.EXMEM_register.alu_result


class ALUControl(PipelineComponent):
    def __init__(self):
        pass

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pipeline_c.IDEX_register.
