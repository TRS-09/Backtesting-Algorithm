from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class SettingsScreen(QWidget):
    go_home = Signal()

    def __init__(self):
        super().__init__()
        home = QPushButton("test")
        home.setStyleSheet("""background-color: grey;""")
        layout2 = QVBoxLayout()
        home.clicked.connect(self.go_home.emit)
        layout2.addWidget(home)

        self.setLayout(layout2)