from Logic.csv_processing import ProcessCSV
from Logic.calculate_signals import IndicatorCalculator
from Logic.portfolio import Portfolio
from Logic.plot_run import PlotData
from PySide6.QtCore import QObject, Signal  


class RecieveData(QObject):

    #signal for changing colour of backtest button/results button to show there is enough data to begin
    ready_to_backtest = Signal()

    def __init__(self):
        super().__init__()
        # To know if data required has been entered/is present
        self.settings_present = False
        self.years_present = False
        self.file_present = False
        self.base_settings_present = False

        # Data filtering parameters
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
        self.base_settings = []

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
        return all([self.settings_present, self.years_present, self.file_present,self.base_settings_present])

    def recieve_years(self, years: list):
        self.start_year = years[0]
        self.end_year = years[1]
        print("Start/End years recorded", self.start_year, self.end_year, "(resultsdata.py)")
        self.years_present = True
        if self.ready():
            self.ready_to_backtest.emit()


    def receive_file(self, input_file: str):
        self.file = input_file
        self.file_present = True
        print("File Recorded", self.file, "(resultsdata.py)")
        if self.ready():
            self.ready_to_backtest.emit()

    def recieve_settings(self, settings: dict):
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

        print("Settings recorded", self.settings, "(resultsdata.py)")
        self.settings_present = True
        if self.ready():
            self.ready_to_backtest.emit()

    def recieve_columns(self, columns_present: list):
        self.columns_present = columns_present
        print("Recieved columns:", self.columns_present, "(resultsdata.py)")
        if self.ready():
            self.ready_to_backtest.emit()
    
    def recieve_base_settings(self, base_settings: list):
        self.base_settings = base_settings
        self.base_settings_present = True
        print("Recieved base settings: ", self.base_settings, "(resultsdata.py)")
        if self.ready():
            self.ready_to_backtest.emit()


class BacktestRun(QObject):  #Inherits from QObject
    
    # Define signal at class level
    results_ready = Signal(list)
    ready_to_results = Signal()

    def __init__(self, logic_handler):
        super().__init__()
        self.logic = logic_handler
        self.CSV = None        

    def calculate_signals(self):
        self.CSV = ProcessCSV(self.logic.file)
        self.CSV.filetype()
        self.CSV.load_price_data(self.logic.start_year, self.logic.end_year)

        self.Signals = IndicatorCalculator(
            self.CSV.closes, self.CSV.dates, self.CSV.lows, self.CSV.highs,
            self.logic.rsi_overbought, self.logic.rsi_oversold, self.logic.rsi_period,
            self.logic.sma_fast, self.logic.sma_slow, self.logic.sma_min_days,
            self.logic.atr_period, self.logic.atr_multiplier, self.logic.atr_cooldown
        )

        self.sma_signals = self.Signals.moving_average()
        self.rsi_signals = self.Signals.RSI_signals()
        self.atr_signals = self.Signals.ATR_signals()

    def run_portfolio(self):
        self.calculate_signals()

        self.SMA_portfolio = Portfolio(self.CSV.opens, self.logic.base_settings[2]/100, self.logic.base_settings[1], 0.001, self.logic.base_settings[0], self.sma_signals, 1)
        self.RSI_portfolio = Portfolio(self.CSV.opens, self.logic.base_settings[2]/100, self.logic.base_settings[1], 0.001, self.logic.base_settings[0], self.rsi_signals, int(self.logic.rsi_period))
        self.ATR_portfolio = Portfolio(self.CSV.opens, self.logic.base_settings[2]/100, self.logic.base_settings[1], 0.001, self.logic.base_settings[0], self.atr_signals, int(self.logic.atr_period))
        
        print("SMA portfolio length:", len(self.SMA_portfolio.portfolio))
        print("RSI portfolio length:", len(self.RSI_portfolio.portfolio))
        print("ATR portfolio length:", len(self.ATR_portfolio.portfolio))
        print("CSV dates length:", len(self.CSV.dates)) 
        print(self.logic.atr_period,self.logic.rsi_period)

        SMA_plot = PlotData(self.CSV.dates, 1, self.SMA_portfolio.portfolio)
        RSI_plot = PlotData(self.CSV.dates, int(self.logic.rsi_period)+3, self.RSI_portfolio.portfolio)
        ATR_plot = PlotData(self.CSV.dates, int(self.logic.atr_period), self.ATR_portfolio.portfolio)

        plottting_data = [
            {"x": SMA_plot.calendar_dates, "y": SMA_plot.portfolio_plot, "label": "SMA", "color": "#4CAF50"},
            {"x": RSI_plot.calendar_dates, "y": RSI_plot.portfolio_plot, "label": "RSI", "color": "#AFAA4C"},
            {"x": ATR_plot.calendar_dates, "y": ATR_plot.portfolio_plot, "label": "ATR", "color": "#494394"}
        ]
        
        self.ready_to_results.emit()
        self.results_ready.emit(plottting_data)
