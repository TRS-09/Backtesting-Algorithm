from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
import sys

#dimensions
xpos = 0
ypos = 0
width = 300
height = 300

class mywindow(QMainWindow):
    #creates the window
    def __init__(self):
        super(mywindow,self).__init__()
        self.setGeometry(0,0,500,500)
        self.initUI()

    #initiates the UI
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("LABALLL")
        self.label.move(50,0)

        self.button = QtWidgets.QPushButton(self)
        self.button.setText("Click me")
        self.button.move(50,50)
        self.button.clicked.connect(self.clicked)

    #change when button is clicked
    def clicked(self):
        self.label.setText("CLICKED!!.................??//")
        self.update()

    #update button size
    def update(self):
        self.label.adjustSize()


def window():
    app  = QApplication(sys.argv)
    win = mywindow()

    win.showMaximized()
    sys.exit(app.exec())


window()


