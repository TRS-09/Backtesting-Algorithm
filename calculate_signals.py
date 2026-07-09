from datetime import datetime

from datetime import datetime

class IndicatorCalculator:
    def __init__(self, closes, dates, minimum_days, period, overbuy, oversell):
        self.closes = closes
        self.dates = dates
        self.minimum_days = minimum_days
        self.period = period
        self.overbuy = overbuy      
        self.oversell = oversell
        
    def moving_average(self):
        closes = self.closes
        minimum_days = self.minimum_days

        prev_signal = "HOLD"
        MA_signals = []
        days_to_wait = 0

        for i in range(30, len(closes)):
            thirty_day_total = sum(closes[i-30:i])
            ten_day_total = sum(closes[i-10:i])

            thirty_day_average = thirty_day_total / 30
            ten_day_average = ten_day_total / 10

            if ten_day_average > thirty_day_average and days_to_wait == 0 and prev_signal != "BUY":
                MA_signals.append("BUY")
                prev_signal = "BUY"
                if minimum_days != 0:
                    days_to_wait = minimum_days + 1

            elif ten_day_average < thirty_day_average and days_to_wait == 0 and prev_signal != "SELL":
                MA_signals.append("SELL")
                prev_signal = "SELL"
                if minimum_days != 0:
                    days_to_wait = minimum_days + 1

            else:
                MA_signals.append("HOLD")
                prev_signal = "HOLD"
                if days_to_wait > 0:
                    days_to_wait -= 1

        return MA_signals

    def calculate_RSI(self):
        closes = self.closes
        period = self.period + 2

        RSI_list = []
        if len(closes) < period + 1:
            return []

        total_gains = 0.0
        total_losses = 0.0

        for i in range(1, period + 1):
            change = closes[i] - closes[i - 1]
            total_gains += max(change, 0.0)
            total_losses += max(-change, 0.0)

        avg_gain = total_gains / period
        avg_loss = total_losses / period

        for i in range(period + 1, len(closes)):
            change = closes[i] - closes[i - 1]
            gain = max(change, 0)
            loss = max(-change, 0)

            avg_gain = (avg_gain * (period - 1) + gain) / period
            avg_loss = (avg_loss * (period - 1) + loss) / period

            if avg_loss == 0:
                RSI = 100.0
            else:
                RS = avg_gain / avg_loss
                RSI = 100 - (100 / (1 + RS))

            RSI_list.append(RSI)

        return RSI_list

    def RSI_signals(self):
        RSI_list = self.calculate_RSI()
        minimum_days = self.minimum_days
        overbuy = self.overbuy
        oversell = self.oversell

        prev_signal = "HOLD"
        signals = []
        prev = RSI_list[0]
        days_to_wait = 0

        for rsi in RSI_list:
            if prev < oversell and rsi >= oversell and days_to_wait == 0 and prev_signal != "BUY":
                signals.append("BUY")
                prev_signal = "BUY"
                if minimum_days != 0:
                    days_to_wait = minimum_days + 1

            elif prev > overbuy and rsi <= overbuy and days_to_wait == 0 and prev_signal != "SELL":
                signals.append("SELL")
                prev_signal = "SELL"
                if minimum_days != 0:
                    days_to_wait = minimum_days + 1

            else:
                signals.append("HOLD")
                prev_signal = "HOLD"
                if days_to_wait > 0:
                    days_to_wait -= 1

            prev = rsi

        return signals

    def ATR(self):
        pass
