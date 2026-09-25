from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QHBoxLayout, QFrame, QCheckBox, QDoubleSpinBox, QSpinBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class HomeScreen(QWidget):
    # Navigation signals
    go_settings = Signal()
    go_CSV = Signal()
    go_results = Signal()

    def __init__(self):
        super().__init__()

        # Main layout setup
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 30, 40, 40)

        # Header section
        layout.addWidget(self.build_title())
        layout.addWidget(self.build_divider())
        layout.addWidget(self.build_welcome_text())
        layout.addSpacing(10)

        # Navigation options
        layout.addLayout(self.build_strategy_row())
        layout.addLayout(self.build_csv_row())
        layout.addLayout(self.build_results_row())

        # Account & Risk Settings panel
        layout.addSpacing(10)
        layout.addWidget(self.build_portfolio_box())

        # Action section
        layout.addStretch()
        layout.addLayout(self.build_backtest_row())
        layout.addStretch()

        # Footer section
        layout.addWidget(self.build_bottom_divider())
        layout.addWidget(self.build_version_text())

        self.setLayout(layout)

    # ------------------------------------------------------------
    # UI Builders
    # ------------------------------------------------------------

    def build_title(self):
        title = QLabel("Stock Backtesting Tool")
        title.setStyleSheet("color: white;")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        return title

    def build_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: grey;")
        return line

    def build_welcome_text(self):
        welcometxt = QLabel("Welcome! Select an option below to set up your backtest.")
        welcometxt.setStyleSheet("color: #d0d0d0; font-size: 18px;")
        welcometxt.setAlignment(Qt.AlignCenter)
        return welcometxt

    def build_strategy_row(self):
        row = QHBoxLayout()
        row.setSpacing(20)

        self.strategysettingsbtn = QPushButton("Strategy Settings")
        self.strategysettingsbtn.setFixedWidth(240)
        self.strategysettingsbtn.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                font-size: 20px;
                padding: 22px 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.strategysettingsbtn.clicked.connect(self.go_settings.emit)

        label = QLabel("Alter settings for RSI, MA periods, overbought/oversold levels")
        label.setStyleSheet("color: #d0d0d0; font-size: 16px;")

        row.addWidget(self.strategysettingsbtn)
        row.addWidget(label)

        return row

    def build_csv_row(self):
        row = QHBoxLayout()
        row.setSpacing(20)

        csv_btn = QPushButton("Enter CSV")
        csv_btn.setFixedWidth(240)
        csv_btn.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                font-size: 20px;
                padding: 22px 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        csv_btn.clicked.connect(self.go_CSV.emit)

        label = QLabel("Input your CSV of choice, then validate it!")
        label.setStyleSheet("color: #d0d0d0; font-size: 16px;")

        row.addWidget(csv_btn)
        row.addWidget(label)

        return row

    def build_results_row(self):
        row = QHBoxLayout()
        row.setSpacing(20)

        results_btn = QPushButton("Results")
        results_btn.setFixedWidth(240)
        results_btn.setStyleSheet("""
            QPushButton {
                background-color: #823838;
                color: white;
                font-size: 20px;
                padding: 22px 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #9E4343;
            }
        """)
        results_btn.clicked.connect(self.go_results.emit)

        label = QLabel("See results and visual analysis of backtests")
        label.setStyleSheet("color: #d0d0d0; font-size: 16px;")

        row.addWidget(results_btn)
        row.addWidget(label)

        return row

    def build_portfolio_box(self):
        frame = QFrame()
        frame.setObjectName("PortfolioFrame")
        frame.setStyleSheet("""
            QFrame#PortfolioFrame {
                background-color: #222222;
                border: 1px solid #444444;
                border-radius: 8px;
            }
            QFrame#PortfolioFrame QLabel {
                background-color: transparent;
            }
            QFrame#PortfolioFrame QCheckBox {
                background-color: transparent;
            }
        """)

        main_box = QVBoxLayout(frame)
        main_box.setContentsMargins(20, 16, 20, 16)
        main_box.setSpacing(14)

        header = QLabel("Account & Risk Settings")
        header.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background: transparent;")
        main_box.addWidget(header)

        controls_row = QHBoxLayout()
        controls_row.setSpacing(35)

        # 1. Checkbox
        self.fees_checkbox = QCheckBox("Include Fees")
        self.fees_checkbox.setChecked(True)
        self.fees_checkbox.setStyleSheet("""
            QCheckBox {
                color: #d0d0d0;
                font-size: 16px;
                spacing: 8px;
                background: transparent;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #555;
                background-color: #141414;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #388238;
                border: 1px solid #45a045;
            }
        """)

        # 2. Initial Cash Input
        cash_layout = QHBoxLayout()
        cash_lbl = QLabel("Initial Cash:")
        cash_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px; background: transparent;")

        self.cash_box = QDoubleSpinBox()
        self.cash_box.setRange(100.0, 10000000.0)
        self.cash_box.setValue(10000.0)
        self.cash_box.setSingleStep(1000.0)
        self.cash_box.setPrefix("$ ")
        self.cash_box.setStyleSheet("""
            QDoubleSpinBox {
                color: white;
                background-color: #141414;
                border: 1px solid #444;
                padding: 6px 10px;
                border-radius: 4px;
                font-size: 15px;
            }
        """)
        cash_layout.addWidget(cash_lbl)
        cash_layout.addWidget(self.cash_box)

        # 3. Risk Percentage Input
        risk_layout = QHBoxLayout()
        risk_lbl = QLabel("Risk per Trade:")
        risk_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px; background: transparent;")

        self.risk_box = QSpinBox()
        self.risk_box.setRange(0, 100)
        self.risk_box.setValue(10)
        self.risk_box.setSuffix("%")
        self.risk_box.setStyleSheet("""
            QSpinBox {
                color: white;
                background-color: #141414;
                border: 1px solid #444;
                padding: 6px 10px;
                border-radius: 4px;
                font-size: 15px;
            }
        """)
        risk_layout.addWidget(risk_lbl)
        risk_layout.addWidget(self.risk_box)

        controls_row.addWidget(self.fees_checkbox)
        controls_row.addLayout(cash_layout)
        controls_row.addLayout(risk_layout)
        controls_row.addStretch()

        main_box.addLayout(controls_row)

        return frame

    def build_backtest_row(self):
        row = QHBoxLayout()
        row.setAlignment(Qt.AlignCenter)

        backtest_btn = QPushButton("Run Backtest")
        backtest_btn.setStyleSheet("""
            QPushButton {
                background-color: #823838;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 16px 48px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #9E4343;
            }
        """)

        row.addWidget(backtest_btn)
        return row

    def build_bottom_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: grey;")
        return line

    def build_version_text(self):
        version = QLabel("Version 1.0 - Teo Smith")
        version.setStyleSheet("color: #888; font-size: 14px;")
        version.setAlignment(Qt.AlignCenter)
        return version

    # ------------------------------------------------------------
    # State updates
    # ------------------------------------------------------------

    def updatestrategyButtonColor(self, loaded: bool):
        if loaded:
            self.strategysettingsbtn.setStyleSheet("""
                QPushButton {
                    background-color: #388238;
                    color: white;
                    font-size: 20px;
                    padding: 22px 10px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #45a045;
                }
            """)
            print("//// CSV LOADED — BUTTON GREEN")
        else:
            self.strategysettingsbtn.setStyleSheet("""
                QPushButton {
                    background-color: #555;
                    color: white;
                    font-size: 20px;
                    padding: 22px 10px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
            """)
            print("... CSV NOT LOADED")