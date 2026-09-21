from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont

class loadCSV(QWidget):
    go_home = Signal()
    csv_loaded = Signal(bool)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(40, 30, 40, 40)

        # Title
        layout.addWidget(self.build_title())

        # Divider
        layout.addWidget(self.build_divider())

        # Drag & Drop box
        layout.addWidget(self.build_dragndrop())

        # Browse button
        layout.addWidget(self.build_browse_button())

        # File selected label
        layout.addWidget(self.build_file_selected(), alignment=Qt.AlignLeft)

        # Columns detected label
        layout.addWidget(self.build_columns_label(), alignment=Qt.AlignLeft)

        layout.addStretch()

        #divider
        layout.addWidget(self.build_divider())
        #validate button
        layout.addWidget(self.build_validate_btn(),alignment=Qt.AlignLeft)

        self.setAcceptDrops(True)
        self.setLayout(layout)

    # ---------------------------
    # Builder methods
    # ---------------------------

    def build_title(self):
        title = QLabel("Upload CSV")
        title.setStyleSheet("color: white;")
        title.setFont(QFont("arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        return title

    def build_divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: grey;")
        return line

    def build_dragndrop(self):
        self.dragndrop = QLabel("Drag & Drop")
        self.dragndrop.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                padding: 60px;
                font-size: 18px;
                color: white;
            }
        """)
        self.dragndrop.setAlignment(Qt.AlignCenter)
        return self.dragndrop

    def build_browse_button(self):
        browse_btn = QPushButton("Browse files")
        browse_btn.setStyleSheet("""
            QWidget{                 
                background-color: #d9d9db;
                padding: 25px 10px;
                color: black;
                font-size: 20px;
            }
        """)
        return browse_btn

    def build_file_selected(self):
        self.file_selected_txt = QLabel("File selected:")
        self.file_selected_txt.setStyleSheet("color:white; font-size:25px;")
        return self.file_selected_txt

    def build_columns_label(self):
        self.columnslabel = QLabel("Columns detected:")
        self.columnslabel.setStyleSheet("color:white; font-size:25px;")
        return self.columnslabel

    def build_validate_btn(self):
        validate_btn = QPushButton("Validate")
        validate_btn.setStyleSheet("background-color:#388238; color:black;")
        return validate_btn

    # ---------------------------
    # Drag & Drop Events
    # ---------------------------

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.dragndrop.setStyleSheet("""
                QLabel {
                    border: 3px dashed #888;
                    padding: 60px;
                    font-size: 18px;
                    background-color: #5e5e5d;
                    color: white;
                }
            """)

    def dragLeaveEvent(self, event):
        self.dragndrop.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                padding: 60px;
                font-size: 18px;
                color: white;
            }
        """)

    def dropEvent(self, event):
        self.dragndrop.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                padding: 60px;
                font-size: 18px;
                background-color: green;
                color: white;
            }
        """)

        QTimer.singleShot(1000, lambda: self.dragndrop.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                padding: 60px;
                font-size: 18px;
                color: white;
            }
        """))

        urls = event.mimeData().urls()
        file_path = urls[0].toLocalFile()

        print(file_path)
