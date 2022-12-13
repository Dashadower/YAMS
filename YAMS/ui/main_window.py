from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from YAMS.ui.register_view import RegisterView
from YAMS.ui.memory_view import MemoryView
from YAMS.ui.pipeline_view import PipelineView
from YAMS.ui.instruction_view import InstructionView
from YAMS.utils import zero_extend_hex_to_word

class MainWindow(QWidget):
    def __init__(self, parent=None, simulator=None):
        super().__init__(parent)
        self.simulator = simulator

    def init_ui(self):
        self.showMaximized()
        self.setWindowTitle("YAMS")
        self.show()

        vbox = QVBoxLayout(self)

        button_vbox = QHBoxLayout()
        self.open_button = QPushButton("Open", self)
        self.open_button.clicked.connect(self.on_open)
        self.step_button = QPushButton("Step 1 cycle", self)
        self.step_button.clicked.connect(self.on_step)
        self.step_button.setEnabled(False)

        self.cycle_label = QLabel("CC: 0")

        button_vbox.addWidget(self.open_button)
        button_vbox.addWidget(self.step_button)
        button_vbox.addWidget(self.cycle_label)


        horizontal_splitter = QSplitter(self)
        horizontal_splitter.setOrientation(Qt.Horizontal)

        self.register_view = RegisterView(horizontal_splitter, simulator=self.simulator)

        tabs = QTabWidget(horizontal_splitter)
        tabs.showMaximized()

        self.pipeline_view = PipelineView()
        self.memory_view = MemoryView(simulator=self.simulator)
        self.instruction_view = InstructionView()
        tabs.addTab(self.pipeline_view, "Pipeline")
        tabs.addTab(self.memory_view, "Memory")
        tabs.addTab(self.instruction_view, "Instruction")

        horizontal_splitter.setStretchFactor(1, 10)

        vbox.addLayout(button_vbox)
        vbox.addWidget(horizontal_splitter)

    def update_views(self):
        self.pipeline_view.update_view(self.simulator.pipeline)
        self.register_view.update_view(self.simulator.pipeline)
        self.instruction_view.update_view(self.simulator.assembler)
        self.memory_view.update_view(self.simulator.data_memory)

    def on_open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'Assembly source (*.s *.asm);; All files (*.*)')
        if fname[0]:
            self.simulator.load_program(fname[0])
            self.step_button.setEnabled(True)
            self.memory_view.addr_entry.setText(zero_extend_hex_to_word(hex(self.simulator.data_memory.starting_address)))
            self.update_views()
            self.cycle_label.setText(f"CC: 0")


    def on_step(self):
        self.cycle_label.setText(f"CC: {self.simulator.clocks + 1}")
        self.simulator.single_step()
        self.update_views()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    w = MainWindow()
    w.init_ui()
    sys.exit(app.exec_())

