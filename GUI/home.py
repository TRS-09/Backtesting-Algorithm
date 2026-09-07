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

        layout.addWidget(self.build_title())
        layout.addWidget(self.build_divider())
        layout.addWidget(self.build_welcome_text())
        layout.addSpacing(40)
        layout.addLayout(self.build_strategy_row())
        layout.addLayout(self.build_csv_row())
        layout.addLayout(self.build_results_row())
        layout.addSpacing(120)
        layout.addLayout(self.build_backtest_row())
        layout.addStretch()
        layout.addWidget(self.build_bottom_divider())
        layout.addWidget(self.build_version_text())

        self.setLayout(layout)

    # -----------------------------
    # Title
    # -----------------------------
    def build_title(self):
        title = QLabel("Stock Backtesting Tool")
        title.setStyleSheet("color: white;")
        title.setFont(QFont("arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        return title

    # -----------------------------
    # Divider
    # -----------------------------
    def build_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: grey;")
        return line

    # -----------------------------
    # Welcome text
    # -----------------------------
    def build_welcome_text(self):
        welcometxt = QLabel("Welcome! Good luck backtesting :)")
        welcometxt.setStyleSheet("color: white;")
        welcometxt.setAlignment(Qt.AlignCenter)
        return welcometxt

    # -----------------------------
    # Strategy Settings row
    # -----------------------------
    def build_strategy_row(self):
        row = QHBoxLayout()

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

        label = QLabel("Alter settings for RSI, MA such as period, overbuy/oversell")
        label.setStyleSheet("color: white;")

        row.addWidget(self.strategysettingsbtn)
        row.addWidget(label)

        return row

    # -----------------------------
    # CSV input row
    # -----------------------------
    def build_csv_row(self):
        row = QHBoxLayout()

        CSVbtn = QPushButton("Enter CSV")
        CSVbtn.setFont(QFont("arial", 18))
        CSVbtn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9db;
                padding: 25px 10px;
                color: black;
            }
        """)
        CSVbtn.clicked.connect(self.go_CSV.emit)

        label = QLabel("Input your CSV of choice, then validate it!")
        label.setStyleSheet("color: white;")

        row.addWidget(CSVbtn)
        row.addWidget(label)

        return row

    # -----------------------------
    # Results row
    # -----------------------------
    def build_results_row(self):
        row = QHBoxLayout()

        resultsBtn = QPushButton("Results")
        resultsBtn.setFont(QFont("arial", 18))
        resultsBtn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9db;
                padding: 25px 10px;
                color: black;
            }
        """)

        label = QLabel("See results and analysis of backtest")
        label.setStyleSheet("color: white;")

        row.addWidget(resultsBtn)
        row.addWidget(label)

        return row

    # -----------------------------
    # Backtest button row
    # -----------------------------
    def build_backtest_row(self):
        row = QHBoxLayout()
        row.addStretch()

        backtestBtn = QPushButton("Run Backtest")
        backtestBtn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9db;
                color: black;
            }
        """)
        backtestBtn.setFixedWidth(100)

        row.addWidget(backtestBtn)
        row.addStretch()

        return row

    # -----------------------------
    # Bottom divider
    # -----------------------------
    def build_bottom_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: grey;")
        return line

    # -----------------------------
    # Version text
    # -----------------------------
    def build_version_text(self):
        version = QLabel("Version 1.0 - Teo Smith")
        version.setStyleSheet("color: white;")
        version.setAlignment(Qt.AlignCenter)
        return version

    # -----------------------------
    # Logic unchanged
    # -----------------------------
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
