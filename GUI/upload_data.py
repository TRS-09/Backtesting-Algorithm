from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class loadCSV(QWidget):
    go_home = Signal()
    csv_loaded = Signal(bool)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # title
        layout.addWidget(QLabel(""))
