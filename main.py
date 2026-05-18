import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from termcolor import colored
from calculate_signals import calculate_RSI, moving_average
from csv_processing import file_find_select, filetype, load_price_data, year_range
from portfolio import calculate_portfolio
from rsi_range import best_RSI_range
from market_closed import plotting_dates,graph_plot_values

end = "N"
prev_overbuy = None
prev_oversell = None

# Base RSI lookback. The RSI strategy later uses `period + 2` to match the original offsets.
period = 14

# Select and inspect the CSV once before entering the backtest loop.
file = file_find_select()

opens_loc,closes_loc,date_loc,descendingcsv = filetype(file)

min_year,max_year = year_range(file, date_loc)


while end != "Y" :
    # These values reset for each run so the user can test different ranges and risk settings.
    risk = 0
    minimum_days = 2
    slippage = 0.001
    
    #colored texts
    fee_text = colored("Would you like the realism of fees (Y/N) :  ","blue")
    invalid_risk_text = colored("Risk must be between 0-100%","yellow")
    risk_text = colored("How much risk do you want to take (x%) :  ","cyan")
    starting_cash_text = colored("Enter initial cash :  ","cyan")

    #starting year code
    starting_year = 0
    ending_year = 0
    invalid_year_txt1 = ("INVALID YEAR , Valid years : "+str(min_year)+" - "+str(max_year))
    incorrect_year_text2 = colored(invalid_year_txt1,"yellow")

    starting_year_text = colored("Enter year to begin investing :  ","cyan")
    ending_year_text = colored("Enter year to end investing (uses data in 'x' year) :  ","cyan")
    while int(starting_year) < min_year or int(starting_year)> max_year:
        starting_year = input(starting_year_text)
        if int(starting_year) < min_year or int(starting_year)> max_year:
            print(incorrect_year_text2) 
            print("")
            
    #for ending year invalidity
    invalid_year_txt3 = ("INVALID YEAR , Valid years : "+str(int(starting_year) + 1)+" - "+str(max_year))
    incorrect_year_text4 = colored(invalid_year_txt3,"yellow")
    while int(ending_year) <= int(starting_year) or int(ending_year)> max_year:
        ending_year = input(ending_year_text)
        if int(ending_year) <= int(starting_year) or int(ending_year)> max_year:
            print(incorrect_year_text4) 
            print("")

    while risk > 100 or risk < 1:
        print("")
        risk = int(input(risk_text))
        risk_percentage = risk / 100
        if risk > 100 or risk < 1:
            print(invalid_risk_text)
    

    starting_cash = int(input(starting_cash_text+"£"))
    fee = input(fee_text).strip().upper()[:1]
    if fee == "Y":
        fees = 2.5
    else:
        fees = 0
    print("")

    # Load only the chosen date window into memory for the strategies to use.
    dates, opens, closes = load_price_data(
        file,
        descendingcsv,
        date_loc,
        opens_loc,
        closes_loc,
        starting_year,
        ending_year,
    )

    if not dates:
        print(colored(f"No data found for year {starting_year}. Try a different year.", "yellow"))
        continue

    dates_dt = [datetime.strptime(d.strip(), "%Y-%m-%d") for d in dates]
        
    plt.ylabel("PORTFOLIO (£)")
    plt.xlabel("YEAR")

    # Run the moving-average strategy first, then plot its portfolio curve.
    MA_signals = moving_average(closes,minimum_days,dates)
    end_cash,portfolio,profit = calculate_portfolio(MA_signals,risk_percentage,starting_cash,opens,30,slippage,fees)
    end_cash_text = colored(round(end_cash,2),"red")
    profit_text = colored(round(profit,2),"red")
    print("Total end cash for MA :",end_cash_text)
    print("Profit for MA :",profit_text)

    #30 because portfolio for MA is 30 less than dates 
    portfolio_plot,dates_dt = graph_plot_values(dates,portfolio,30)
    plt.plot(dates_dt, portfolio_plot,label = "MA | Risk = "+str(risk) +"% | Profit =  £"+ str(round(profit,2))+ " | "+str(starting_year)+"→" + str(int(ending_year)+1))

    # Choose RSI thresholds manually, reuse the previous pair, or brute-force a new pair.
    overbuy,oversell = best_RSI_range(closes,risk_percentage,starting_cash,opens,period,minimum_days,slippage,fees,prev_overbuy,prev_oversell)
    prev_overbuy,prev_oversell = overbuy,oversell
    print("Best range for RSI found. Overbuy =",overbuy,"Oversell =",oversell)

    # Run the RSI strategy with the selected thresholds and plot the result.
    RSI_signals = calculate_RSI(closes,overbuy,oversell,period+2,minimum_days)
    end_cash,portfolio,profit = calculate_portfolio(RSI_signals,risk_percentage,starting_cash,opens,period+2,slippage,fees)
    end_cash_text = colored(round(end_cash,2),"red")
    profit_text = colored(round(profit,2),"red")
    print("Total end cash for RSI :",end_cash_text)
    print("Profit for RSI :",profit_text)
    
    #17 = period+3
    portfolio_plot,dates_dt = graph_plot_values(dates,portfolio,17)

    plt.plot(dates_dt, portfolio_plot,label = "RSI | Risk = "+str(risk) +"% | Profit =  £"+ str(round(profit,2)) +" | Overbuy = "+ str(overbuy) +" | Oversell = "+ str(oversell) + " | "+str(starting_year) +"→" + str(int(ending_year)+1))
    plt.legend(fontsize=8)

    # Format the x-axis in yearly steps so long backtests stay readable.
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    plt.title("Backtesting Results")

    plt.show(block=False)

    end = input("Quit(Y/N) : ").strip().upper()[:1]

# ATR — volatility measurement
# OBV — volume pressure
