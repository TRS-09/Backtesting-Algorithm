from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal,QTimer
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
        title = QLabel("Upload CSV")
        title.setStyleSheet("color: white;")
        title.setFont(QFont("arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: grey;")
        layout.addWidget(line)

        # drag and drop file
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
        layout.addWidget(self.dragndrop)

        layout.addStretch() 
        
        self.setAcceptDrops(True)
        self.setLayout(layout)
    
    # when the user drags the file in the screen
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
            
    # when the user moves the file out of the screen
    def dragLeaveEvent(self, event):
        self.dragndrop.setStyleSheet("""
            QLabel {
                border: 3px dashed #888;
                padding: 60px;
                font-size: 18px;
                color: white;
            }
        """)
        
    # when the user drops the file into the box, flash green then normal then print file path
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

        QTimer.singleShot(1000,lambda: self.dragndrop.setStyleSheet("""
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

"""
ISSUES

- Woudlnt flash green
- Had to make it so it would change colour of the box

"""
