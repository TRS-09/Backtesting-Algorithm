from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QHBoxLayout, QFrame, QTextEdit
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

# Matplotlib integration imports
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Results(QWidget):
    # Navigation signals
    go_home = Signal()

    def __init__(self):
        super().__init__()

        # Main layout setup
        main = QVBoxLayout()
        main.setSpacing(25)
        main.setContentsMargins(40, 30, 40, 40)

        # Top bar with back button, centered title, and spacer for layout symmetry
        top_bar = QHBoxLayout()

        self.back_btn = self.build_back_button()
        top_bar.addWidget(self.back_btn)

        title_label = self.build_title()
        top_bar.addWidget(title_label, stretch=1)

        spacer = QWidget()
        spacer.setFixedWidth(100)
        top_bar.addWidget(spacer)

        main.addLayout(top_bar)
        main.addWidget(self.build_divider())

        # Content split: Graph area on left, Text summary on right
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        self.graph_container = self.build_graph_panel()
        self.text_container = self.build_text_panel()

        content_layout.addWidget(self.graph_container, stretch=3)
        content_layout.addWidget(self.text_container, stretch=2)

        main.addLayout(content_layout, stretch=1)

        # Bottom section with save option
        main.addWidget(self.build_divider())

        bottom_buttons = QHBoxLayout()
        bottom_buttons.setAlignment(Qt.AlignLeft)
        bottom_buttons.setSpacing(15)

        self.save_btn = self.build_save_button()
        bottom_buttons.addWidget(self.save_btn)

        main.addLayout(bottom_buttons)

        self.setLayout(main)

    # ------------------------------------------------------------
    # UI Builders
    # ------------------------------------------------------------

    def build_back_button(self):
        btn = QPushButton("← Back")
        btn.setFixedWidth(100)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                font-size: 18px;
                padding: 8px 0px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        btn.clicked.connect(self.go_home.emit)
        return btn

    def build_title(self):
        label = QLabel("Results")
        label.setStyleSheet("color: white;")
        label.setFont(QFont("Arial", 28, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        return label

    def build_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: grey;")
        return line

    def build_graph_panel(self):
        layout = QVBoxLayout()

        header = QLabel("📈 Matplotlib Graph")
        header.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

        # 1. Create Matplotlib Figure & Subplot styled for dark theme
        self.fig = Figure(facecolor='#2b2b2b')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#2b2b2b')
        
        # Style axis lines, ticks, and labels for dark mode visibility
        self.ax.tick_params(colors='#d0d0d0', labelsize=10)
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#555')

        # 2. Create the Canvas widget
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border: 1px solid #555;
                border-radius: 6px;
            }
        """)

        widget = QWidget()
        widget.setLayout(layout)
        layout.addWidget(header)
        layout.addWidget(self.canvas, stretch=1)

        return widget

    def build_text_panel(self):
        layout = QVBoxLayout()

        header = QLabel("📋 Output Details")
        header.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

        # Styled text box for summary output / log text
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setPlaceholderText("Results output text will appear here...")
        self.text_box.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #d0d0d0;
                font-size: 16px;
                padding: 12px;
                border: 1px solid #555;
                border-radius: 6px;
            }
        """)

        widget = QWidget()
        widget.setLayout(layout)
        layout.addWidget(header)
        layout.addWidget(self.text_box, stretch=1)

        return widget

    def build_save_button(self):
        btn = QPushButton("Save Results")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #388238;
                color: white;
                font-size: 18px;
                padding: 10px 24px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a045;
            }
        """)
        return btn

    # ------------------------------------------------------------
    # Graph Plotting Helper
    # ------------------------------------------------------------
    def update_graph(self, series_list, title="Portfolio Performance"):
            self.ax.clear()
            
            # Loop through each series and plot it
            for series in series_list:
                x = series.get("x")
                y = series.get("y")
                label = series.get("label", "")
                color = series.get("color", None)
                
                self.ax.plot(x, y, label=label, color=color, linewidth=2)
                
            self.ax.set_title(title, color='white', fontsize=12, pad=10)
            
            # Re-apply dark theme styling after clearing axes
            self.ax.set_facecolor('#2b2b2b')
            self.ax.tick_params(colors='#d0d0d0', labelsize=10)
            for spine in self.ax.spines.values():
                spine.set_edgecolor('#555')
                
            # Add a styled legend if labels are provided
            if any(s.get("label") for s in series_list):
                legend = self.ax.legend(
                    facecolor='#323232', 
                    edgecolor='#555', 
                    labelcolor='white',
                    fontsize=10
                )
                
            self.fig.tight_layout()
            self.canvas.draw()