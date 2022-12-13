from .pipeline_component import PipelineComponent
from .instructions import InstructionMemoryHandler, Instruction, SpecialFormat
from .utils import zero_extend_hex_to_word
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pipeline import PipelineCoordinator

class PCSrcMux(PipelineComponent):
    def __init__(self):
        self.pc_out: int = 0
        self.mux_input: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        # If branch is taken, change to branch target address
        if pipeline_c.ID_BranchEqualAND.value:
            self.mux_input = 2
            self.pc_out = pipeline_c.ID_BranchPCAdder.value

        # If jump, jump to targe address
        elif pipeline_c.ID_Control.Jump:
            self.mux_input = 1
            self.pc_out = pipeline_c.ID_JaddrCalc.value

        else:
            self.mux_input = 0
            self.pc_out = pipeline_c.IF_PC4Adder.result

        #print("PC MUX is", hex(self.pc_out), self.mux_input)

    def get_info(self) -> str:
        ret = f"""PCSrcMux - Selects the source of the Program Counter
- mux_input:
0: PC comes from the PC + 4 Adder
1: PC comes from the Jump Address calculator
2: PC comes from PC + 4 + BranchOffset

Values:
MUX input = {self.mux_input}
output PC value = {zero_extend_hex_to_word(hex(self.pc_out))}
"""
        return ret

class PCCounter(PipelineComponent):
    def __init__(self):
        self.current_pc: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.PCWrite == 1:
            self.current_pc = pipeline_c.IF_PCSrcMUX.pc_out
            #print("Update pc to", hex(self.current_pc))

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def get_info(self) -> str:
        ret = f"""PCCounter - Keeps track of the current Program Counter

Values:
current PC = {zero_extend_hex_to_word(hex(self.current_pc))}
"""
        return ret


class PC4Adder(PipelineComponent):
    def __init__(self):
        self.result: int = 0

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        #self.update(pipeline_c)
        pass

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        current_pc = pipeline_c.IF_PCCounter.current_pc

        self.result = current_pc + 4

    def get_info(self) -> str:
        ret = f"""PC4Adder - Computes PC + 4

Values:
result = {zero_extend_hex_to_word(hex(self.result))}
"""
        return ret


class InstructionMemory(PipelineComponent):
    def __init__(self, instruction_handler: InstructionMemoryHandler):
        self.im_handler = instruction_handler
        self.current_instruction: Instruction = SpecialFormat(opcode=0, funct=0)
        self.stage_write_index: int = None

    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        instruction_addr = pipeline_c.IF_PCCounter.current_pc
        self.current_instruction = self.im_handler.fetch_instruction(instruction_addr)
        #self.update(pipeline_c)

    def write_stage_data(self, pipeline_c: "PipelineCoordinator") -> None:
        if pipeline_c.ID_HazardDetector.IFIDWrite:
            self.stage_write_index = pipeline_c.executed_instructions
            pipeline_c.executed_instructions += 1
        if self.stage_write_index is not None:
            if pipeline_c.ID_HazardDetector.IFIDWrite == 1:
                pipeline_c.stage_information.append([self.current_instruction.original_instruction])
                pipeline_c.stage_information[self.stage_write_index].extend([""] * pipeline_c.cycles)
                if pipeline_c.ID_BranchEqualAND.IFFlush == 1:
                    pipeline_c.stage_information[self.stage_write_index].append("IF(flush)")
                else:
                    pipeline_c.stage_information[self.stage_write_index].append("IF")
            else:
                self.stage_write_index = None

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        pass

    def get_info(self) -> str:
        ret = f"""InstructionMemory - Keeps track of the current instruction

Values:
current instruction = {self.current_instruction.__repr__()}
binary format = {self.current_instruction.to_binary()}
"""
        return ret