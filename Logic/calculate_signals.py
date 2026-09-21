from datetime import datetime


class IndicatorCalculator:
    def __init__(self, closes, dates, minimum_days, period, overbuy, oversell, lows, highs):
        self.closes = closes
        self.dates = dates
        self.highs = highs
        self.lows = lows
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

        # pad first 30 days with HOLD so signals align with closes
        for _ in range(30):
            MA_signals.append("HOLD")

        for i in range(30, len(closes)):
            thirty_day_avg = sum(closes[i-30:i]) / 30
            ten_day_avg = sum(closes[i-10:i]) / 10

            # BUY signal
            if ten_day_avg > thirty_day_avg and days_to_wait == 0 and prev_signal != "BUY":
                MA_signals.append("BUY")
                prev_signal = "BUY"
                days_to_wait = minimum_days

            # SELL signal
            elif ten_day_avg < thirty_day_avg and days_to_wait == 0 and prev_signal != "SELL":
                MA_signals.append("SELL")
                prev_signal = "SELL"
                days_to_wait = minimum_days

            # HOLD
            else:
                MA_signals.append("HOLD")

                # cooldown countdown
                if days_to_wait > 0:
                    days_to_wait -= 1

                # IMPORTANT: do NOT reset prev_signal here
                # HOLD is not a signal, it's just a state

        return MA_signals

    def calculate_RSI(self):
        closes = self.closes
        period = self.period

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

    def calculate_ATR(self):
        """function to calculate raw ATR values."""
        highs = self.highs
        lows = self.lows
        closes = self.closes
        period = self.period

        if len(highs) < period + 1:
            return []

        TR_list = []

        # Step 1: Compute True Range for each day
        for i in range(1, len(highs)):
            high = highs[i]
            low = lows[i]
            prev_close = closes[i - 1]

            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            TR_list.append(tr)

        # Step 2: Seed ATR with first period TR average
        first_atr = sum(TR_list[:period]) / period
        ATR_values = [first_atr]

        # Step 3: Wilder smoothing for remaining ATR values
        prev_atr = first_atr
        for tr in TR_list[period:]:
            atr = ((prev_atr * (period - 1)) + tr) / period
            ATR_values.append(atr)
            prev_atr = atr

        return ATR_values

    def ATR(self):
        """Generates BUY/SELL/HOLD signals using an ATR Volatility Breakout model."""
        atr_values = self.calculate_ATR()
        closes = self.closes
        period = self.period
        minimum_days = self.minimum_days

        signals = []
        if not atr_values:
            return signals

        # Pad initial days where ATR isn't available to keep output aligned with closes length
        padding_count = len(closes) - len(atr_values)
        for _ in range(padding_count):
            signals.append("HOLD")

        prev_signal = "HOLD"
        days_to_wait = 0

        for k, atr in enumerate(atr_values):
            i = period + k
            curr_close = closes[i]
            prev_close = closes[i - 1]

            # Breakout logic: Price exceeds previous close by more than 1 ATR
            upper_band = prev_close + atr
            lower_band = prev_close - atr

            # BUY signal (bullish volatility breakout)
            if curr_close > upper_band and days_to_wait == 0 and prev_signal != "BUY":
                signals.append("BUY")
                prev_signal = "BUY"
                days_to_wait = minimum_days

            # SELL signal (bearish volatility breakdown)
            elif curr_close < lower_band and days_to_wait == 0 and prev_signal != "SELL":
                signals.append("SELL")
                prev_signal = "SELL"
                days_to_wait = minimum_days

            # HOLD
            else:
                signals.append("HOLD")
                if days_to_wait > 0:
                    days_to_wait -= 1

        return signals