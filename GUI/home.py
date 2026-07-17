from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class HomeScreen(QWidget):
    go_settings = Signal()
    go_CSV = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(40, 30, 40, 40)

        # Title
        title = QLabel("Stock Backtesting Tool")
        title.setFont(QFont("arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: grey;")
        layout.addWidget(line)

        # Welcome text
        welcometxt = QLabel("Welcome! Good luck backtesting :)")
        welcometxt.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcometxt)

        layout.addSpacing(40)

        # CSV row
        row1 = QHBoxLayout()
        self.strategysettingsbtn = QPushButton("Strategy Settings")   # THIS is the button you want to update
        self.strategysettingsbtn.setFont(QFont("arial", 18))
        self.strategysettingsbtn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9db;
                padding: 25px 10px;
            }
        """)
        self.strategysettingsbtn.clicked.connect(self.go_settings.emit)
        row1.addWidget(self.strategysettingsbtn)

        row1.addWidget(QLabel("Alter settings for RSI, MA such as period, overbuy/oversell"))

        layout.addLayout(row1)

        # add buttons/text -------------

        layout.addStretch()

        # Bottom divider
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("color: grey;")
        layout.addWidget(line2)

        # Version text
        version = QLabel("Version 1.0 - Teo Smith")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        self.setLayout(layout)

    def updatestrategyButtonColor(self, loaded: bool):
        if loaded:
            self.strategysettingsbtn.setStyleSheet("""
                QPushButton {
                    background-color: #7ed957;
                    padding: 25px 10px;
                }
            """)
            print("//// CSV LOADED — BUTTON GREEN")
        else:
            print("... CSV NOT LOADED")
