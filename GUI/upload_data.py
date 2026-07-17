from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

class loadCSV(QWidget):
    go_home = Signal()
    csv_loaded = Signal(bool)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        testbtn = QPushButton("test")
        testbtn.setStyleSheet("background-color: black;")

        # Emit True when clicked
        testbtn.clicked.connect(lambda: self.csv_loaded.emit(True))

        # Go home
        testbtn.clicked.connect(self.go_home.emit)

        layout.addWidget(testbtn)
        self.setLayout(layout)
