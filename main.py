import sys
from PySide6.QtWidgets import QApplication, QStackedWidget

# Import your GUI screens
from GUI.home import HomeScreen
from GUI.results import Results
from GUI.settings import SettingsScreen
from GUI.upload_file import loadCSV

# Import your Logic handler
from Logic.resultsdata import RecieveData,BacktestRun

app = QApplication(sys.argv)

stack = QStackedWidget()
stack.setStyleSheet("background-color: #323232;")

# 1. Instantiate your GUI screens AND your Logic handler
home = HomeScreen()
setting = SettingsScreen()
csvscreen = loadCSV()
results = Results()
logic_handler = RecieveData()  # <--- Created logic instance here

stack.addWidget(home)  # index 0
stack.addWidget(setting)  # index 1
stack.addWidget(csvscreen)  # index 2
stack.addWidget(results)  # index 3

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

# Connect signals from GUI to results data
setting.settings_applied.connect(logic_handler.recieve_settings)    
csvscreen.years_applied.connect(logic_handler.recieve_years)
csvscreen.file_path_got.connect(logic_handler.receive_file)
csvscreen.columns_validated.connect(logic_handler.recieve_columns)
home.base_settings.connect(logic_handler.recieve_base_settings)

#connect signals from resultsdata to home.py
logic_handler.ready_to_backtest.connect(home.set_backtest_button_green)
#logic_handler.ready_to_results.connect(home.set_results_button_green)



def run_portfolio_if_ready():
    if logic_handler.ready():
        Backtest1.run_portfolio()
    else:
        print(">>>>> Not enough data to calculate portfolio <<<<<")

Backtest1 = BacktestRun(logic_handler)
home.run_backtest.connect(run_portfolio_if_ready)

#send the results to the results graph screen
Backtest1.results_ready.connect(results.update_graph)

stack.show()
sys.exit(app.exec()) 