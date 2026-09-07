from PySide6.QtWidgets import QComboBox, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class SettingsScreen(QWidget):
    go_home = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(40, 30, 40, 40)

        layout.addLayout(self.build_top_bar())
        layout.addWidget(self.build_divider())
        layout.addWidget(self.build_rsi_box())
        layout.addWidget(self.build_ema_box())
        layout.addLayout(self.build_run_button())
        layout.addStretch()

        self.setLayout(layout)

    # -----------------------------
    # Top bar (Back + Title)
    # -----------------------------
    def build_top_bar(self):
        title = QLabel("Strategy Settings")
        title.setStyleSheet("color: white;")
        title.setFont(QFont("arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        backBtn = QPushButton("Back")
        backBtn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9db;
                padding: 5px 10px;
                color: black;
            }
        """)

        row = QHBoxLayout()
        row.addWidget(backBtn)
        row.addStretch()
        row.addWidget(title)
        row.addStretch()

        return row

    # -----------------------------
    # Divider
    # -----------------------------
    def build_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: grey;")
        return line

    # -----------------------------
    # RSI Settings Box
    # -----------------------------
    def build_rsi_box(self):
        frame = QFrame()
        frame.setObjectName("RSIFrame")
        frame.setStyleSheet("""
            QFrame#RSIFrame {
                border: 5px solid grey;
                background-color: #323232;
            }
            QFrame#RSIFrame * {
                background-color: #323232;
                color: white;
            }
        """)

        box = QVBoxLayout(frame)

        # Title
        label = QLabel("RSI Settings")
        label.setStyleSheet("color: white;")
        box.addWidget(label)

        # Overbought row
        row = QHBoxLayout()

        over_lbl = QLabel("Overbought:")
        over_lbl.setStyleSheet("color: white; padding: 5px;")

        over_box = QComboBox()
        over_box.addItems([str(i) for i in range(50, 105, 5)])
        over_box.setCurrentText("70")
        over_box.setStyleSheet("""
            QComboBox {
                color: white;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                color: white;
            }
        """)

        row.addWidget(over_lbl)
        row.addWidget(over_box)
        box.addLayout(row)

        # Oversold row
        row3 = QHBoxLayout()

        oversoldlbl = QLabel("Oversold:")
        oversoldlbl.setStyleSheet("color: white; padding: 5px;")

        oversoldbox = QComboBox()
        oversold_items = [str(i) for i in range(5, 55, 5)]
        oversoldbox.addItems(oversold_items)
        oversoldbox.setCurrentText("30")

        oversoldbox.setStyleSheet("""
            QComboBox {
                color: white;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                color: white;
            }
        """)

        row3.addWidget(oversoldlbl)
        row3.addWidget(oversoldbox)
        box.addLayout(row3)

        # RSI Period row
        row_period = QHBoxLayout()

        period_lbl = QLabel("RSI Period:")
        period_lbl.setStyleSheet("color: white; padding: 5px;")

        period_box = QComboBox()
        period_box.addItems(["7", "14", "21", "28", "50"])
        period_box.setCurrentText("14")   # industry standard
        period_box.setStyleSheet("""
            QComboBox {
                color: white;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                color: white;
            }
        """)

        row_period.addWidget(period_lbl)
        row_period.addWidget(period_box)
        box.addLayout(row_period)

        return frame


    def build_ema_box(self):
        #initial setup for EMA settings box
        
        frame = QFrame()
        frame.setObjectName("EMAFrame")
        frame.setStyleSheet("""
            QFrame#EMAFrame {
                border: 5px solid grey;
                background-color: #323232;
            }
            QFrame#EMAFrame * {
                background-color: #323232;
                color: white;
            }
        """)
        box = QVBoxLayout(frame)

        # Title
        label = QLabel("SMA Settings")
        label.setStyleSheet("color: white;")
        box.addWidget(label)
        
        # Fast MA row
        row_fast = QHBoxLayout()

        fast_lbl = QLabel("Fast MA:")
        fast_lbl.setStyleSheet("color: white; padding: 5px;")

        fast_box = QComboBox()
        fast_box.addItems([str(i) for i in range(5, 31, 5)])   # 5, 10, 15, 20, 25, 30
        fast_box.setCurrentText("10")
        fast_box.setStyleSheet("""
            QComboBox {
                color: white;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                color: white;
            }
        """)

        row_fast.addWidget(fast_lbl)
        row_fast.addWidget(fast_box)
        box.addLayout(row_fast)


        # Slow MA row
        row_slow = QHBoxLayout()

        slow_lbl = QLabel("Slow MA:")
        slow_lbl.setStyleSheet("color: white; padding: 5px;")

        slow_box = QComboBox()
        slow_box.addItems([str(i) for i in range(20, 101, 10)])  # 20, 30, 40, ..., 100
        slow_box.setCurrentText("30")
        slow_box.setStyleSheet("""
            QComboBox {
                color: white;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                color: white;
            }
        """)

        row_slow.addWidget(slow_lbl)
        row_slow.addWidget(slow_box)
        box.addLayout(row_slow)

        # Minimum days row
        row_min = QHBoxLayout()

        min_lbl = QLabel("Minimum Days:")
        min_lbl.setStyleSheet("color: white; padding: 5px;")

        min_box = QComboBox()
        min_box.addItems(["5","10","14","20","30"])  
        min_box.setCurrentText("14")
        min_box.setStyleSheet("""
            QComboBox {
                color: white;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                color: white;
            }
        """)

        row_min.addWidget(min_lbl)
        row_min.addWidget(min_box)
        box.addLayout(row_min)

        return frame        


    def build_run_button(self):
        row = QHBoxLayout()
        row.addStretch()   # pushes button to the right

        run_btn = QPushButton("Run")
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        row.addWidget(run_btn)
        return row



        
        