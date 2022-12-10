from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .registers import MainRegister, IFIDRegister, IDEXREgister, EXMEMRegister, MEMWBRegister
    from .IF_components import *
    from .EX_components import *


class PipelineCoordinator:
    def __init__(self):
        self.IF_PCCounter: "PCCounter" = None
        self.IF_PC4Adder: "PC4Adder" = None
        self.IF_InstructionMemory = None
        self.IFC_PCSrcMUX: "PCSrcMux" = None
        self.IFID_register: IFIDRegister = None

        self.ID_HazardDetector = None
        self.ID_Control = None
        self.ID_ControlZeroMUX = None
        self.ID_ControlZeroSetOR = None
        self.ID_BranchPCAdder = None
        self.ID_ImmediateSLL2 = None
        self.ID_ImmediateSignExtender = None
        self.ID_MainRegister: MainRegister = None
        self.ID_BranchEqualCMP = None
        self.ID_BranchEqualAND = None
        self.IDEX_register: IDEXREgister = None

        self.EX_ForwardAMUX = None
        self.EX_ForwardBMUX = None
        self.EX_ALUControl = None
        self.EX_ALU = None
        self.EX_ForwardingUnit = None
        self.EX_RegDstMUX = None
        self.EXMEM_register: EXMEMRegister = None

        self.MEM_Memory = None
        self.MEMWB_register: MEMWBRegister = None

        self.WB_Mem2RegMUX = None



    def rising_edge(self):
        # 1. Update main register write
        self.ID_MainRegister.on_rising_edge(self)

        # 2. Write to memory
        self.MEM_Memory.on_rising_edge(self)

        # 3. Update pipeline registers in reverse order to save dependency
        self.MEMWB_register.on_rising_edge(self)
        self.EXMEM_register.on_rising_edge(self)
        self.IDEX_register.on_rising_edge(self)
        self.IFID_register.on_rising_edge(self)

    def update(self):
        self.IFID_register.on_rising_edge(self)
        self.IDEX_register.on_rising_edge(self)
        self.EXMEM_register.on_rising_edge(self)
        self.MEMWB_register.on_rising_edge(self)

        self.EX_ForwardingUnit.on_rising_edge(self)