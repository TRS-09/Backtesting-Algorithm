from Logic.csv_processing import ProcessCSV
from Logic.calculate_signals import IndicatorCalculator

class RecieveData:

    def __init__(self):
        # To know if data required has been entered/is present
        self.settings_present = False
        self.years_present = False
        self.file_present = False
        self.file_valid = True

        # Data filtering parameters
        self.min_year = 0
        self.max_year = 0
        self.start_year = None
        self.end_year = None
        self.csvdata = None
        self.file = ""

        # Columns and data lists
        self.columns_present = []
        self.dates = []
        self.opens = []
        self.closes = []
        self.highs = []
        self.lows = []

        # Dictionary to hold raw settings
        self.settings = {}

        # Individual typed variables for calculations
        self.rsi_overbought = 70
        self.rsi_oversold = 30
        self.rsi_period = 14
        self.sma_fast = 10
        self.sma_slow = 30
        self.sma_min_days = 14
        self.atr_period = 14
        self.atr_multiplier = 1.5
        self.atr_cooldown = 2

    def ready(self):
        print("ready")
        print([self.settings_present, self.years_present, self.file_present, self.file_valid])
        return all([self.settings_present, self.years_present, self.file_present, self.file_valid])

    def recieve_years(self, years: list):
        self.start_year = years[0]
        self.end_year = years[1]
        print("Start/End years recorded", self.start_year, self.end_year, "(resultsdata.py)")
        self.years_present = True

    def receive_file(self, input_file: str):
        self.file = input_file
        self.file_present = True
        print("File Recorded",self.file,"(resultsdata.py)")

    def recieve_settings(self, settings: dict):
        # Once settings are emitted from GUI - settings.py they are sent to main.py, then here.
        self.settings = settings

        self.rsi_overbought = int(self.settings.get("rsi_overbought", 70))
        self.rsi_oversold = int(self.settings.get("rsi_oversold", 30))
        self.rsi_period = int(self.settings.get("rsi_period", 14))

        self.sma_fast = int(self.settings.get("sma_fast", 10))
        self.sma_slow = int(self.settings.get("sma_slow", 30))
        self.sma_min_days = int(self.settings.get("sma_min_days", 14))

        self.atr_period = int(self.settings.get("atr_period", 14))
        self.atr_multiplier = float(self.settings.get("atr_multiplier", 1.5))
        self.atr_cooldown = int(self.settings.get("atr_cooldown", 2))

        print("Settings recorded",self.settings,"(resultsdata.py)")
        self.settings_present = True

    def recieve_columns(self, columns_present: list):
        self.columns_present = columns_present

        print("Recieved columns:",self.columns_present, "(resultsdata.py)")

class BacktestRun:
    def __init__(self,logic_handler):
        self.logic = logic_handler
        self.CSV = ProcessCSV(self.logic.file)
        self.CSV.filetype()
        self.CSV.load_price_data(self.logic.min_year,self.logic.max_year)

    def calculate_signals(self):
        #runs the init of the Inicator calculator, passing through data from the CSV + settings from GUI
        self.Signals = IndicatorCalculator(self.CSV.closes,self.CSV.dates,self.CSV.lows,self.CSV.highs,self.logic.rsi_overbought,self.logic.rsi_oversold,self.logic.rsi_period,self.logic.sma_fast,self.logic.sma_slow,
        self.logic.sma_min_days,self.logic.atr_period,self.logic.atr_multiplier,self.logic.atr_cooldown)

        #assign signals to attributes
        self.sma_signals = self.Signals.moving_average()
        self.rsi_signals = self.Signals.RSI_signals()
        self.atr_signals = self.Signals.ATR_signals()

    def run_portfolio(self):
        #NEED TO DO THIS
        pass


