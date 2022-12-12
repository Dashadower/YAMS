from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MemoryView(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("")
        self.setReadOnly(True)
