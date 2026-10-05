from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SettingsScreen(QWidget):
  go_home = Signal()
  # Define a signal that will carry all your settings as a dictionary
  settings_applied = Signal(dict)

  def __init__(self):
    super().__init__()

    layout = QVBoxLayout()
    layout.setSpacing(30)
    layout.setContentsMargins(40, 30, 40, 40)

    layout.addLayout(self.build_top_bar())
    layout.addWidget(self.build_divider())
    layout.addWidget(self.build_rsi_box())
    layout.addWidget(self.build_ema_box())
    layout.addWidget(self.build_atr_box())
    layout.addLayout(self.build_run_button())
    layout.addStretch()

    self.setLayout(layout)

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
    backBtn.clicked.connect(self.go_home.emit)

    row = QHBoxLayout()
    row.addWidget(backBtn)
    row.addStretch()
    row.addWidget(title)
    row.addStretch()
    return row

  def build_divider(self):
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("color: grey;")
    return line

  # -----------------------------
  # RSI Settings Box (Prefixed with self.)
  # -----------------------------
  def build_rsi_box(self):
    frame = QFrame()
    frame.setObjectName("RSIFrame")
    frame.setStyleSheet("""
            QFrame#RSIFrame { border: 5px solid grey; background-color: #323232; }
            QFrame#RSIFrame * { background-color: #323232; color: white; }
        """)
    box = QVBoxLayout(frame)

    label = QLabel("RSI Settings")
    label.setStyleSheet("color: white;")
    box.addWidget(label)

    # Overbought row
    row = QHBoxLayout()
    over_lbl = QLabel("Overbought:")
    over_lbl.setStyleSheet("color: white; padding: 5px;")

    # Changed to self.rsi_over_box
    self.rsi_over_box = QComboBox()
    self.rsi_over_box.addItems([str(i) for i in range(50, 105, 5)])
    self.rsi_over_box.setCurrentText("70")
    self.rsi_over_box.setStyleSheet(
        "QComboBox { color: white; padding: 5px; } QComboBox QAbstractItemView"
        " { color: white; }"
    )

    row.addWidget(over_lbl)
    row.addWidget(self.rsi_over_box)
    box.addLayout(row)

    # Oversold row
    row3 = QHBoxLayout()
    oversoldlbl = QLabel("Oversold:")
    oversoldlbl.setStyleSheet("color: white; padding: 5px;")

    # Changed to self.rsi_oversold_box
    self.rsi_oversold_box = QComboBox()
    self.rsi_oversold_box.addItems([str(i) for i in range(5, 55, 5)])
    self.rsi_oversold_box.setCurrentText("30")
    self.rsi_oversold_box.setStyleSheet(
        "QComboBox { color: white; padding: 5px; } QComboBox QAbstractItemView"
        " { color: white; }"
    )

    row3.addWidget(oversoldlbl)
    row3.addWidget(self.rsi_oversold_box)
    box.addLayout(row3)

    # RSI Period row
    row_period = QHBoxLayout()
    period_lbl = QLabel("RSI Period:")
    period_lbl.setStyleSheet("color: white; padding: 5px;")

    # Changed to self.rsi_period_box
    self.rsi_period_box = QComboBox()
    self.rsi_period_box.addItems(["7", "14", "21", "28", "50"])
    self.rsi_period_box.setCurrentText("14")
    self.rsi_period_box.setStyleSheet(
        "QComboBox { color: white; padding: 5px; } QComboBox QAbstractItemView"
        " { color: white; }"
    )

    row_period.addWidget(period_lbl)
    row_period.addWidget(self.rsi_period_box)
    box.addLayout(row_period)

    return frame

  # -----------------------------
  # EMA/SMA Settings Box (Prefixed with self.)
  # -----------------------------
  def build_ema_box(self):
    frame = QFrame()
    frame.setObjectName("EMAFrame")
    frame.setStyleSheet("""
            QFrame#EMAFrame { border: 5px solid grey; background-color: #323232; }
            QFrame#EMAFrame * { background-color: #323232; color: white; }
        """)
    box = QVBoxLayout(frame)

    label = QLabel("SMA Settings")
    label.setStyleSheet("color: white;")
    box.addWidget(label)

    # Fast MA row
    row_fast = QHBoxLayout()
    fast_lbl = QLabel("Fast MA:")
    fast_lbl.setStyleSheet("color: white; padding: 5px;")

    # Changed to self.sma_fast_box
    self.sma_fast_box = QComboBox()
    self.sma_fast_box.addItems([str(i) for i in range(5, 31, 5)])
    self.sma_fast_box.setCurrentText("10")
    self.sma_fast_box.setStyleSheet(
        "QComboBox { color: white; padding: 5px; } QComboBox QAbstractItemView"
        " { color: white; }"
    )

    row_fast.addWidget(fast_lbl)
    row_fast.addWidget(self.sma_fast_box)
    box.addLayout(row_fast)

    # Slow MA row
    row_slow = QHBoxLayout()
    slow_lbl = QLabel("Slow MA:")
    slow_lbl.setStyleSheet("color: white; padding: 5px;")

    # Changed to self.sma_slow_box
    self.sma_slow_box = QComboBox()
    self.sma_slow_box.addItems([str(i) for i in range(20, 101, 10)])
    self.sma_slow_box.setCurrentText("30")
    self.sma_slow_box.setStyleSheet(
        "QComboBox { color: white; padding: 5px; } QComboBox QAbstractItemView"
        " { color: white; }"
    )

    row_slow.addWidget(slow_lbl)
    row_slow.addWidget(self.sma_slow_box)
    box.addLayout(row_slow)

    # Minimum days row
    row_min = QHBoxLayout()
    min_lbl = QLabel("Minimum Days:")
    min_lbl.setStyleSheet("color: white; padding: 5px;")

    # Changed to self.sma_min_box
    self.sma_min_box = QComboBox()
    self.sma_min_box.addItems(["5", "10", "14", "20", "30"])
    self.sma_min_box.setCurrentText("14")
    self.sma_min_box.setStyleSheet(
        "QComboBox { color: white; padding: 5px; } QComboBox QAbstractItemView"
        " { color: white; }"
    )

    row_min.addWidget(min_lbl)
    row_min.addWidget(self.sma_min_box)
    box.addLayout(row_min)

    return frame

  # -----------------------------
  # ATR Settings Box (Prefixed with self.)
  # -----------------------------
  def build_atr_box(self):
    frame = QFrame()
    frame.setObjectName("ATRFrame")
    frame.setStyleSheet("""
            QFrame#ATRFrame { border: 5px solid grey; background-color: #323232; }
            QFrame#ATRFrame * { background-color: #323232; color: white; }
        """)
    box = QVBoxLayout(frame)

    label = QLabel("ATR Settings")
    label.setStyleSheet("color: white;")
    box.addWidget(label)

    # ATR Period Row
    row_period = QHBoxLayout()
    period_lbl = QLabel("ATR Period:")
    period_lbl.setStyleSheet("color: white; padding: 5px;")

    # Changed to self.atr_period_box
    self.atr_period_box = QComboBox()
    self.atr_period_box.addItems(["7", "10", "14", "21", "28"])
    self.atr_period_box.setCurrentText("14")
    self.atr_period_box.setStyleSheet(
        "QComboBox { color: white; padding: 5px; } QComboBox QAbstractItemView"
        " { color: white; }"
    )

    row_period.addWidget(period_lbl)
    row_period.addWidget(self.atr_period_box)
    box.addLayout(row_period)

    # ATR Multiplier Row
    row_mult = QHBoxLayout()
    mult_lbl = QLabel("ATR Multiplier (K-Factor):")
    mult_lbl.setStyleSheet("color: white; padding: 5px;")

    # Changed to self.atr_mult_box
    self.atr_mult_box = QComboBox()
    self.atr_mult_box.addItems(["1.0", "1.25", "1.5", "2.0", "2.5", "3.0"])
    self.atr_mult_box.setCurrentText("1.5")
    self.atr_mult_box.setStyleSheet(
        "QComboBox { color: white; padding: 5px; } QComboBox QAbstractItemView"
        " { color: white; }"
    )

    row_mult.addWidget(mult_lbl)
    row_mult.addWidget(self.atr_mult_box)
    box.addLayout(row_mult)

    # Cooldown Days Row
    row_min = QHBoxLayout()
    min_lbl = QLabel("Minimum Cooldown Days:")
    min_lbl.setStyleSheet("color: white; padding: 5px;")

    # Already self.min_box (let's rename to self.atr_cooldown_box for clarity)
    self.atr_cooldown_box = QComboBox()
    self.atr_cooldown_box.addItems(["0", "2", "5", "10", "14"])
    self.atr_cooldown_box.setCurrentText("2")
    self.atr_cooldown_box.setStyleSheet(
        "QComboBox { color: white; padding: 5px; } QComboBox QAbstractItemView"
        " { color: white; }"
    )

    row_min.addWidget(min_lbl)
    row_min.addWidget(self.atr_cooldown_box)
    box.addLayout(row_min)

    return frame

  def build_run_button(self):
    row = QHBoxLayout()
    row.addStretch()

    run_btn = QPushButton("Apply")
    run_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
    # Connect to the completion method below
    run_btn.clicked.connect(self.emit_settings)

    row.addWidget(run_btn)
    return row

  # -----------------------------
  # Collect and Emit Settings
  # -----------------------------
  def emit_settings(self):
    # Package all current dropdown selections into a dictionary
    settings_data = {
        "rsi_overbought": self.rsi_over_box.currentText(),
        "rsi_oversold": self.rsi_oversold_box.currentText(),
        "rsi_period": self.rsi_period_box.currentText(),
        "sma_fast": self.sma_fast_box.currentText(),
        "sma_slow": self.sma_slow_box.currentText(),
        "sma_min_days": self.sma_min_box.currentText(),
        "atr_period": self.atr_period_box.currentText(),
        "atr_multiplier": self.atr_mult_box.currentText(),
        "atr_cooldown": self.atr_cooldown_box.currentText(),
    }

    # Emit the dictionary out via the signal
    self.settings_applied.emit(settings_data)