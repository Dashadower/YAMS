from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QGraphicsEllipseItem
from PyQt5.QtGui import QTransform, QPen, QColor
from PyQt5.QtCore import Qt
import sys
from YAMS.ui.pipeline_objects import *
from typing import TYPE_CHECKING
from YAMS.utils import zero_extend_hex, zero_extend_binary, int_to_signed_bits
if TYPE_CHECKING:
    from YAMS.pipeline import PipelineCoordinator

class PipelineScene(QGraphicsView):
    def __init__(self, parent=None, pipeline_view=None):
        super().__init__(parent)
        self.pipeline_view = pipeline_view
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.last_position = None
        self._zoom = 0
        self.object_scale_factor = 30

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.draw()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)

    def clicked_object(self, name):
        print(name)

    def draw(self):
        self.PCSrcMUX = PCSrcMUXObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.PCSrcMUX)

        self.PCCounter = PCCounterObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.PCCounter)

        self.PC4Adder = PC4AdderObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.PC4Adder)

        self.InstructionMemory = InstructionMemoryObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.InstructionMemory)

        self.IFIDRegister = IFIDRegisterObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.IFIDRegister)

        ##########

        self.HazardDetector = HazardDetectorObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.HazardDetector)

        self.Control = ControlObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.Control)

        self.ControlZeroMUX = ControlZeroMUXObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.ControlZeroMUX)

        self.BranchEqualAnd = BranchEqualANDObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.BranchEqualAnd)

        self.BranchEqualCMP = BranchEqualCMPObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.BranchEqualCMP)

        self.BranchForwardA = BranchCMPForwardAMUXObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.BranchForwardA)

        self.BranchForwardB = BranchCMPForwardBMUXObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.BranchForwardB)

        self.MainRegister = MainRegisterObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.MainRegister)

        self.ImmediateSignExtender = ImmediateSignExtenderObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.ImmediateSignExtender)

        self.ImmediateSLL16 = ImmediateSLL16Obj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.ImmediateSLL16)

        self.BranchPCAdder = BranchPCAdderObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.BranchPCAdder)

        self.JAddrCalc = JAddrCalcObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.JAddrCalc)

        self.IDEXRegister = IDEXRegisterObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.IDEXRegister)

        ###########

        self.ForwardAMUX = ForwardAMUXObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.ForwardAMUX)

        self.ForwardBMUX = ForwardBMUXObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.ForwardBMUX)

        self.ALUSrcMUX = ALUSrcMUXObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.ALUSrcMUX)

        self.ALU = ALUObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.ALU)

        self.ALUControl = ALUControlObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.ALUControl)

        self.RegDstMUX = RegDstMUXObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.RegDstMUX)

        self.ForwardingUnit = ForwardingUnitObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.ForwardingUnit)

        self.EXMEMRegister = EXMEMRegisterObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.EXMEMRegister)

        self.Memory = MemoryObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.Memory)

        self.MEMWBRegister = MEMWBRegisterObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.MEMWBRegister)

        self.MemtoRegMUX = MemtoRegMUXObj(self.object_scale_factor, self.pipeline_view)
        self.scene.addItem(self.MemtoRegMUX)

        self.draw_lines()
        self.draw_labels()

    def draw_grid_line(self, x1, y1, x2, y2, pen, start_middle=True, end_middle=True):
        """
        :param x1: start point x grid cord
        :param y1: start point y grid coord
        :param x2: end point x grid coord
        :param y2: end point y grid coord
        :param p1_middle: Whether line should start from the center of the start grid, or its border
        :param p2_middle: Whether line should end at the center of the end point grid, or its border
        """
        x1 *= self.object_scale_factor
        x2 *= self.object_scale_factor
        y1 *= self.object_scale_factor
        y2 *= self.object_scale_factor
        half = self.object_scale_factor // 2
        if x1 == x2:
            if y1 > y2:
                direction = "up"
                if start_middle:
                    x1 += half
                    y1 += half
                else:
                    x1 += half
                    y1 += self.object_scale_factor

                if end_middle:
                    x2 += half
                    y2 += half
                else:
                    x2 += half

            else:
                direction = "down"
                if start_middle:
                    x1 += half
                    y1 += half
                else:
                    x1 += half
                    y1 += self.object_scale_factor

                if end_middle:
                    x2 += half
                    y2 += half
                else:
                    x2 += half

        else:
            if x1 > x2:
                direction = "left"
                if start_middle:
                    x1 += half
                    y1 += half
                else:
                    x1 += self.object_scale_factor
                    y1 += half

                if end_middle:
                    x2 += half
                    y2 += half
                else:
                    y2 += half
            else:
                direction = "right"
                if start_middle:
                    x1 += half
                    y1 += half
                else:
                    y1 += half

                if end_middle:
                    x2 += half
                    y2 += half
                else:
                    x2 += self.object_scale_factor
                    y2 += half


        self.scene.addLine(x1, y1, x2, y2, pen)

    def draw_half_gridline(self, x, y, pen, direction):
        x *= self.object_scale_factor
        y *= self.object_scale_factor
        middle_x = x + self.object_scale_factor // 2
        middle_y = y + self.object_scale_factor // 2
        if direction == "left":
            self.scene.addLine(middle_x, middle_y, x, middle_y, pen)
        elif direction == "right":
            self.scene.addLine(middle_x, middle_y, x + self.object_scale_factor, middle_y, pen)
        elif direction == "up":
            self.scene.addLine(middle_x, middle_y, middle_x, y, pen)
        elif direction == "down":
            self.scene.addLine(middle_x, middle_y, middle_x, y + self.object_scale_factor, pen)
        else:
            raise Exception("Unknown direction", direction)

    def draw_vertical_gridline(self, x, y, pen):
        x *= self.object_scale_factor
        y *= self.object_scale_factor
        self.scene.addLine(x + self.object_scale_factor // 2, y, x + self.object_scale_factor // 2, y + self.object_scale_factor, pen)

    def draw_horizontal_gridline(self, x, y, pen):
        x *= self.object_scale_factor
        y *= self.object_scale_factor
        self.scene.addLine(x, y + self.object_scale_factor // 2, x + self.object_scale_factor, y + self.object_scale_factor // 2)

    def draw_grid_dot(self, x, y):
        pen = QPen(Qt.black, 2)
        brush = QBrush(Qt.black)
        x *= self.object_scale_factor
        y *= self.object_scale_factor
        x += self.object_scale_factor // 2
        y += self.object_scale_factor // 2
        radius = self.object_scale_factor // 15
        self.scene.addEllipse(x - radius, y - radius, radius * 2, radius * 2, pen, brush)

    def draw_lines(self):
        line_pen = QPen(Qt.black, 1)
        control_line_pen = QPen(Qt.blue, 1)

        # PCSrcMUX -> PCCounter
        self.draw_grid_line(5, 22, 6, 22, line_pen, False, False)

        # PCCounter -> PC4Adder
        self.draw_grid_line(9, 22, 12, 22, line_pen, False, False)
        self.draw_grid_dot(10, 22)
        self.draw_grid_line(10, 22, 10, 12, line_pen, True, True)
        self.draw_half_gridline(10, 12, line_pen, "right")

        # PCCounter -> InstructionMemory
        self.draw_grid_line(9, 22, 12, 22, line_pen, False, False)

        # PC4Adder -> IFIDRegister
        self.draw_grid_dot(14, 12)
        self.draw_grid_line(13, 12, 17, 12, line_pen, False, False)

        # PC4Adder -> PCSrcMUX
        self.draw_grid_line(14, 12, 14, 9, line_pen, True, True)
        self.draw_grid_line(14, 9, 3, 9, line_pen, True, True)
        self.draw_grid_line(3, 9, 3, 21, line_pen, True, True)
        self.draw_half_gridline(3, 21, line_pen, "right")

        # InstructionMemory -> IFIDRegister
        self.draw_horizontal_gridline(17, 22, line_pen)

        ############################
        # ID

        # IFIDRegister -> BranchPCAdder (PC)
        self.draw_grid_line(22, 12, 32, 12, line_pen, False, False)

        # IFIDRegister -> JAddrCalc (I)
        # PC
        self.draw_grid_dot(24, 12)
        self.draw_grid_line(24, 12, 24, 10, line_pen, True, True)
        self.draw_grid_line(24, 10, 27, 10, line_pen, True, False)
        # Immediate
        self.draw_grid_dot(23, 11)
        self.draw_grid_line(23, 11, 27, 11, line_pen, True, False)

        # Spread out instruction from IFIDRegister
        #      |
        # IFID-|
        #      |
        self.draw_grid_line(22, 22, 23, 22, line_pen, False, True)
        self.draw_grid_line(23, 5, 23, 33, line_pen, True, True)

        # Spread i-path -> Control
        self.draw_grid_dot(23, 7)
        self.draw_half_gridline(23, 7, line_pen, "right")

        # Spread i-path -> HazardDetector
        self.draw_grid_line(23, 5, 29, 5, line_pen, True, False)

        # spread i-path -> MainRegister
        self.draw_grid_line(23, 17, 32, 17, line_pen, True, False)
        self.draw_grid_dot(23, 17)
        self.draw_grid_line(23, 19, 32, 19, line_pen, True, False)
        self.draw_grid_dot(23, 19)

        # spread i-path -> ImmediateSignExtender
        self.draw_grid_line(23, 28, 26, 28, line_pen, True, False)
        self.draw_grid_dot(23, 28)

        # spread i-path -> ImmediateSLL16
        self.draw_grid_line(24, 28, 24, 29, line_pen, True, True)
        self.draw_half_gridline(24, 29, line_pen, "right")
        self.draw_grid_dot(24, 28)

        # spread i-path -> IDEXRegister
        # Rt
        self.draw_grid_line(23, 31, 48, 31, line_pen, True, False)
        self.draw_grid_dot(23, 31)
        # Rs
        self.draw_grid_line(23, 32, 48, 32, line_pen, True, False)
        self.draw_grid_dot(23, 32)
        # Rd
        self.draw_grid_line(23, 33, 48, 33, line_pen, True, False)

        # ImmediateSignExtender -> IDEXRegister
        self.draw_grid_line(30, 28, 48, 28, line_pen, False, False)

        # ImmediateSignExtender -> BranchPCAdder
        self.draw_grid_dot(30, 28)
        self.draw_grid_line(30, 28, 30, 14, line_pen, True, True)
        self.draw_grid_line(30, 14, 32, 14, line_pen, True, False)

        # ImmediateSLL16 -> IDEXRegister
        self.draw_grid_line(27, 30, 48, 30, line_pen, False, False)

        # BranchPCAdder -> PCSrcMUX
        self.draw_grid_line(35, 13, 36, 13, line_pen, False, True)
        self.draw_grid_line(36, 13, 36, 1, line_pen, True, True)
        self.draw_grid_line(36, 1, 1, 1, line_pen, True, True)
        self.draw_grid_line(1, 1, 1, 23, line_pen, True, True)
        self.draw_grid_line(1, 23, 3, 23, line_pen, True, False)

        # JAddrCalc -> PCSrcMUX
        self.draw_grid_line(28, 9, 28, 4, line_pen, False, True)
        self.draw_grid_line(28, 4, 2, 4, line_pen, True, True)
        self.draw_grid_line(2, 4, 2, 22, line_pen, True, True)
        self.draw_grid_line(2, 22, 3, 22, line_pen, True, False)

        # Control -> ControlZeroMUX
        self.draw_grid_line(27, 8, 37, 8, control_line_pen, False, False)

        # ControlZeroMUX -> IDEXRegister
        self.draw_grid_line(39, 9, 48, 9, control_line_pen, False, False)

        # MainRegister -> IDEXRegister
        self.draw_grid_line(38, 22, 48, 22, line_pen, False, False)
        self.draw_grid_line(38, 25, 48, 25, line_pen, False, False)

        # MainRegister -> BranchCMPForwardAMUX
        self.draw_grid_line(38, 22, 38, 13, line_pen, True, True)
        self.draw_grid_dot(38, 22)
        self.draw_grid_line(38, 13, 42, 13, line_pen, True, False)

        # MainRegister -> BranchCMPForwardBMUX
        self.draw_grid_line(39, 25, 39, 17, line_pen, True, True)
        self.draw_grid_dot(39, 25)
        self.draw_grid_line(39, 17, 42, 17, line_pen, True, False)

        # BranchForwardAMUX, BranchForwardBMUX -> BranchEqualCMP
        self.draw_horizontal_gridline(44, 14, line_pen)
        self.draw_horizontal_gridline(44, 18, line_pen)

        # BranchEqualCMP -> BranchEqualAND
        self.draw_half_gridline(47, 16, line_pen, "left")
        self.draw_grid_line(47, 16, 47, 7, line_pen, True, False)

        # ControlZeroMUX -> BranchEqualAND
        self.draw_grid_line(46, 9, 46, 7, control_line_pen, True, False)
        self.draw_grid_dot(46, 9)

        # EX
        #######################

        # IDEXRegister -> ForwardAMUX
        self.draw_half_gridline(53, 22, line_pen, "left")
        self.draw_grid_line(53, 22, 53, 12, line_pen, True, True)
        self.draw_grid_line(53, 12, 59, 12, line_pen, True, False)

        #IDEXRegister -> ForwardBMUX
        self.draw_grid_line(53, 25, 54, 25, line_pen, False, True)
        self.draw_grid_line(54, 25, 54, 19, line_pen, True, True)
        self.draw_grid_line(54, 19, 58, 19, line_pen, True, False)

        #IDEXREgister -> ALUSrcMUX (immediate)
        # immediate
        self.draw_grid_line(53, 28, 61, 28, line_pen, False, True)
        self.draw_grid_line(61, 28, 61, 21, line_pen, True, True)
        self.draw_grid_line(61, 21, 62, 21, line_pen, True, False)
        # immediate sll 16
        self.draw_grid_line(53, 30, 62, 30, line_pen, False, True)
        self.draw_grid_line(62, 30, 62, 22, line_pen, True, True)
        self.draw_half_gridline(62, 22, line_pen, "right")
        #self.draw_grid_line(62, 30, )

        # IDEXREgister -> RegDSTMUX
        # Rt
        self.draw_grid_line(53, 31, 60, 31, line_pen, False, False)
        # Rd
        self.draw_grid_line(53, 33, 60, 33, line_pen, False, False)

        # IDEXRegister -> ForwardingUnit (Rt, Rs)
        # Rt
        self.draw_grid_line(59, 31, 59, 36, line_pen, True, True)
        self.draw_grid_dot(59, 31)
        self.draw_grid_line(59, 36, 63, 36, line_pen, True, False)
        # Rs
        self.draw_grid_line(53, 32, 58, 32, line_pen, False, True)
        self.draw_grid_line(58, 32, 58, 38, line_pen, True, True)
        self.draw_grid_line(58, 38, 63, 38, line_pen, True, False)

        # IDEXRegister -> EXMEMRegister
        # immediate sll 16 (lui)
        #self.draw_grid_line(53, 30, 72, 30, line_pen, False, False)

        # RegDstMUX -> EXMEMRegister
        self.draw_grid_line(62, 32, 72, 32, line_pen, False, False)

        # ForwardAMUX -> ALU
        self.draw_grid_line(61, 13, 64, 13, line_pen, False, False)

        # ForwardBMUX -> ALUSrcMUX
        self.draw_grid_line(60, 20, 62, 20, line_pen, False, False)

        # ForwardBMUX -> EXMEMRegister
        self.draw_grid_line(60, 20, 60, 23, line_pen, True, True)
        self.draw_grid_dot(60, 20)
        self.draw_grid_line(60, 23, 72, 23, line_pen, True, False)

        # ALUSrcMUX -> ALU
        self.draw_horizontal_gridline(64, 21, line_pen)

        # ALU -> EXMEMRegister
        self.draw_grid_line(70, 16, 72, 16, line_pen, False, False)

        # ALUControl -> ALU
        self.draw_grid_line(66, 25, 66, 22, control_line_pen, False, False)

        # MEM
        ##################

        # EXMEM -> Memory
        # ALUResult
        self.draw_grid_line(77, 16, 80, 16, line_pen, False, False)
        # register read (forwardB)
        self.draw_grid_line(77, 23, 80, 23, line_pen, False, False)

        # EXMEM -> branch forward mux, ALU forward MUX
        self.draw_grid_line(79, 16, 79, 40, line_pen, True, True)
        self.draw_grid_dot(79, 16)
        self.draw_grid_line(79, 40, 41, 40, line_pen, True, True)
        # ForwardA
        self.draw_grid_line(56, 40, 56, 14, line_pen, True, True)
        self.draw_grid_dot(56, 40)
        self.draw_grid_line(56, 14, 59, 14, line_pen, True, False)
        # ForwardB
        self.draw_grid_line(56, 21, 58, 21, line_pen, True, False)
        self.draw_grid_dot(56, 21)
        # Branch mux
        self.draw_grid_line(41, 40, 41, 15, line_pen, True, True)
        self.draw_grid_line(41, 15, 42, 15, line_pen, True, False)
        # branch mux B
        self.draw_grid_line(41, 19, 42, 19, line_pen, True, False)
        self.draw_grid_dot(41, 19)

        # EXMEM -> MEMWB
        # ALU Result
        self.draw_grid_line(79, 26, 87, 26, line_pen, True, False)
        self.draw_grid_dot(79, 26)
        # Rd
        self.draw_grid_line(77, 32, 87, 32, line_pen, False, False)
        # immediate sll 16
        #self.draw_grid_line(77, 30, 87, 30, line_pen, False, False)


        # EXMEM -> ForwardingUnit
        self.draw_grid_line(78, 32, 78, 36, line_pen, True, True)
        self.draw_grid_dot(78, 32)
        self.draw_grid_line(78, 36, 69, 36, line_pen, True, False)

        # Memory -> MEMWB
        self.draw_grid_line(86, 18, 87, 18, line_pen, False, False)

        # WB
        ###################
        # MEMWB -> MemToRegMUX
        # Memory read data
        self.draw_grid_line(92, 18, 93, 18, line_pen, False, True)
        self.draw_grid_line(93, 18, 93, 26, line_pen, True, True)
        self.draw_grid_line(93, 26, 94, 26, line_pen, True, False)
        # Previous ALU result
        self.draw_half_gridline(92, 26, line_pen, "left")
        self.draw_grid_line(92, 26, 92, 24, line_pen, True, True)
        self.draw_grid_line(92, 24, 94, 24, line_pen, True, False)
        # immediate SLL 16 (lui)
        # self.draw_grid_line(92, 30, 94, 30, line_pen, False, True)
        # self.draw_grid_line(94, 30, 94, 26, line_pen, True, True)
        # self.draw_half_gridline(94, 26, line_pen, "right")


        # MEMWB -> MainRegister
        # Write address
        self.draw_grid_line(92, 32, 94, 32, line_pen, False, True)
        self.draw_grid_line(94, 32, 94, 46, line_pen, True, True)
        self.draw_grid_line(94, 46, 31, 46, line_pen, True, True)
        self.draw_grid_line(31, 46, 31, 23, line_pen, True, True)
        self.draw_grid_line(31, 23, 32, 23, line_pen, True, False)

        # MEMWB -> ForwardUnit
        self.draw_grid_line(70, 46, 70, 38, line_pen, True, True)
        self.draw_grid_dot(70, 46)
        self.draw_grid_line(70, 38, 69, 38, line_pen, True, False)

        # Mem2RegMUX -> MainRegister (Write data)
        self.draw_grid_line(96, 25, 97, 25, line_pen, False, True)
        self.draw_grid_line(97, 25, 97, 44, line_pen, True, True)
        self.draw_grid_line(97, 44, 32, 44, line_pen, True, True)
        self.draw_grid_line(32, 44, 32, 25, line_pen, True, True)
        self.draw_half_gridline(32, 25, line_pen, "right")

        # Mem2RegMUX -> Branch/ALU Forward MUXes (writeback data)
        # ALU
        self.draw_grid_line(55, 44, 55, 13, line_pen, True, True)
        self.draw_grid_dot(55, 44)
        # FwdA
        self.draw_grid_line(55, 13, 59, 13, line_pen, True, False)
        # FwdB
        self.draw_grid_line(55, 20, 58, 20, line_pen, True, False)
        self.draw_grid_dot(55, 20)
        # Branch Fwd A
        self.draw_grid_line(40, 44, 40, 14, line_pen, True, True)
        self.draw_grid_dot(40, 44)
        self.draw_grid_line(40, 14, 42, 14, line_pen, True, False)
        # Branch Fwd B
        self.draw_grid_line(40, 18, 42, 18, line_pen, True, False)
        self.draw_grid_dot(40, 18)

    def draw_labels(self):
        value_label_brush = QBrush(Qt.red)
        control_label_brush = QBrush(Qt.blue)

        self.PCSrcMUXinput_label = QGraphicsSimpleTextItem()
        self.PCSrcMUXinput_label.setBrush(control_label_brush)
        self.PCSrcMUXinput_label.setPos(self.object_scale_factor * 4, self.object_scale_factor * 24)
        self.PCSrcMUXinput_label.setText("PCSrcMUXinput")
        self.scene.addItem(self.PCSrcMUXinput_label)

        self.PC_label = QGraphicsSimpleTextItem()
        self.PC_label.setBrush(value_label_brush)
        self.PC_label.setPos(self.object_scale_factor * 7, self.object_scale_factor * 25)
        self.PC_label.setText("PC")
        self.scene.addItem(self.PC_label)

        self.PCWrite_label = QGraphicsSimpleTextItem()
        self.PCWrite_label.setBrush(control_label_brush)
        self.PCWrite_label.setPos(self.object_scale_factor * 7, self.object_scale_factor * 20)
        self.PCWrite_label.setText("PCWrite")
        self.scene.addItem(self.PCWrite_label)

        self.Instruction_label = QGraphicsSimpleTextItem()
        self.Instruction_label.setBrush(value_label_brush)
        self.Instruction_label.setPos(self.object_scale_factor * 13, self.object_scale_factor * 27)
        self.Instruction_label.setText("Instruction")
        self.scene.addItem(self.Instruction_label)

        self.PC4Addvalue_label = QGraphicsSimpleTextItem()
        self.PC4Addvalue_label.setBrush(value_label_brush)
        self.PC4Addvalue_label.setPos(self.object_scale_factor * 13, self.object_scale_factor * 13)
        self.PC4Addvalue_label.setText("PC4Addvalue")
        self.scene.addItem(self.PC4Addvalue_label)

        self.IFIDWrite_label = QGraphicsSimpleTextItem()
        self.IFIDWrite_label.setBrush(control_label_brush)
        self.IFIDWrite_label.setPos(self.object_scale_factor * 18, self.object_scale_factor * 11)
        self.IFIDWrite_label.setText("IFIDWrite")
        self.scene.addItem(self.IFIDWrite_label)

        self.IFIDPCvalue_label = QGraphicsSimpleTextItem()
        self.IFIDPCvalue_label.setBrush(value_label_brush)
        self.IFIDPCvalue_label.setPos(self.object_scale_factor * 22, self.object_scale_factor * 13)
        self.IFIDPCvalue_label.setText("IFIDPCvalue")
        self.scene.addItem(self.IFIDPCvalue_label)

        self.Immediatevalue_label = QGraphicsSimpleTextItem()
        self.Immediatevalue_label.setBrush(value_label_brush)
        self.Immediatevalue_label.setPos(self.object_scale_factor * 24, self.object_scale_factor * 27)
        self.Immediatevalue_label.setText("Immediatevalue")
        self.scene.addItem(self.Immediatevalue_label)

        self.ImmSignExtendedvalue_label = QGraphicsSimpleTextItem()
        self.ImmSignExtendedvalue_label.setBrush(value_label_brush)
        self.ImmSignExtendedvalue_label.setPos(self.object_scale_factor * 30, self.object_scale_factor * 29)
        self.ImmSignExtendedvalue_label.setText("ImmSignExtendedvalue")
        self.scene.addItem(self.ImmSignExtendedvalue_label)

        self.ImmediateSLL16value_label = QGraphicsSimpleTextItem()
        self.ImmediateSLL16value_label.setBrush(value_label_brush)
        self.ImmediateSLL16value_label.setPos(self.object_scale_factor * 27, self.object_scale_factor * 30)
        self.ImmediateSLL16value_label.setText("ImmediateSLL16value")
        self.scene.addItem(self.ImmediateSLL16value_label)

        self.JAddrCalcvalue_label = QGraphicsSimpleTextItem()
        self.JAddrCalcvalue_label.setBrush(value_label_brush)
        self.JAddrCalcvalue_label.setPos(self.object_scale_factor * 29, self.object_scale_factor * 9)
        self.JAddrCalcvalue_label.setText("JAddrCalcvalue")
        self.scene.addItem(self.JAddrCalcvalue_label)

        self.BTAvalue_label = QGraphicsSimpleTextItem()
        self.BTAvalue_label.setBrush(value_label_brush)
        self.BTAvalue_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 15)
        self.BTAvalue_label.setText("BTAvalue")
        self.scene.addItem(self.BTAvalue_label)

        self.BranchPCAddervalue_label = QGraphicsSimpleTextItem()
        self.BranchPCAddervalue_label.setBrush(value_label_brush)
        self.BranchPCAddervalue_label.setPos(self.object_scale_factor * 35, self.object_scale_factor * 14)
        self.BranchPCAddervalue_label.setText("BranchPCAddervalue")
        self.scene.addItem(self.BranchPCAddervalue_label)

        self.RegWrite_label = QGraphicsSimpleTextItem()
        self.RegWrite_label.setBrush(control_label_brush)
        self.RegWrite_label.setPos(self.object_scale_factor * 35, self.object_scale_factor * 27)
        self.RegWrite_label.setText("RegWrite")
        self.scene.addItem(self.RegWrite_label)

        self.ReadReg1_label = QGraphicsSimpleTextItem()
        self.ReadReg1_label.setBrush(value_label_brush)
        self.ReadReg1_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 18)
        self.ReadReg1_label.setText("ReadReg1")
        self.scene.addItem(self.ReadReg1_label)

        self.ReadReg2_label = QGraphicsSimpleTextItem()
        self.ReadReg2_label.setBrush(value_label_brush)
        self.ReadReg2_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 20)
        self.ReadReg2_label.setText("ReadReg2")
        self.scene.addItem(self.ReadReg2_label)

        self.WriteReg_label = QGraphicsSimpleTextItem()
        self.WriteReg_label.setBrush(value_label_brush)
        self.WriteReg_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 24)
        self.WriteReg_label.setText("WriteReg")
        self.scene.addItem(self.WriteReg_label)

        self.WriteRegData_label = QGraphicsSimpleTextItem()
        self.WriteRegData_label.setBrush(value_label_brush)
        self.WriteRegData_label.setPos(self.object_scale_factor * 32, self.object_scale_factor * 26)
        self.WriteRegData_label.setText("WriteData")
        self.scene.addItem(self.WriteRegData_label)

        self.RegRead1value_label = QGraphicsSimpleTextItem()
        self.RegRead1value_label.setBrush(value_label_brush)
        self.RegRead1value_label.setPos(self.object_scale_factor * 38, self.object_scale_factor * 23)
        self.RegRead1value_label.setText("RegRead1value")
        self.scene.addItem(self.RegRead1value_label)

        self.RegRead2value_label = QGraphicsSimpleTextItem()
        self.RegRead2value_label.setBrush(value_label_brush)
        self.RegRead2value_label.setPos(self.object_scale_factor * 38, self.object_scale_factor * 26)
        self.RegRead2value_label.setText("RegRead2value")
        self.scene.addItem(self.RegRead2value_label)

        self.ControlZeroMUXinput_label = QGraphicsSimpleTextItem()
        self.ControlZeroMUXinput_label.setBrush(control_label_brush)
        self.ControlZeroMUXinput_label.setPos(self.object_scale_factor * 38, self.object_scale_factor * 7)
        self.ControlZeroMUXinput_label.setText("ControlZeroMUXinput")
        self.scene.addItem(self.ControlZeroMUXinput_label)

        self.ControlZeroMUXvalue_label = QGraphicsSimpleTextItem()
        self.ControlZeroMUXvalue_label.setBrush(control_label_brush)
        self.ControlZeroMUXvalue_label.setPos(self.object_scale_factor * 39, self.object_scale_factor * 10)
        self.ControlZeroMUXvalue_label.setText("ControlZeroMUXvalue")
        self.scene.addItem(self.ControlZeroMUXvalue_label)

        self.BranchCMPForwardAMUXinput_label = QGraphicsSimpleTextItem()
        self.BranchCMPForwardAMUXinput_label.setBrush(control_label_brush)
        self.BranchCMPForwardAMUXinput_label.setPos(self.object_scale_factor * 43, self.object_scale_factor * 12)
        self.BranchCMPForwardAMUXinput_label.setText("BranchCMPForwardAMUXinput")
        self.scene.addItem(self.BranchCMPForwardAMUXinput_label)

        self.BranchCMPForwardAMUXvalue_label = QGraphicsSimpleTextItem()
        self.BranchCMPForwardAMUXvalue_label.setBrush(value_label_brush)
        self.BranchCMPForwardAMUXvalue_label.setPos(self.object_scale_factor * 44, self.object_scale_factor * 15)
        self.BranchCMPForwardAMUXvalue_label.setText("BranchCMPForwardAMUXvalue")
        self.scene.addItem(self.BranchCMPForwardAMUXvalue_label)

        self.BranchCMPForwardBMUXinput_label = QGraphicsSimpleTextItem()
        self.BranchCMPForwardBMUXinput_label.setBrush(control_label_brush)
        self.BranchCMPForwardBMUXinput_label.setPos(self.object_scale_factor * 43, self.object_scale_factor * 20)
        self.BranchCMPForwardBMUXinput_label.setText("BranchCMPForwardBMUXinput")
        self.scene.addItem(self.BranchCMPForwardBMUXinput_label)

        self.BranchCMPForwardBMUXvalue_label = QGraphicsSimpleTextItem()
        self.BranchCMPForwardBMUXvalue_label.setBrush(value_label_brush)
        self.BranchCMPForwardBMUXvalue_label.setPos(self.object_scale_factor * 44, self.object_scale_factor * 19)
        self.BranchCMPForwardBMUXvalue_label.setText("BranchCMPForwardBMUXvalue")
        self.scene.addItem(self.BranchCMPForwardBMUXvalue_label)

        self.BranchControl_label = QGraphicsSimpleTextItem()
        self.BranchControl_label.setBrush(control_label_brush)
        self.BranchControl_label.setPos(self.object_scale_factor * 44, self.object_scale_factor * 7)
        self.BranchControl_label.setText("BranchControl")
        self.scene.addItem(self.BranchControl_label)

        self.BranchEqualCMPvalue_label = QGraphicsSimpleTextItem()
        self.BranchEqualCMPvalue_label.setBrush(value_label_brush)
        self.BranchEqualCMPvalue_label.setPos(self.object_scale_factor * 47, self.object_scale_factor * 17)
        self.BranchEqualCMPvalue_label.setText("BranchEqualCMPvalue")
        self.scene.addItem(self.BranchEqualCMPvalue_label)

        self.IFFlush_label = QGraphicsSimpleTextItem()
        self.IFFlush_label.setBrush(control_label_brush)
        self.IFFlush_label.setPos(self.object_scale_factor * 46, self.object_scale_factor * 3)
        self.IFFlush_label.setText("IFFlush")
        self.scene.addItem(self.IFFlush_label)

        # EX

        self.ForwardAMUXinput_label = QGraphicsSimpleTextItem()
        self.ForwardAMUXinput_label.setBrush(control_label_brush)
        self.ForwardAMUXinput_label.setPos(self.object_scale_factor * 60, self.object_scale_factor * 11)
        self.ForwardAMUXinput_label.setText("ForwardAMUXinput")
        self.scene.addItem(self.ForwardAMUXinput_label)

        self.ForwardAMUXvalue_label = QGraphicsSimpleTextItem()
        self.ForwardAMUXvalue_label.setBrush(value_label_brush)
        self.ForwardAMUXvalue_label.setPos(self.object_scale_factor * 61, self.object_scale_factor * 14)
        self.ForwardAMUXvalue_label.setText("ForwardAMUXvalue")
        self.scene.addItem(self.ForwardAMUXvalue_label)

        self.ForwardBMUXinput_label = QGraphicsSimpleTextItem()
        self.ForwardBMUXinput_label.setBrush(control_label_brush)
        self.ForwardBMUXinput_label.setPos(self.object_scale_factor * 59, self.object_scale_factor * 22)
        self.ForwardBMUXinput_label.setText("ForwardBMUXinput")
        self.scene.addItem(self.ForwardBMUXinput_label)

        self.ForwardBMUXvalue_label = QGraphicsSimpleTextItem()
        self.ForwardBMUXvalue_label.setBrush(value_label_brush)
        self.ForwardBMUXvalue_label.setPos(self.object_scale_factor * 60, self.object_scale_factor * 21)
        self.ForwardBMUXvalue_label.setText("ForwardBMUXvalue")
        self.scene.addItem(self.ForwardBMUXvalue_label)

        self.ALUSrcMUXinput_label = QGraphicsSimpleTextItem()
        self.ALUSrcMUXinput_label.setBrush(control_label_brush)
        self.ALUSrcMUXinput_label.setPos(self.object_scale_factor * 63, self.object_scale_factor * 23)
        self.ALUSrcMUXinput_label.setText("ALUSrcMUXinput")
        self.scene.addItem(self.ALUSrcMUXinput_label)

        self.ALUSrcMUXvalue_label = QGraphicsSimpleTextItem()
        self.ALUSrcMUXvalue_label.setBrush(value_label_brush)
        self.ALUSrcMUXvalue_label.setPos(self.object_scale_factor * 64, self.object_scale_factor * 22)
        self.ALUSrcMUXvalue_label.setText("ALUSrcMUXvalue")
        self.scene.addItem(self.ALUSrcMUXvalue_label)

        self.ALUResult_label = QGraphicsSimpleTextItem()
        self.ALUResult_label.setBrush(value_label_brush)
        self.ALUResult_label.setPos(self.object_scale_factor * 70, self.object_scale_factor * 17)
        self.ALUResult_label.setText("ALUResult")
        self.scene.addItem(self.ALUResult_label)

        self.ALUControlvalue_label = QGraphicsSimpleTextItem()
        self.ALUControlvalue_label.setBrush(control_label_brush)
        self.ALUControlvalue_label.setPos(self.object_scale_factor * 67, self.object_scale_factor * 25)
        self.ALUControlvalue_label.setText("ALUControlvalue")
        self.scene.addItem(self.ALUControlvalue_label)

        self.RegDstMUXinput_label = QGraphicsSimpleTextItem()
        self.RegDstMUXinput_label.setBrush(control_label_brush)
        self.RegDstMUXinput_label.setPos(self.object_scale_factor * 61, self.object_scale_factor * 34)
        self.RegDstMUXinput_label.setText("RegDstMUXinput")
        self.scene.addItem(self.RegDstMUXinput_label)

        self.RegDstMUXvalue_label = QGraphicsSimpleTextItem()
        self.RegDstMUXvalue_label.setBrush(value_label_brush)
        self.RegDstMUXvalue_label.setPos(self.object_scale_factor * 62, self.object_scale_factor * 33)
        self.RegDstMUXvalue_label.setText("RegDstMUXvalue")
        self.scene.addItem(self.RegDstMUXvalue_label)

        # MEM

        self.MemRead_label = QGraphicsSimpleTextItem()
        self.MemRead_label.setBrush(control_label_brush)
        self.MemRead_label.setPos(self.object_scale_factor * 83, self.object_scale_factor * 13)
        self.MemRead_label.setText("MemRead")
        self.scene.addItem(self.MemRead_label)

        self.MemWrite_label = QGraphicsSimpleTextItem()
        self.MemWrite_label.setBrush(control_label_brush)
        self.MemWrite_label.setPos(self.object_scale_factor * 83, self.object_scale_factor * 25)
        self.MemWrite_label.setText("MemWrite")
        self.scene.addItem(self.MemWrite_label)

        self.MemoryWriteaddr_label = QGraphicsSimpleTextItem()
        self.MemoryWriteaddr_label.setBrush(value_label_brush)
        self.MemoryWriteaddr_label.setPos(self.object_scale_factor * 80, self.object_scale_factor * 17)
        self.MemoryWriteaddr_label.setText("MemoryWriteaddr")
        self.scene.addItem(self.MemoryWriteaddr_label)

        self.MemoryWritevalue_label = QGraphicsSimpleTextItem()
        self.MemoryWritevalue_label.setBrush(value_label_brush)
        self.MemoryWritevalue_label.setPos(self.object_scale_factor * 80, self.object_scale_factor * 24)
        self.MemoryWritevalue_label.setText("MemoryWritevalue")
        self.scene.addItem(self.MemoryWritevalue_label)

        self.MemoryReadvalue_label = QGraphicsSimpleTextItem()
        self.MemoryReadvalue_label.setBrush(value_label_brush)
        self.MemoryReadvalue_label.setPos(self.object_scale_factor * 86, self.object_scale_factor * 19)
        self.MemoryReadvalue_label.setText("MemoryReadvalue")
        self.scene.addItem(self.MemoryReadvalue_label)

        # WB

        self.MemtoRegMUXinput_label = QGraphicsSimpleTextItem()
        self.MemtoRegMUXinput_label.setBrush(control_label_brush)
        self.MemtoRegMUXinput_label.setPos(self.object_scale_factor * 95, self.object_scale_factor * 23)
        self.MemtoRegMUXinput_label.setText("MemtoRegMUXinput")
        self.scene.addItem(self.MemtoRegMUXinput_label)

        self.MemtoRegMUXvalue_label = QGraphicsSimpleTextItem()
        self.MemtoRegMUXvalue_label.setBrush(value_label_brush)
        self.MemtoRegMUXvalue_label.setPos(self.object_scale_factor * 96, self.object_scale_factor * 26)
        self.MemtoRegMUXvalue_label.setText("MemtoRegMUXvalue")
        self.scene.addItem(self.MemtoRegMUXvalue_label)

    def update_label_values(self, pipeline_c: "PipelineCoordinator"):
        self.PCSrcMUXinput_label.setText(f"PCSrc: {pipeline_c.IF_PCSrcMUX.mux_input}")
        self.PC_label.setText(zero_extend_hex(hex(pipeline_c.IF_PCCounter.current_pc), bytes=4))

        self.PCWrite_label.setText(f"PCWrite: {pipeline_c.ID_HazardDetector.PCWrite}")

        self.Instruction_label.setText(pipeline_c.IF_InstructionMemory.current_instruction.to_binary())

        self.PC4Addvalue_label.setText(zero_extend_hex(hex(pipeline_c.IF_PC4Adder.result),  bytes=4))

        self.IFIDWrite_label.setText(f"IFIDWrite: {pipeline_c.ID_HazardDetector.IFIDWrite}")

        self.IFIDPCvalue_label.setText(zero_extend_hex(hex(pipeline_c.IFID_register.pc), bytes=4))

        self.Immediatevalue_label.setText(pipeline_c.IFID_register.instruction.to_binary()[-16:])

        self.ImmSignExtendedvalue_label.setText(pipeline_c.ID_ImmediateSignExtender.value)

        self.ImmediateSLL16value_label.setText(pipeline_c.ID_ImmediateSLL16.value)

        self.JAddrCalcvalue_label.setText(zero_extend_hex(hex(pipeline_c.ID_JaddrCalc.value), bytes=4))

        self.BTAvalue_label.setText(pipeline_c.ID_ImmediateSLL2.value)

        self.BranchPCAddervalue_label.setText(zero_extend_hex(hex(pipeline_c.ID_BranchPCAdder.value), bytes=4))

        self.RegWrite_label.setText(f"RegWrite: {pipeline_c.MEMWB_register.control_RegWrite}")

        self.ReadReg1_label.setText(str(pipeline_c.IFID_register.instruction.get_rs()))

        self.ReadReg2_label.setText(str(pipeline_c.IFID_register.instruction.get_rt()))

        self.WriteReg_label.setText(str(pipeline_c.MEMWB_register.RegisterRd))

        self.WriteRegData_label.setText(str(pipeline_c.WB_Mem2RegMUX.value))

        self.RegRead1value_label.setText(str(pipeline_c.ID_MainRegister.read_value1))

        self.RegRead2value_label.setText(str(pipeline_c.ID_MainRegister.read_value2))

        self.ControlZeroMUXinput_label.setText(str(pipeline_c.ID_ControlZeroMUX.mux_input))

        self.ControlZeroMUXvalue_label.setText("Control" if pipeline_c.ID_ControlZeroMUX.mux_input == 0 else "0000")

        self.BranchCMPForwardAMUXinput_label.setText(str(pipeline_c.ID_BranchCMPForwardAMUX.mux_input))

        self.BranchCMPForwardAMUXvalue_label.setText(str(pipeline_c.ID_BranchCMPForwardAMUX.value))

        self.BranchCMPForwardBMUXinput_label.setText(str(pipeline_c.ID_BranchCMPForwardBMUX.mux_input))

        self.BranchCMPForwardBMUXvalue_label.setText(str(pipeline_c.ID_BranchCMPForwardBMUX.value))

        self.BranchEqualCMPvalue_label.setText(str(pipeline_c.ID_BranchEqualCMP.value))

        self.IFFlush_label.setText(f"IFFlush: {pipeline_c.ID_BranchEqualAND.value}")

        self.BranchControl_label.setText(f"Branch: {pipeline_c.ID_Control.Branch}")

        self.ForwardAMUXinput_label.setText(str(pipeline_c.EX_ForwardAMUX.mux_input))

        self.ForwardAMUXvalue_label.setText(str(pipeline_c.EX_ForwardAMUX.value))

        self.ForwardBMUXinput_label.setText(str(pipeline_c.EX_ForwardBMUX.mux_input))

        self.ForwardBMUXvalue_label.setText(str(pipeline_c.EX_ForwardBMUX.value))

        self.ALUSrcMUXinput_label.setText(str(pipeline_c.EX_ALUSrcMUX.mux_input))

        self.ALUSrcMUXvalue_label.setText(str(pipeline_c.EX_ALUSrcMUX.value))

        self.ALUResult_label.setText(str(pipeline_c.EX_ALU.result))

        self.ALUControlvalue_label.setText(zero_extend_binary(bin(pipeline_c.EX_ALUControl.control_ALUControl)[2:], bits=4))

        self.RegDstMUXinput_label.setText(str(pipeline_c.EX_RegDstMUX.mux_input))

        self.RegDstMUXvalue_label.setText(str(pipeline_c.EX_RegDstMUX.RegisterRd))

        self.MemRead_label.setText(f"MemRead: {pipeline_c.EXMEM_register.control_MemRead}")

        self.MemWrite_label.setText(f"MemWrite:{pipeline_c.EXMEM_register.control_MemWrite}")

        self.MemoryWriteaddr_label.setText(zero_extend_hex(hex(int(int_to_signed_bits(pipeline_c.EXMEM_register.alu_result), 2)), bytes=4))

        self.MemoryWritevalue_label.setText(str(pipeline_c.EXMEM_register.read_data2))

        self.MemoryReadvalue_label.setText(str(pipeline_c.MEM_Memory.read_value))

        self.MemtoRegMUXinput_label.setText(str(pipeline_c.WB_Mem2RegMUX.mux_value))

        self.MemtoRegMUXvalue_label.setText(str(pipeline_c.WB_Mem2RegMUX.value))







    def update(self):
        self.IFFlush_label.setText()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PipelineScene()
    window.draw()
    window.show()

    app.exec_()

