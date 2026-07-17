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
        self.strategysettingsbtn = QPushButton("Strategy Settings")
        self.strategysettingsbtn.setFont(QFont("arial", 18))
        self.strategysettingsbtn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9db;
                padding: 25px 10px;
                color: black;
            }
        """)
        self.strategysettingsbtn.clicked.connect(self.go_settings.emit)
        row1.addWidget(self.strategysettingsbtn)

        row1.addWidget(QLabel("Alter settings for RSI, MA such as period, overbuy/oversell"))

        layout.addLayout(row1)

        #CSV input
        row2 = QHBoxLayout()
        CSVbtn = QPushButton("Enter CSV")
        CSVbtn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9db;
                padding: 25px 10px;
                color: black;
            }
        """)
        CSVbtn.setFont(QFont("arial", 18))
        CSVbtn.clicked.connect(self.go_CSV.emit)

        row2.addWidget(CSVbtn)
        row2.addWidget(QLabel("Input your CSV of choice, then validate it!"))
        layout.addLayout(row2)

        #results button/text
        row3 = QHBoxLayout()

        resultsBtn = QPushButton("Results")
        resultsBtn.setStyleSheet("""
            QPushButton {
                background-color: red;
                padding: 25px 10px;
                color: white;
            }
        """)
        resultsBtn.setFont(QFont("arial", 18))

        row3.addWidget(resultsBtn)
        row3.addWidget(QLabel("See results and analysis of backtest"))
        layout.addLayout(row3)

        # backtest button
        layout.addSpacing(120)
        backtestrow = QHBoxLayout()
        backtestrow.addStretch()
        backtestBtn = QPushButton("Run Backtest")
        backtestBtn.setStyleSheet("""QPushButton { 
                                            background-color: red;
                                  }""")
        backtestBtn.setFixedWidth(100)
        backtestrow.addWidget(backtestBtn)
        backtestrow.addStretch()

        layout.addLayout(backtestrow)


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
