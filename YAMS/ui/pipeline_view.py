from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from YAMS.ui.pipeline_scene import PipelineScene

class PipelineView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()

        vertical_splitter = QSplitter(Qt.Vertical)

        top = PipelineScene(vertical_splitter)
        bottom_right = QGroupBox(vertical_splitter)
        bottom_right.setTitle("bottom_Right")

        vertical_splitter.setStretchFactor(0, 3)
        vertical_splitter.setStretchFactor(1, 1)

        hbox.addWidget(vertical_splitter)
        self.setLayout(hbox)
        self.show()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    w = PipelineView()
    sys.exit(app.exec_())