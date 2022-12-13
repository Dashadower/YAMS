from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from YAMS.ui.pipeline_scene import PipelineScene
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from YAMS.pipeline import PipelineCoordinator


class PipelineView(QWidget):
    def __init__(self, parent=None, simulator=None):
        super().__init__(parent)
        self.simulator = simulator
        self.active_object = ""
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()

        vertical_splitter = QSplitter(Qt.Vertical)


        self.pipeline_scene = PipelineScene(vertical_splitter, self)
        self.object_info_box = QTextEdit(vertical_splitter)
        self.object_info_box.setReadOnly(True)

        vertical_splitter.setStretchFactor(0, 3)
        vertical_splitter.setStretchFactor(1, 1)

        hbox.addWidget(vertical_splitter)
        self.setLayout(hbox)
        self.show()

    def clicked_object(self, name):
        if not self.simulator.pipeline: return
        self.active_object = name
        if name == "ALUSrcMUXObj":
            self.object_info_box.setText(self.simulator.pipeline.EX_ALUSrcMUX.get_info())

        elif name == "JAddrCalcObj":
            print(name)
            self.object_info_box.setText(self.simulator.pipeline.ID_JaddrCalc.get_info())

        elif name == "IDEXRegisterObj":
            self.object_info_box.setText(self.simulator.pipeline.IDEX_register.get_info())

        elif name == "ControlObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_Control.get_info())

        elif name == "ForwardAMUXObj":
            self.object_info_box.setText(self.simulator.pipeline.EX_ForwardAMUX.get_info())

        elif name == "ForwardBMUXObj":
            self.object_info_box.setText(self.simulator.pipeline.EX_ForwardBMUX.get_info())

        elif name == "MainRegisterObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_MainRegister.get_info())

        elif name == "ControlZeroMUXObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_ControlZeroMUX.get_info())

        elif name == "BranchCMPForwardAMUXObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_BranchCMPForwardAMUX.get_info())

        elif name == "BranchPCAdderObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_BranchPCAdder.get_info())

        elif name == "MemtoRegMUXObj":
            self.object_info_box.setText(self.simulator.pipeline.WB_Mem2RegMUX.get_info())

        elif name == "ALUControlObj":
            self.object_info_box.setText(self.simulator.pipeline.EX_ALUControl.get_info())

        elif name == "EXMEMRegisterObj":
            self.object_info_box.setText(self.simulator.pipeline.EXMEM_register.get_info())

        elif name == "MEMWBRegisterObj":
            self.object_info_box.setText(self.simulator.pipeline.MEMWB_register.get_info())

        elif name == "ALUObj":
            self.object_info_box.setText(self.simulator.pipeline.EX_ALU.get_info())

        elif name == "MemoryObj":
            self.object_info_box.setText(self.simulator.pipeline.MEM_Memory.get_info())

        elif name == "BranchCMPForwardBMUXObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_BranchCMPForwardBMUX.get_info())

        elif name == "BranchEqualCMPObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_BranchEqualCMP.get_info())

        elif name == "PCCounterObj":
            self.object_info_box.setText(self.simulator.pipeline.IF_PCCounter.get_info())

        elif name == "PC4AdderObj":
            self.object_info_box.setText(self.simulator.pipeline.IF_PC4Adder.get_info())

        elif name == "PCSrcMUXObj":
            self.object_info_box.setText(self.simulator.pipeline.IF_PCSrcMUX.get_info())

        elif name == "ForwardingUnitObj":
            self.object_info_box.setText(self.simulator.pipeline.EX_ForwardingUnit.get_info())

        elif name == "BranchEqualANDObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_BranchEqualAND.get_info())

        elif name == "InstructionMemoryObj":
            self.object_info_box.setText(self.simulator.pipeline.IF_InstructionMemory.get_info())

        elif name == "IFIDRegisterObj":
            self.object_info_box.setText(self.simulator.pipeline.IFID_register.get_info())

        elif name == "ImmediateSignExtenderObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_ImmediateSignExtender.get_info())

        elif name == "RegDstMUXObj":
            self.object_info_box.setText(self.simulator.pipeline.EX_RegDstMUX.get_info())

        elif name == "HazardDetectorObj":
            self.object_info_box.setText(self.simulator.pipeline.ID_HazardDetector.get_info())

    def update_view(self, pipeline_c):
        self.pipeline_scene.update_label_values(pipeline_c)
        self.clicked_object(self.active_object)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    w = PipelineView()
    sys.exit(app.exec_())