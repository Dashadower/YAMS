from typing import TYPE_CHECKING
from .registers import MainRegister, IFIDRegister, IDEXREgister, EXMEMRegister, MEMWBRegister
from .IF_components import *
from .ID_components import *
from .EX_components import *
from .MEM_components import *
from .WB_components import *
from .instructions import InstructionMemoryHandler
from .memory import Memory

class PipelineCoordinator:
    def __init__(self, instruction_handler: InstructionMemoryHandler, memory_handler: Memory):
        self.instruction_handler = instruction_handler
        self.memory_handler = memory_handler
        self.IF_PCCounter: "PCCounter" = PCCounter()
        self.IF_PCCounter.current_pc = instruction_handler.starting_addr
        self.IF_PC4Adder: "PC4Adder" = PC4Adder()
        self.IF_InstructionMemory: "InstructionMemory" = InstructionMemory(instruction_handler)
        self.IF_PCSrcMUX: "PCSrcMux" = PCSrcMux()
        self.IFID_register: IFIDRegister = IFIDRegister()

        self.ID_HazardDetector: HazardDetector = HazardDetector()
        self.ID_Control: Control = Control()
        self.ID_ControlZeroMUX: ControlZeroMUX = ControlZeroMUX()
        self.ID_ControlZeroSetOR: ControlZeroSetOR = ControlZeroSetOR()
        self.ID_BranchPCAdder: BranchPCAdder = BranchPCAdder()
        self.ID_ImmediateSLL2: ImmediateSLL2 = ImmediateSLL2()
        self.ID_ImmediateSignExtender: ImmediateSignExtender = ImmediateSignExtender()

        self.ID_MainRegister: MainRegister = MainRegister(sp=0x7ffffe40, gp=0x10008000)

        self.ID_BranchEqualCMP: BranchEqualCMP = BranchEqualCMP()
        self.ID_BranchCMPForwardAMUX: BranchCMPForwardAMUX = BranchCMPForwardAMUX()
        self.ID_BranchCMPForwardBMUX: BranchCMPForwardBMUX = BranchCMPForwardBMUX()
        self.ID_BranchForwardingUnit: BranchForwardingUnit = BranchForwardingUnit()
        self.ID_BranchEqualAND: BranchEqualAND = BranchEqualAND()
        self.ID_PCUpper4bitSelector: PCUpper4bitSelector = PCUpper4bitSelector()
        self.ID_JAddrSLL2: JAddrSLL2 = JAddrSLL2()
        self.ID_JaddrCalc: JaddrCalc = JaddrCalc()
        self.IDEX_register: IDEXREgister = IDEXREgister()

        self.EX_ForwardAMUX: ForwardAMUX = ForwardAMUX()
        self.EX_ForwardBMUX: ForwardBMUX = ForwardBMUX()
        self.EX_ALUSrcMUX: ALUSrcMUX = ALUSrcMUX()
        self.EX_ALUControl: ALUControl = ALUControl()
        self.EX_ALU: ALU = ALU()
        self.EX_ForwardingUnit: ForwardingUnit = ForwardingUnit()
        self.EX_RegDstMUX: RegDstMUX = RegDstMUX()
        self.EXMEM_register: EXMEMRegister = EXMEMRegister()

        self.MEM_Memory: MainMemory = MainMemory(memory_handler)
        self.MEMWB_register: MEMWBRegister = MEMWBRegister()

        self.WB_Mem2RegMUX: Mem2RegMUX = Mem2RegMUX()

        self.cycles: int = 0

        self.executed_instructions: int = 0
        self.stage_information = []

    def initialize(self):
        self.executed_instructions = 0
        self.cycles = 0
        self.stage_information = []
        self.IF_PCCounter.current_pc = self.instruction_handler.starting_addr
        self.IF_PC4Adder.update(self)
        self.IF_PCSrcMUX.update(self)
        self.IF_InstructionMemory.on_rising_edge(self)
        self.IF_InstructionMemory.write_stage_data(self)


    def single_step(self):
        self.cycles += 1
        self.rising_edge()
        self.update()
        #self.executed_instructions += 1
        self.write_stages()

    def write_stages(self):
        self.IF_InstructionMemory.write_stage_data(self)
        self.IFID_register.write_stage_data(self)
        self.IDEX_register.write_stage_data(self)
        self.EXMEM_register.write_stage_data(self)
        self.MEMWB_register.write_stage_data(self)

    def rising_edge(self):
        # 1. Update main register write
        self.ID_MainRegister.on_rising_edge(self)

        self.MEMWB_register.on_rising_edge(self)
        self.EXMEM_register.on_rising_edge(self)
        self.IDEX_register.on_rising_edge(self)
        self.IFID_register.on_rising_edge(self)

        # 2. Write to memory
        self.MEM_Memory.on_rising_edge(self)

        self.IF_PCCounter.on_rising_edge(self)
        self.IF_InstructionMemory.on_rising_edge(self)

        # 3. Update pipeline registers in reverse order to save dependency


    def update(self):
        """
        Update dependencies:
        """
        self.WB_Mem2RegMUX.update(self)

        # Update control and related stuff since it's independent
        self.ID_MainRegister.update(self)
        self.ID_Control.update(self)
        self.ID_HazardDetector.update(self)
        self.ID_ControlZeroMUX.update(self)
        self.ID_ControlZeroSetOR.update(self)

        # Update branch and jump target calculation
        self.ID_ImmediateSignExtender.update(self)
        self.ID_ImmediateSLL2.update(self)
        self.ID_BranchForwardingUnit.update(self)
        self.ID_BranchCMPForwardAMUX.update(self)
        self.ID_BranchCMPForwardBMUX.update(self)
        self.ID_BranchPCAdder.update(self)
        self.ID_BranchEqualCMP.update(self)
        self.ID_BranchEqualAND.update(self)
        self.ID_PCUpper4bitSelector.update(self)
        self.ID_JAddrSLL2.update(self)
        self.ID_JaddrCalc.update(self)

        # Update PC increment/update logic
        self.IF_PC4Adder.update(self)
        self.IF_PCSrcMUX.update(self)
        self.IF_PCCounter.update(self)
        self.IF_InstructionMemory.update(self)

        # Update pre-ALU stuff and then ALU
        self.EX_ForwardingUnit.update(self)
        self.EX_ForwardAMUX.update(self)
        self.EX_ForwardBMUX.update(self)
        self.EX_ALUSrcMUX.update(self)
        self.EX_ALUControl.update(self)
        self.EX_ALU.update(self)
        self.EX_RegDstMUX.update(self)

        self.MEM_Memory.update(self)

