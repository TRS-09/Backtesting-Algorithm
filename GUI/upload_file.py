from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame, QFileDialog, QComboBox
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont
from Logic.csv_processing import ProcessCSV


class loadCSV(QWidget):
    # Navigation signals
    go_home = Signal()
    csv_loaded = Signal(bool)
    go_settings = Signal()

    def __init__(self):
        super().__init__()

        # State variables
        self.file_path = None
        self.CSV = None
        self.start_year = None
        self.end_year = None

        # Main layout setup
        main = QVBoxLayout()
        main.setSpacing(30)
        main.setContentsMargins(40, 30, 40, 40)

        # Top bar with back button, centered title, and a dummy spacer to keep alignment true
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
        main.addWidget(self.build_dragndrop())
        main.addWidget(self.build_browse_button())

        # Selected file & detected columns info
        main.addWidget(self.build_file_panel())
        main.addWidget(self.build_columns_panel())

        # Container for start/end year dropdowns (built dynamically post-load)
        self.year_area = QWidget()
        self.year_layout = QVBoxLayout()
        self.year_area.setLayout(self.year_layout)
        main.addWidget(self.year_area)

        # Bottom action buttons
        main.addStretch()
        main.addWidget(self.build_divider())

        bottom_buttons = QHBoxLayout()
        bottom_buttons.setAlignment(Qt.AlignLeft)
        bottom_buttons.setSpacing(15)

        self.validate_btn = self.build_validate_button()
        bottom_buttons.addWidget(self.validate_btn)

        self.switch_btn = self.build_switch_button()
        bottom_buttons.addWidget(self.switch_btn)

        main.addLayout(bottom_buttons)

        # Enable file drag-and-drop
        self.setAcceptDrops(True)
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
        label = QLabel("Upload CSV")
        label.setStyleSheet("color:white;")
        label.setFont(QFont("Arial", 28, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        return label

    def build_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color:grey;")
        return line

    def build_dragndrop(self):
        self.dragndrop = QLabel("Drag & Drop")
        self.dragndrop.setAlignment(Qt.AlignCenter)
        self.dragndrop.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                padding: 60px;
                font-size: 18px;
                color: white;
            }
        """)
        return self.dragndrop

    def build_browse_button(self):
        btn = QPushButton("Browse files")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #d9d9db;
                padding: 25px 10px;
                color: black;
                font-size: 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ececec;
            }
        """)
        btn.clicked.connect(self.open_file_dialog)
        return btn

    def build_file_panel(self):
        layout = QVBoxLayout()

        title = QLabel("📄 File Selected")
        title.setStyleSheet("color:white; font-size:22px; font-weight:bold;")

        self.file_label = QLabel("None")
        self.file_label.setStyleSheet("""
            color:#d0d0d0;
            font-size:18px;
            padding:8px;
            background-color:#2b2b2b;
            border-radius:6px;
        """)

        widget = QWidget()
        widget.setLayout(layout)
        layout.addWidget(title)
        layout.addWidget(self.file_label)

        return widget

    def build_columns_panel(self):
        layout = QVBoxLayout()

        title = QLabel("🧩 Columns Detected")
        title.setStyleSheet("color:white; font-size:22px; font-weight:bold;")

        self.columns_label = QLabel("None")
        self.columns_label.setStyleSheet("""
            color:#d0d0d0;
            font-size:18px;
            padding:8px;
            background-color:#2b2b2b;
            border-radius:6px;
        """)

        widget = QWidget()
        widget.setLayout(layout)
        layout.addWidget(title)
        layout.addWidget(self.columns_label)

        return widget

    def build_validate_button(self):
        btn = QPushButton("Validate")
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
        btn.clicked.connect(self.on_validate_clicked)
        return btn

    def build_switch_button(self):
        self.btn = QPushButton("Settings")
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                font-size: 18px;
                padding: 10px 24px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.btn.clicked.connect(self.go_settings.emit)
        return self.btn

    # ------------------------------------------------------------
    # File loading + year dropdowns
    # ------------------------------------------------------------

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "CSV Files (*.csv)")
        if not path:
            return

        self.file_path = path
        self.file_label.setText(path)

        self.CSV = ProcessCSV(path)
        self.build_year_dropdowns()

    def build_year_dropdowns(self):
        # Clear existing widgets before rebuilding
        while self.year_layout.count():
            item = self.year_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        min_year, max_year = self.CSV.year_range()

        # Shared style for dark-themed dropdowns
        combo_style = """
            QComboBox {
                background-color: #2b2b2b;
                color: white;
                font-size: 16px;
                padding: 8px 12px;
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

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(15)

        # Start year dropdown
        start_label = QLabel("Start at:")
        start_label.setStyleSheet("color:white; font-size:18px;")

        self.start_dropdown = QComboBox()
        self.start_dropdown.setFixedWidth(140)
        self.start_dropdown.setStyleSheet(combo_style)
        self.start_dropdown.addItems([str(y) for y in range(min_year, max_year)])

        # End year dropdown
        end_label = QLabel("End at:")
        end_label.setStyleSheet("color:white; font-size:18px;")

        self.end_dropdown = QComboBox()
        self.end_dropdown.setFixedWidth(140)
        self.end_dropdown.setStyleSheet(combo_style)
        self.end_dropdown.addItems([str(y) for y in range(min_year + 1, max_year + 1)])

        # Update valid end years when start year changes
        self.start_dropdown.currentIndexChanged.connect(self.update_end_dropdown)

        row.addWidget(start_label)
        row.addWidget(self.start_dropdown)
        row.addSpacing(15)
        row.addWidget(end_label)
        row.addWidget(self.end_dropdown)
        row.addStretch()

        self.year_layout.addLayout(row)

    def update_end_dropdown(self):
        # Keep end year range constrained relative to start year selection
        start = int(self.start_dropdown.currentText())
        self.end_dropdown.clear()
        self.end_dropdown.addItems([str(y) for y in range(start + 1, start + 6)])

    # ------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------

    def on_validate_clicked(self):
        if not self.file_path:
            print("No file selected")
            return

        # Remap column indices into readable display strings
        col_indices = list(self.CSV.filetype())
        col_indices.pop(3)

        names = ["Opens", "Closes", "Dates", "Lows", "Highs"]
        mapped = []

        for idx, name in zip(col_indices, names):
            mapped.insert(idx, name)

        self.columns_label.setText(", ".join(mapped))

        self.start_year = self.start_dropdown.currentText()
        self.end_year = self.end_dropdown.currentText()

        print("Validated:")
        print("File:", self.file_path)
        print("Start:", self.start_year)
        print("End:", self.end_year)

    # ------------------------------------------------------------
    # Drag & Drop
    # ------------------------------------------------------------

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.dragndrop.setStyleSheet("""
                QLabel {
                    border: 3px dashed #888;
                    padding: 60px;
                    font-size: 18px;
                    background-color:#5e5e5d;
                    color:white;
                }
            """)

    def dragLeaveEvent(self, event):
        self.dragndrop.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                padding: 60px;
                font-size: 18px;
                color:white;
            }
        """)

    def dropEvent(self, event):
        # Brief green highlight feedback on drop
        self.dragndrop.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                padding: 60px;
                font-size: 18px;
                background-color:green;
                color:white;
            }
        """)

        QTimer.singleShot(1000, lambda: self.dragndrop.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                padding: 60px;
                font-size: 18px;
                color:white;
            }
        """))

        file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_path = file_path
        self.file_label.setText(file_path)

        self.CSV = ProcessCSV(file_path)
        self.build_year_dropdowns()

        print(file_path)