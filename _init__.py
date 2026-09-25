from PySide6.QtWidgets import QApplication, QStackedWidget
import sys

from GUI.settings import SettingsScreen
from GUI.upload_file import loadCSV
from GUI.home import HomeScreen
from GUI.results import Results

app = QApplication(sys.argv)

stack = QStackedWidget()   
stack.setStyleSheet("background-color: #323232;")
home = HomeScreen()
setting = SettingsScreen()
csvscreen = loadCSV()
results = Results()

stack.addWidget(home)      # index 0
stack.addWidget(setting)   # index 1
stack.addWidget(csvscreen)  # index 2
stack.addWidget(results)     # index 3

# Navigation
home.go_settings.connect(lambda: stack.setCurrentIndex(1))

home.go_CSV.connect(lambda: stack.setCurrentIndex(2))
home.go_results.connect(lambda: stack.setCurrentIndex(3))

setting.go_home.connect(lambda: stack.setCurrentIndex(0))

csvscreen.go_home.connect(lambda: stack.setCurrentIndex(0))
csvscreen.go_settings.connect(lambda: stack.setCurrentIndex(1))

results.go_home.connect(lambda: stack.setCurrentIndex(0))



# CSV → HomeScreen button update
csvscreen.csv_loaded.connect(home.updatestrategyButtonColor)

stack.show()
sys.exit(app.exec())
