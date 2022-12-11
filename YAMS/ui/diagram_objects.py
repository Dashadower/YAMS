from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsSimpleTextItem, QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt


class PCCounterObj(QGraphicsEllipseItem):
    def __init__(self, component):
        super().__init__(0, 0, 40, 100)
        self.component = component

        pen = QPen(Qt.black, 5)
        self.setPen(pen)


class PC4AdderObj(QG)