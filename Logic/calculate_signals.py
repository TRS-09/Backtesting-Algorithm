from datetime import datetime


class IndicatorCalculator:
    def __init__(
        self,closes,dates,lows,highs,rsi_overbought=70,rsi_oversold=30,rsi_period=14,sma_fast=10,sma_slow=30,
        sma_min_days=14,atr_period=14,atr_multiplier=1.5,atr_cooldown=2
    ):
        self.closes = closes
        self.dates = dates
        self.highs = highs
        self.lows = lows

        # RSI Settings
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.rsi_period = rsi_period

        # SMA Settings
        self.sma_fast = sma_fast
        self.sma_slow = sma_slow
        self.sma_min_days = sma_min_days

        # ATR Settings
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier
        self.atr_cooldown = atr_cooldown

    def moving_average(self):
        closes = self.closes

        prev_signal = "HOLD"
        MA_signals = []
        days_to_wait = 0

        # pad first sma_slow days with HOLD so signals align with closes
        for _ in range(self.sma_slow):
            MA_signals.append("HOLD")

        for i in range(self.sma_slow, len(closes)):
            slow_avg = sum(closes[i - self.sma_slow : i]) / self.sma_slow
            fast_avg = sum(closes[i - self.sma_fast : i]) / self.sma_fast

            # BUY signal
            if fast_avg > slow_avg and days_to_wait == 0 and prev_signal != "BUY":
                MA_signals.append("BUY")
                prev_signal = "BUY"
                days_to_wait = self.sma_min_days

            # SELL signal
            elif fast_avg < slow_avg and days_to_wait == 0 and prev_signal != "SELL":
                MA_signals.append("SELL")
                prev_signal = "SELL"
                days_to_wait = self.sma_min_days

            # HOLD
            else:
                MA_signals.append("HOLD")

                # cooldown countdown
                if days_to_wait > 0:
                    days_to_wait -= 1

        return MA_signals

    def calculate_RSI(self):
        closes = self.closes
        period = self.rsi_period

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
        minimum_days = self.sma_min_days
        overbuy = self.rsi_overbought
        oversell = self.rsi_oversold

        prev_signal = "HOLD"
        signals = []
        if not RSI_list:
            return signals

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
        period = self.atr_period

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

    def ATR_signals(self):
        """Generates BUY/SELL/HOLD signals using an ATR Volatility Breakout model."""
        atr_values = self.calculate_ATR()
        closes = self.closes
        period = self.atr_period
        cooldown = self.atr_cooldown
        multiplier = self.atr_multiplier

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

            # Breakout logic using dynamic multiplier
            upper_band = prev_close + (atr * multiplier)
            lower_band = prev_close - (atr * multiplier)

            # BUY signal (bullish volatility breakout)
            if curr_close > upper_band and days_to_wait == 0 and prev_signal != "BUY":
                signals.append("BUY")
                prev_signal = "BUY"
                days_to_wait = cooldown

            # SELL signal (bearish volatility breakdown)
            elif curr_close < lower_band and days_to_wait == 0 and prev_signal != "SELL":
                signals.append("SELL")
                prev_signal = "SELL"
                days_to_wait = cooldown

            # HOLD
            else:
                signals.append("HOLD")
                if days_to_wait > 0:
                    days_to_wait -= 1

        return signals