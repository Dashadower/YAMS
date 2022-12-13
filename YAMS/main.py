import sys
from PyQt5.QtWidgets import QApplication
from YAMS.ui.main_window import MainWindow
from YAMS.pipeline import PipelineCoordinator
from YAMS.parser import Parser
from YAMS.assembler import Assembler
from YAMS.instructions import InstructionMemoryHandler
from YAMS.memory import Memory

class MIPSSimulator:
    def __init__(self):
        self.file_path = ""
        self.parser = None
        self.assembler = None
        self.pipeline = None
        self.instruction_memory = None
        self.data_memory = None

        self.clocks = 0

    def load_program(self, filepath):
        self.file_path = filepath
        self.parser = Parser(open(self.file_path).read())
        data_segment, text_segment = self.parser.parse()
        self.assembler = Assembler(text_segment, data_segment)
        self.assembler.assemble()

        self.instruction_memory = InstructionMemoryHandler()
        self.instruction_memory.load_instructions(self.assembler.text_segment)
        self.data_memory = Memory()
        self.data_memory.load_datasegment(data_segment)

        self.pipeline = PipelineCoordinator(self.instruction_memory, self.data_memory)
        self.pipeline.initialize()
        self.clocks = 0

    def single_step(self):
        self.pipeline.single_step()
        self.clocks += 1


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    s = MIPSSimulator()
    w = MainWindow(simulator=s)
    w.init_ui()
    sys.exit(app.exec_())