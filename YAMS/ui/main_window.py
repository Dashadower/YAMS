from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from YAMS.ui.register_view import RegisterView
from YAMS.ui.memory_view import MemoryView
from YAMS.ui.pipeline_view import PipelineView

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def init_ui(self):
        self.showMaximized()
        self.setWindowTitle("YAMS")
        self.show()

        hbox = QHBoxLayout(self)

        horizontal_splitter = QSplitter(self)
        horizontal_splitter.setOrientation(Qt.Horizontal)

        register = RegisterView(horizontal_splitter)
        register.setText("text\n")

        tabs = QTabWidget(horizontal_splitter)
        tabs.showMaximized()

        self.pipeline_view = PipelineView()
        self.memory_view = MemoryView()
        self.instruction_view = MemoryView()
        tabs.addTab(self.pipeline_view, "Pipeline")
        tabs.addTab(self.memory_view, "Memory")
        tabs.addTab(self.instruction_view, "Instruction")

        horizontal_splitter.setStretchFactor(1, 10)

        hbox.addWidget(horizontal_splitter)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    w = MainWindow()
    w.init_ui()
    sys.exit(app.exec_())

