from Logic.csv_processing import ProcessCSV


class RecieveData:

  def __init__(self):
    # To know if data required has been entered/is present
    self.settings_present = False
    self.years_present = False
    self.file_present = False
    self.file_valid = False

    # Fixed: Initialize them properly
    self.min_year = 0
    self.max_year = 0
    self.csvdata = None
    self.file = ""

    # Fixed: Initialize lists separately
    self.dates = []
    self.opens = []
    self.closes = []
    self.highs = []
    self.lows = []

    # Dictionary to hold raw settings
    self.settings = {}

    # Individual typed variables for your calculations
    self.rsi_overbought = 70
    self.rsi_oversold = 30
    self.rsi_period = 14
    self.sma_fast = 10
    self.sma_slow = 30
    self.sma_min_days = 14
    self.atr_period = 14
    self.atr_multiplier = 1.5
    self.atr_cooldown = 2

  def recieve_years(self, years: list):
    self.start_year = years[0]
    self.end_year = years[1]
    print("recieved ",self.start_year,self.end_year," at results data")

  def receive_file(self, input_file: str):
    self.file = input_file

  def recieve_settings(self, settings: dict):
    # Once the settings are emmited from GUI - settings.py they are sent to main.py, then sent to resultsdata(here). 
    # This automatically runs this function

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

    print("Logic successfully saved settings!")
    
  def recieve_columns(self,columns_present:list):
    self.columns_present = columns_present

    print("Recieved columns: resultsdata.py")
    print("col_present",columns_present)
    
    


