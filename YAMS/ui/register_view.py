from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class RegisterView(QWidget):
    def __init__(self, parent=None, simulator=None):
        super().__init__(parent)
        self.representation = "Decimal"
        self.simulator = simulator
        layout = QVBoxLayout(self)
        self.textarea = QTextEdit()
        self.textarea.setText("")
        self.textarea.setReadOnly(True)
        font = QFont("Monospace")
        #font.setStyleHint(QFont.TypeWriter)
        self.textarea.setCurrentFont(font)

        button_layout = QHBoxLayout()
        self.representation_group = QButtonGroup(self)
        dec_btn = QRadioButton("Decimal")
        dec_btn.setChecked(True)
        self.representation_group.addButton(dec_btn)
        hex_btn = QRadioButton("Hex")
        self.representation_group.addButton(hex_btn)
        bin_btn = QRadioButton("Binary")
        self.representation_group.addButton(bin_btn)
        button_layout.addWidget(dec_btn)
        button_layout.addWidget(hex_btn)
        button_layout.addWidget(bin_btn)
        self.representation_group.buttonClicked.connect(self.change_representation)

        layout.addLayout(button_layout)
        layout.addWidget(self.textarea)

        self.setLayout(layout)

    def change_representation(self, btn):
        self.representation = btn.text()
        if self.simulator:
            self.update_view(self.simulator.pipeline)

    def update_view(self, pipeline_c):
        if self.representation == "Decimal":
            self.textarea.setText(pipeline_c.ID_MainRegister.__repr__())
        elif self.representation == "Hex":
            self.textarea.setText(pipeline_c.ID_MainRegister.repr_hex())
        else:
            self.textarea.setText(pipeline_c.ID_MainRegister.repr_binary())
