# Generate MA buy/sell/hold signals from 10-day vs 30-day averages.
def moving_average(closes, minimum_days):
    MA_signals = []
    days_to_wait = 0
    # Start at day 30 so both moving-average windows are available.
    for i in range(30, len(closes)):
        thirty_day_total = 0
        ten_day_total = 0

        for j in range(i - 30, i):
            thirty_day_total += closes[j]

        thirty_day_average = (thirty_day_total / 30)

        # 10 day average
        ten_day_total = 0

        for j in range(i - 10, i):
            ten_day_total += closes[j]

        ten_day_average = (ten_day_total / 10)

        # Enforce a cooldown so signals are not allowed to fire on consecutive days.
        if ten_day_average > thirty_day_average and days_to_wait == 0:
            MA_signals.append("BUY")
            if minimum_days != 0:
                days_to_wait = minimum_days + 1
        elif ten_day_average < thirty_day_average and days_to_wait == 0:
            MA_signals.append("SELL")
            if minimum_days != 0:
                days_to_wait = minimum_days + 1
        else:
            MA_signals.append("HOLD")
            if days_to_wait > 0:
                days_to_wait -= 1

    return MA_signals

# Calculate RSI values, then convert threshold crossings into trade signals.
def calculate_RSI(closes, overbuy, oversell, period, minimum_days):
    RSI_list = []
    # RSI needs at least one full lookback period plus the prior close.
    if len(closes) < period + 1:
        return []

    total_gains = 0.0
    total_losses = 0.0
    # Seed Wilder's smoothing with the first full window of gains and losses.
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
        # Handle flat/up-only stretches without dividing by zero.
        if avg_loss == 0:
            RSI = 100.0
        else:
            RS = avg_gain / avg_loss
            # Convert relative strength into the standard 0-100 RSI scale.
            RSI = 100 - (100 / (1 + RS))
        RSI_list.append(RSI)

    signals = RSI_signals(RSI_list, minimum_days, overbuy, oversell)
    return signals

# Turn RSI threshold crossings into buy/sell/hold signals.
def RSI_signals(RSI_list, minimum_days, overbuy, oversell):
    signals = []
    prev = RSI_list[0]
    days_to_wait = 0
    for rsi in RSI_list:
        if prev < oversell and rsi >= oversell and days_to_wait == 0:
            signals.append("BUY")
            if minimum_days != 0:
                days_to_wait = minimum_days + 1
        elif prev > overbuy and rsi <= overbuy and days_to_wait == 0:
            signals.append("SELL")
            if minimum_days != 0:
                days_to_wait = minimum_days + 1
        else:
            signals.append("HOLD")
            if days_to_wait > 0:
                days_to_wait -= 1
        prev = rsi

    return signals


def ATR():
    pass
