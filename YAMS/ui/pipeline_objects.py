
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class ALUSrcMUXObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(63 * scale_factor, 20 * scale_factor, 1 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("ALUSrcMUX", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class JAddrCalcObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(28 * scale_factor, 10 * scale_factor, 2 * scale_factor, 2 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("JAddrCalc", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class IDEXRegisterObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(49 * scale_factor, 9 * scale_factor, 4 * scale_factor, 26 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("IDEXRegister", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class ControlObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(24 * scale_factor, 6 * scale_factor, 3 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("Control", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class ForwardAMUXObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(60 * scale_factor, 12 * scale_factor, 1 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("ForwardAMUX", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class ForwardBMUXObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(60 * scale_factor, 19 * scale_factor, 1 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("ForwardBMUX", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class MainRegisterObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(33 * scale_factor, 16 * scale_factor, 5 * scale_factor, 11 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("MainRegister", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class ControlZeroMUXObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(38 * scale_factor, 8 * scale_factor, 1 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("ControlZeroMUX", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class BranchCMPForwardAMUXObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(43 * scale_factor, 13 * scale_factor, 1 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("BranchCMPForwardAMUX", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class BranchPCAdderObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(33 * scale_factor, 12 * scale_factor, 2 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("BranchPCAdder", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class MemtoRegMUXObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(95 * scale_factor, 24 * scale_factor, 1 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("MemtoRegMUX", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class ALUControlObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(65 * scale_factor, 26 * scale_factor, 3 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("ALUControl", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class EXMEMRegisterObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(73 * scale_factor, 9 * scale_factor, 4 * scale_factor, 26 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("EXMEMRegister", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class MEMWBRegisterObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(88 * scale_factor, 9 * scale_factor, 4 * scale_factor, 26 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("MEMWBRegister", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class ALUObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(65 * scale_factor, 13 * scale_factor, 5 * scale_factor, 9 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("ALU", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class MemoryObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(81 * scale_factor, 14 * scale_factor, 5 * scale_factor, 11 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("Memory", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class BranchCMPForwardBMUXObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(43 * scale_factor, 17 * scale_factor, 1 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("BranchCMPForwardBMUX", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class BranchEqualCMPObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(45 * scale_factor, 14 * scale_factor, 2 * scale_factor, 5 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("BranchEqualCMP", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class PCCounterObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(7 * scale_factor, 21 * scale_factor, 2 * scale_factor, 4 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("PCCounter", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class PC4AdderObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(11 * scale_factor, 11 * scale_factor, 2 * scale_factor, 2 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("PC4Adder", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class PCSrcMUXObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(4 * scale_factor, 21 * scale_factor, 1 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("PCSrcMUX", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class ForwardingUnitObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(64 * scale_factor, 35 * scale_factor, 5 * scale_factor, 4 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("ForwardingUnit", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class BranchEqualANDObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(46 * scale_factor, 4 * scale_factor, 2 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("BranchEqualAND", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class InstructionMemoryObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(13 * scale_factor, 19 * scale_factor, 4 * scale_factor, 8 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("InstructionMemory", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class IFIDRegisterObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(18 * scale_factor, 12 * scale_factor, 4 * scale_factor, 23 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("IFIDRegister", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class ImmediateSignExtenderObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(27 * scale_factor, 28 * scale_factor, 3 * scale_factor, 2 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("ImmediateSignExtender", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class RegDstMUXObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(61 * scale_factor, 31 * scale_factor, 1 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("RegDstMUX", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    


class HazardDetectorObj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__(30 * scale_factor, 3 * scale_factor, 4 * scale_factor, 3 * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("HazardDetector", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    

