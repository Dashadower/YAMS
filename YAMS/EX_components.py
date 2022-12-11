from .pipeline_component import PipelineComponent
from typing import TYPE_CHECKING
from .utils import zero_extend_binary, string_numeric_to_decimal, signed_bits_to_int
if TYPE_CHECKING:
    from .pipeline import PipelineCoordinator

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
        self.ForwardA: int = 0
        self.ForwardB: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        self.ForwardA = 0
        self.ForwardB = 0
        # ForwardA: MEM stage hazard
        if pipeline_c.MEMWB_register.control_RegWrite and pipeline_c.MEMWB_register.RegisterRd != 0 and \
                pipeline_c.MEMWB_register.RegisterRd == pipeline_c.IDEX_register.RegisterRs:
            self.ForwardA = 1

        # ForwardA: EX stage hazard
        if pipeline_c.EXMEM_register.control_RegWrite and pipeline_c.EXMEM_register.RegisterRd != 0 and \
                pipeline_c.EXMEM_register.RegisterRd == pipeline_c.IDEX_register.RegisterRs:
            self.ForwardA = 2

        # ForwardB: MEM stage hazard
        if pipeline_c.MEMWB_register.control_RegWrite and pipeline_c.MEMWB_register.RegisterRd != 0 and \
                pipeline_c.MEMWB_register.RegisterRd == pipeline_c.IDEX_register.RegisterRt:
            self.ForwardB = 1

        # ForwardB: EX stage hazard
        if pipeline_c.EXMEM_register.control_RegWrite and pipeline_c.EXMEM_register.RegisterRd != 0 and \
                pipeline_c.EXMEM_register.RegisterRd == pipeline_c.IDEX_register.RegisterRt:
            self.ForwardB = 2

        pipeline_c.EX_ForwardAMUX.set_mux_input(self.ForwardA)
        pipeline_c.EX_ForwardBMUX.set_mux_input(self.ForwardB)


class ALUSrcMUX(PipelineComponent):
    def __init__(self):
        self.value: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.IDEX_register.control_ALUSrc == 0:
            self.value = pipeline_c.EX_ForwardBMUX.value
        else:
            self.value = signed_bits_to_int(pipeline_c.IDEX_register.immediate)

class ForwardAMUX(PipelineComponent):
    def __init__(self):
        self.value: int = 0
        self.mux_input: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def set_mux_input(self, value: int):
        self.mux_input = value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.mux_input == 0:  # main register read value
            self.value = pipeline_c.IDEX_register.read_data1
        elif self.mux_input == 1:  # memory read/previous ALU value
            self.value = pipeline_c.WB_Mem2RegMUX.value
        elif self.mux_input == 2:  # alu result
            self.value = pipeline_c.EXMEM_register.alu_result


class ForwardBMUX(PipelineComponent):
    def __init__(self):
        self.value: int = 0
        self.mux_input: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def set_mux_input(self, value: int):
        self.mux_input = value

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if self.mux_input == 0:  # main register read value
            self.value = pipeline_c.EX_ALUSrcMUX.value
        elif self.mux_input == 1:  # memory read/previous ALU value
            self.value = pipeline_c.WB_Mem2RegMUX.value
        elif self.mux_input == 2:  # alu result
            self.value = pipeline_c.EXMEM_register.alu_result


class ALUControl(PipelineComponent):
    def __init__(self):
        self.control_ALUControl = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        """
        ALUOp
        - 0: add
        - 1: subtract
        - 2: different based on funct field
        The following are unofficial implementations
        - 3: or
        """
        if pipeline_c.IDEX_register.control_ALUOp == 0:
            self.control_ALUControl = 2  # add
        elif pipeline_c.IDEX_register.control_ALUOp == 1:
            self.control_ALUControl = 6  # subtract
        elif pipeline_c.IDEX_register.control_ALUOp == 2:
            funct_field = pipeline_c.IDEX_register.immediate[-6:]
            if funct_field == "100000":
                self.control_ALUControl = 2  # add
            elif funct_field == "100010":
                self.control_ALUControl = 6  # subtract
            elif funct_field == "100100":
                self.control_ALUControl = 0  # AND
            elif funct_field == "100101":
                self.control_ALUControl = 1  # OR
            elif funct_field == "101010":
                self.control_ALUControl = 7  # set-on-less-than


class ALU(PipelineComponent):
    def __init__(self):
        self.result: int = 0
        self.zero: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        operand1 = pipeline_c.EX_ForwardAMUX.value
        operand2 = pipeline_c.EX_ALUSrcMUX.value

        alu_control = pipeline_c.EX_ALUControl.control_ALUControl
        if alu_control == 0:
            if isinstance(operand2, str):
                operand2 = int(zero_extend_binary(operand2, 32), 2)
            self.result = operand1 & operand2
        elif alu_control == 1:
            if isinstance(operand2, str):
                operand2 = int(zero_extend_binary(operand2, 32), 2)
            self.result = operand1 | operand2
        elif alu_control == 2:
            if isinstance(operand2, str):
                operand2 = signed_bits_to_int(operand2)
            self.result = operand1 + operand2
        elif alu_control == 6:
            if isinstance(operand2, str):
                operand2 = signed_bits_to_int(operand2)
            self.result = operand1 - operand2
        elif alu_control == 7:
            self.result = 1 if operand1 < operand2 else 0

        if self.result == 0:
            self.zero = 1
        else:
            self.zero = 0

        print(f"ALU: {operand1} @ {operand2} = {self.result}")

class RegDstMUX(PipelineComponent):
    def __init__(self):
        self.RegisterRd: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.IDEX_register.control_RegDst == 0:
            self.RegisterRd = pipeline_c.IDEX_register.RegisterRt
        else:
            self.RegisterRd = pipeline_c.IDEX_register.RegisterRd
