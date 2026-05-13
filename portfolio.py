# Simulate trades from signals and return ending cash, curve, and profit.
def calculate_portfolio(signals, risk_percentage, starting_cash, opens, offset, slippage, fees):
    portfolio = []
    shares_holding = 0
    cash = starting_cash

    tradable_days = min(len(signals), len(opens) - offset)
    if tradable_days <= 0:
        return starting_cash, portfolio, 0.0

    for i in range(tradable_days):
        price = opens[i + offset]
        # The strategy holds either cash or one share position at a time.
        if shares_holding == 0 and signals[i] == "BUY":
            cash_to_spend = cash * risk_percentage
            shares_holding = int(cash_to_spend // price)
            if shares_holding > 0:
                # slippage is 0.1%
                cash -= ((shares_holding * price * (1 + slippage)) + fees)
        elif shares_holding > 0 and signals[i] == "SELL":
            # slippage is 0.1%
            cash += ((shares_holding * price * (1 - slippage)) - fees)
            shares_holding = 0
        portfolio.append(cash + shares_holding * price)

    end_cash = portfolio[-1] if portfolio else starting_cash
    profit = end_cash - starting_cash
    return end_cash, portfolio, profit
