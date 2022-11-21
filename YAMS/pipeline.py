from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .registers import MainRegister, IFIDRegister, IDEXREgister, EXMEMRegister, MEMWBRegister


class PipelineSnapshot:


class PipelineCoordinator:
    def __init__(self):
        self.IF_PCCounter = None
        self.IFC_PCSrcMUX = None
        self.IF_instruction_memory = None
        self.IFID_register: IFIDRegister = None

        self.ID_control = None
        self.ID_sign_extender = None
        self.ID_main_register: MainRegister = None
        self.ID_hazard_detector = None
        self.IDEX_register: IDEXREgister = None

        self.EX_ALU = None
        self.EX_forwarding_unit = None
        self.EXMEM_register: EXMEMRegister = None

        self.MEM_memory = None
        self.MEMWB_register: MEMWBRegister = None



    def rising_edge(self):
        # 1. Update main register write
        self.ID_main_register.on_rising_edge(self)