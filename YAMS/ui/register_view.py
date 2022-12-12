from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class RegisterView(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("")
        self.setReadOnly(True)
