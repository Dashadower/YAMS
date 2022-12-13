from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from YAMS.utils import string_numeric_to_decimal

class MemoryView(QWidget):
    def __init__(self, parent=None, simulator=None):
        super().__init__(parent)
        self.simulator = simulator
        main_layout = QVBoxLayout(self)

        button_layout = QHBoxLayout()
        self.addr_entry = QLineEdit()
        self.submit_btn = QPushButton()
        self.submit_btn.setText("Go")
        self.submit_btn.clicked.connect(self.on_submit)
        button_layout.addWidget(self.addr_entry)
        button_layout.addWidget(self.submit_btn)

        self.representation = "Decimal"
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

        self.textarea = QTextEdit()
        self.textarea.setText("")
        self.textarea.setReadOnly(True)
        font = QFont("Monospace")
        # font.setStyleHint(QFont.TypeWriter)
        self.textarea.setCurrentFont(font)

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.textarea)

        self.setLayout(main_layout)

    def change_representation(self, btn):
        self.representation = btn.text()
        if self.simulator.data_memory:
            self.update_view(self.simulator.data_memory)

    def on_submit(self, event):
        if self.simulator.data_memory:
            self.update_view(self.simulator.data_memory)

    def update_view(self, data_memory):
        self.textarea.setText(data_memory.get_wordview(string_numeric_to_decimal(self.addr_entry.text()), representation=self.representation.lower()))

