from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class InstructionView(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def update_view(self, assembler):
        self.setText(assembler.repr_instructions())