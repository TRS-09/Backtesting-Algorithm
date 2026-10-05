from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class SettingsScreen(QWidget):
  go_home = Signal()
  settings_applied = Signal(dict)

  def __init__(self):
    super().__init__()

    # Main outer layout
    layout = QVBoxLayout()
    layout.setSpacing(15)
    layout.setContentsMargins(40, 20, 40, 20)

    # 1. Fixed Top Bar
    top_bar = QHBoxLayout()

    self.back_btn = self.build_back_button()
    top_bar.addWidget(self.back_btn)

    title_label = self.build_title()
    top_bar.addWidget(title_label, stretch=1)

    spacer = QWidget()
    spacer.setFixedWidth(100)
    top_bar.addWidget(spacer)

    layout.addLayout(top_bar)
    layout.addWidget(self.build_divider())

    # 2. Scrollable Middle Area for Settings Cards
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #2b2b2b;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

    # Container widget inside scroll area
    scroll_content = QWidget()
    scroll_content.setStyleSheet("background-color: transparent;")
    scroll_layout = QVBoxLayout(scroll_content)
    scroll_layout.setSpacing(15)
    scroll_layout.setContentsMargins(0, 0, 10, 0)

    scroll_layout.addWidget(self.build_rsi_box())
    scroll_layout.addWidget(self.build_ema_box())
    scroll_layout.addWidget(self.build_atr_box())
    scroll_layout.addStretch()

    scroll_area.setWidget(scroll_content)
    layout.addWidget(scroll_area, stretch=1)

    # 3. Fixed Bottom Action Bar
    layout.addWidget(self.build_divider())

    bottom_buttons = QHBoxLayout()
    bottom_buttons.setAlignment(Qt.AlignLeft)

    self.apply_btn = self.build_run_button()
    bottom_buttons.addWidget(self.apply_btn)

    layout.addLayout(bottom_buttons)

    self.setLayout(layout)

  # ------------------------------------------------------------
  # UI Builders & Shared Styles
  # ------------------------------------------------------------

  def build_back_button(self):
    btn = QPushButton("← Back")
    btn.setFixedWidth(100)
    btn.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                font-size: 16px;
                padding: 6px 0px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
    btn.clicked.connect(self.go_home.emit)
    return btn

  def build_title(self):
    label = QLabel("Strategy Settings")
    label.setStyleSheet("color: white;")
    label.setFont(QFont("Arial", 24, QFont.Bold))
    label.setAlignment(Qt.AlignCenter)
    return label

  def build_divider(self):
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("color: #444;")
    return line

  def get_combo_style(self):
    return """
            QComboBox {
                background-color: #2b2b2b;
                color: white;
                font-size: 15px;
                padding: 6px 10px;
                border: 1px solid #555;
                border-radius: 6px;
            }
            QComboBox:hover {
                border-color: #888;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #2b2b2b;
                color: white;
                selection-background-color: #555;
                border: 1px solid #555;
            }
        """

  # -----------------------------
  # RSI Settings Box
  # -----------------------------
  def build_rsi_box(self):
    frame = QFrame()
    frame.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
            }
        """)
    box = QVBoxLayout(frame)
    box.setSpacing(10)

    label = QLabel("RSI Settings")
    label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
    box.addWidget(label)

    # Overbought row
    row = QHBoxLayout()
    over_lbl = QLabel("Overbought:")
    over_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px;")

    self.rsi_over_box = QComboBox()
    self.rsi_over_box.setFixedWidth(140)
    self.rsi_over_box.addItems([str(i) for i in range(50, 105, 5)])
    self.rsi_over_box.setCurrentText("70")
    self.rsi_over_box.setStyleSheet(self.get_combo_style())

    row.addWidget(over_lbl)
    row.addStretch()
    row.addWidget(self.rsi_over_box)
    box.addLayout(row)

    # Oversold row
    row3 = QHBoxLayout()
    oversoldlbl = QLabel("Oversold:")
    oversoldlbl.setStyleSheet("color: #d0d0d0; font-size: 16px;")

    self.rsi_oversold_box = QComboBox()
    self.rsi_oversold_box.setFixedWidth(140)
    self.rsi_oversold_box.addItems([str(i) for i in range(5, 55, 5)])
    self.rsi_oversold_box.setCurrentText("30")
    self.rsi_oversold_box.setStyleSheet(self.get_combo_style())

    row3.addWidget(oversoldlbl)
    row3.addStretch()
    row3.addWidget(self.rsi_oversold_box)
    box.addLayout(row3)

    # RSI Period row
    row_period = QHBoxLayout()
    period_lbl = QLabel("RSI Period:")
    period_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px;")

    self.rsi_period_box = QComboBox()
    self.rsi_period_box.setFixedWidth(140)
    self.rsi_period_box.addItems(["7", "14", "21", "28", "50"])
    self.rsi_period_box.setCurrentText("14")
    self.rsi_period_box.setStyleSheet(self.get_combo_style())

    row_period.addWidget(period_lbl)
    row_period.addStretch()
    row_period.addWidget(self.rsi_period_box)
    box.addLayout(row_period)

    return frame

  # -----------------------------
  # EMA/SMA Settings Box
  # -----------------------------
  def build_ema_box(self):
    frame = QFrame()
    frame.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
            }
        """)
    box = QVBoxLayout(frame)
    box.setSpacing(10)

    label = QLabel("SMA Settings")
    label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
    box.addWidget(label)

    # Fast MA row
    row_fast = QHBoxLayout()
    fast_lbl = QLabel("Fast MA:")
    fast_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px;")

    self.sma_fast_box = QComboBox()
    self.sma_fast_box.setFixedWidth(140)
    self.sma_fast_box.addItems([str(i) for i in range(5, 31, 5)])
    self.sma_fast_box.setCurrentText("10")
    self.sma_fast_box.setStyleSheet(self.get_combo_style())

    row_fast.addWidget(fast_lbl)
    row_fast.addStretch()
    row_fast.addWidget(self.sma_fast_box)
    box.addLayout(row_fast)

    # Slow MA row
    row_slow = QHBoxLayout()
    slow_lbl = QLabel("Slow MA:")
    slow_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px;")

    self.sma_slow_box = QComboBox()
    self.sma_slow_box.setFixedWidth(140)
    self.sma_slow_box.addItems([str(i) for i in range(20, 101, 10)])
    self.sma_slow_box.setCurrentText("30")
    self.sma_slow_box.setStyleSheet(self.get_combo_style())

    row_slow.addWidget(slow_lbl)
    row_slow.addStretch()
    row_slow.addWidget(self.sma_slow_box)
    box.addLayout(row_slow)

    # Minimum days row
    row_min = QHBoxLayout()
    min_lbl = QLabel("Minimum Days:")
    min_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px;")

    self.sma_min_box = QComboBox()
    self.sma_min_box.setFixedWidth(140)
    self.sma_min_box.addItems(["5", "10", "14", "20", "30"])
    self.sma_min_box.setCurrentText("14")
    self.sma_min_box.setStyleSheet(self.get_combo_style())

    row_min.addWidget(min_lbl)
    row_min.addStretch()
    row_min.addWidget(self.sma_min_box)
    box.addLayout(row_min)

    return frame

  # -----------------------------
  # ATR Settings Box
  # -----------------------------
  def build_atr_box(self):
    frame = QFrame()
    frame.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px;
            }
        """)
    box = QVBoxLayout(frame)
    box.setSpacing(10)

    label = QLabel("ATR Settings")
    label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
    box.addWidget(label)

    # ATR Period Row
    row_period = QHBoxLayout()
    period_lbl = QLabel("ATR Period:")
    period_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px;")

    self.atr_period_box = QComboBox()
    self.atr_period_box.setFixedWidth(140)
    self.atr_period_box.addItems(["7", "10", "14", "21", "28"])
    self.atr_period_box.setCurrentText("14")
    self.atr_period_box.setStyleSheet(self.get_combo_style())

    row_period.addWidget(period_lbl)
    row_period.addStretch()
    row_period.addWidget(self.atr_period_box)
    box.addLayout(row_period)

    # ATR Multiplier Row
    row_mult = QHBoxLayout()
    mult_lbl = QLabel("ATR Multiplier (K-Factor):")
    mult_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px;")

    self.atr_mult_box = QComboBox()
    self.atr_mult_box.setFixedWidth(140)
    self.atr_mult_box.addItems(["1.0", "1.25", "1.5", "2.0", "2.5", "3.0"])
    self.atr_mult_box.setCurrentText("1.5")
    self.atr_mult_box.setStyleSheet(self.get_combo_style())

    row_mult.addWidget(mult_lbl)
    row_mult.addStretch()
    row_mult.addWidget(self.atr_mult_box)
    box.addLayout(row_mult)

    # Cooldown Days Row
    row_min = QHBoxLayout()
    min_lbl = QLabel("Minimum Cooldown Days:")
    min_lbl.setStyleSheet("color: #d0d0d0; font-size: 16px;")

    self.atr_cooldown_box = QComboBox()
    self.atr_cooldown_box.setFixedWidth(140)
    self.atr_cooldown_box.addItems(["0", "2", "5", "10", "14"])
    self.atr_cooldown_box.setCurrentText("2")
    self.atr_cooldown_box.setStyleSheet(self.get_combo_style())

    row_min.addWidget(min_lbl)
    row_min.addStretch()
    row_min.addWidget(self.atr_cooldown_box)
    box.addLayout(row_min)

    return frame

  def build_run_button(self):
    run_btn = QPushButton("Apply Settings")
    run_btn.setStyleSheet("""
            QPushButton {
                background-color: #388238;
                color: white;
                font-size: 16px;
                padding: 10px 24px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a045;
            }
        """)
    run_btn.clicked.connect(self.emit_settings)
    return run_btn

  # -----------------------------
  # Collect and Emit Settings
  # -----------------------------
  def emit_settings(self):
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

    self.settings_applied.emit(settings_data)