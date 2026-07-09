from portfolio import calculate_portfolio

# Choose RSI thresholds manually, reuse the previous pair, or brute-force a new pair.
def best_RSI_range(risk_percentage,starting_cash,opens,slippage,fees,prev_overbuy,prev_oversell,ind):
    choose_RSI_range = ""
    while choose_RSI_range not in ["1","2","3"]:
        choose_RSI_range = input("Do you wish to use your own RSI range, previous, or find a new one? (1,2,3) ")
        
    if choose_RSI_range == "2":
        if prev_overbuy is not None and prev_oversell is not None:
            best_overbuy = prev_overbuy
            best_oversell = prev_oversell
        else:
            while choose_RSI_range == "2":
                print("ERROR - No previous RSI range stored!")
                choose_RSI_range = input("Do you wish to use your own RSI range, previous, or find a new one? (1,2,3) ")

    if choose_RSI_range == "1":
        best_overbuy = int(input("Enter overbuy point: "))
        best_oversell = int(input("Enter oversell point: "))


    if choose_RSI_range == "3":
        highest = None
        # Search a coarse grid of RSI thresholds and keep the most profitable pair.
        for i in range(1, 10):
            oversell = i * 5
            for j in range(1, 10):
                overbuy = 100 - j * 5
                ind.overbuy = overbuy
                ind.oversell = oversell
                RSI_signals = ind.RSI_signals()
                end_cash, portfolio, profit = calculate_portfolio(
                    RSI_signals,
                    risk_percentage,
                    starting_cash,
                    opens,
                    ind.period + 3,
                    slippage,
                    fees,
                )
                if highest is None or profit > highest:
                    highest = profit
                    best_overbuy = overbuy
                    best_oversell = oversell

    ind.overbuy = best_overbuy
    ind.oversell = best_oversell
    return best_overbuy, best_oversell
