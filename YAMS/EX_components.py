from .pipeline_component import PipelineComponent

class ForwardingUnit:
    """
    ForwardA MUX becomes input of ALUSrc_1
    00: The first ALU Operand comes from the ID/EX register
    10: The first ALU Operand comes from the prior ALU result (EX/MEM Register)
    01: The first ALU Operand comes from the data memory or an earlier ALU result (MemtoReg MUX of MEM/WB register)

    ForwardB MUX becomes input of ALUSrc_2
    00: The second ALU Operand comes from the ID/EX register
    10: The second ALU Operand comes from the prior ALU result (EX/MEM Register)
    01: The second ALU Operand comes from the data memory or an earlier ALU result (MemtoReg MUX of MEM/WB register)
    """