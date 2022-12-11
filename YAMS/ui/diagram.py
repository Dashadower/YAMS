from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QApplication, QGraphicsEllipseItem
from PyQt5.QtGui import QTransform, QPen, QColor
from PyQt5.QtCore import Qt
import sys
from diagram_objects import *

class DiagramScene(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.last_position = None
        self._zoom = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_position:
            # calculate the distance the mouse has been dragged
            delta = self.last_position - event.pos()
            # get the current transformation (which is a matrix that includes the
            # scaling ratios
            transform = self.transform()
            # m11 refers to the horizontal scale, m22 to the vertical scale;
            # divide the delta by their corresponding ratio
            deltaX = delta.x() / transform.m11()
            deltaY = delta.y() / transform.m22()
            # translate the current sceneRect by the delta
            self.setSceneRect(self.sceneRect().translated(deltaX, deltaY))
            # update the new origin point to the current position
            self.last_position = event.pos()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        self.scale(factor, factor)

    def draw(self):
        self.resize(800, 800)
        self.scene.addItem(PCCounterObj(None))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiagramScene()
    window.draw()
    window.show()

    app.exec_()

