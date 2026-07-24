from PySide6.QtWidgets import QApplication, QStackedWidget
import sys

from settings import SettingsScreen
from home import HomeScreen
from upload_data import loadCSV

app = QApplication(sys.argv)

stack = QStackedWidget()
stack.setStyleSheet("background-color: #323232;")
home = HomeScreen()
setting = SettingsScreen()
csv = loadCSV()

stack.addWidget(home)      # index 0
stack.addWidget(setting)   # index 1
stack.addWidget(csv)       # index 2

# Navigation
home.go_settings.connect(lambda: stack.setCurrentIndex(1))
home.go_CSV.connect(lambda: stack.setCurrentIndex(2))
setting.go_home.connect(lambda: stack.setCurrentIndex(0))
csv.go_home.connect(lambda: stack.setCurrentIndex(0))



# CSV → HomeScreen button update
csv.csv_loaded.connect(home.updatestrategyButtonColor)

stack.show()
sys.exit(app.exec())
