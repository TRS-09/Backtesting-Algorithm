import matplotlib.pyplot as plt
from termcolor import colored
from calculate_signals import IndicatorCalculator
from csv_processing import file_find_select, filetype, load_price_data, year_range
from portfolio import calculate_portfolio
from rsi_range import best_RSI_range
from market_closed import plotting_dates,graph_plot_values

# Base RSI lookback. The RSI strategy later uses `period + 2` to match the original offsets.
period = 14

end = "N"
prev_overbuy = None
prev_oversell = None

overbuy = 0
oversell = 0

# Select and inspect the CSV once before entering the backtest loop.
file = file_find_select()

opens_loc,closes_loc,date_loc,descendingcsv = filetype(file)

min_year,max_year = year_range(file, date_loc)

#colored texts
fee_text = colored("Would you like the realism of fees (Y/N) :  ","blue")
invalid_risk_text = colored("Risk must be between 0-100%","yellow")
risk_text = colored("How much risk do you want to take (x%) :  ","cyan")
starting_cash_text = colored("Enter initial cash :  ","cyan")

invalid_year_txt1 = ("INVALID YEAR , Valid years : "+str(min_year)+" - "+str(max_year))
incorrect_year_text2 = colored(invalid_year_txt1,"yellow")

starting_year_text = colored("Enter year to begin investing :  ","cyan")
ending_year_text = colored("Enter year to end investing (uses data in 'x' year) :  ","cyan")


while end != "Y" :
    # These values reset for each run so the user can test different ranges and risk settings.
    risk = 0
    minimum_days = 2
    slippage = 0.001

    #starting year code
    starting_year = 0
    ending_year = 0

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
        
    plt.ylabel("PORTFOLIO (£)")
    plt.xlabel("YEAR")


    # Run the indicator class
    ind = IndicatorCalculator(closes,dates,minimum_days,period,overbuy,oversell)
    # Run the moving-average strategy first, then plot its portfolio curve.
    MA_signals = ind.moving_average()
    end_cash,portfolio,profit = calculate_portfolio(MA_signals,risk_percentage,starting_cash,opens,30,slippage,fees)
    end_cash_text = colored(round(end_cash,2),"red")
    profit_text = colored(round(profit,2),"red")
    print("Total end cash for MA :",end_cash_text)
    print("Profit for MA :",profit_text)

    #30 because portfolio for MA is 30 less than dates 
    portfolio_plot,dates_dt = graph_plot_values(dates,portfolio,30)
    plt.plot(dates_dt, portfolio_plot,label = "MA | Risk = "+str(risk) +"% | Profit =  £"+ str(round(profit,2))+ " | "+str(starting_year)+"→" + str(int(ending_year)+1))

    # Choose RSI thresholds manually, reuse the previous pair, or brute-force a new pair.
    overbuy,oversell = best_RSI_range(risk_percentage,starting_cash,opens,slippage,fees,prev_overbuy,prev_oversell,ind)
    prev_overbuy,prev_oversell = overbuy,oversell
    print("Best range for RSI found. Overbuy =",overbuy,"Oversell =",oversell)

    # Run the RSI strategy with the selected thresholds and plot the result.
    ind.overbuy = overbuy
    ind.oversell = oversell
    RSI_signals = ind.RSI_signals()
    rsi_offset = period + 3
    end_cash,portfolio,profit = calculate_portfolio(RSI_signals,risk_percentage,starting_cash,opens,rsi_offset,slippage,fees)
    end_cash_text = colored(round(end_cash,2),"red")
    profit_text = colored(round(profit,2),"red")
    print("Total end cash for RSI :",end_cash_text)
    print("Profit for RSI :",profit_text)
    
    portfolio_plot,dates_dt = graph_plot_values(dates,portfolio,rsi_offset)

    plt.plot(dates_dt, portfolio_plot,label = "RSI | Risk = "+str(risk) +"% | Profit =  £"+ str(round(profit,2)) +" | Overbuy = "+ str(overbuy) +" | Oversell = "+ str(oversell) + " | "+str(starting_year) +"→" + str(int(ending_year)+1))

    #x-axis year steps
    index = []
    amount = 0
    index_check_year = 0
    for i in dates_dt:
        year = (i.split("-"))[0]
        if index_check_year != year:
            index.append(amount)
            index_check_year = year
        amount += 1

    #  append the final date, as it falls the day before a new year (only if there is a sufficient gap of 100 
    # dates inbetween to prevent overcrowding)
    if len(dates_dt) - index[-1] > 100:
        index.append(len(dates_dt)-1)

    plt.xticks(index)

    plt.title("Backtesting Results")

    #display savings account at rate 5%
    def plot_savings():
        yvalues = [starting_cash]
        for i in range(0,((int(ending_year))-int(starting_year))):
            yvalues.append(yvalues[i]*(1.05))
        xvalues = [f"{year}-01-01" for year in range(int(starting_year)+1,int(ending_year)+1)]
        # just add the first date in dates_dt, into xvalues. This is because the first date of dates_dt can change
        xvalues.insert(0,dates_dt[0])
        plt.plot(xvalues,yvalues,label = "Savings Account (5% AER)")
    
    plot_savings()

    plt.legend(fontsize=8)
    plt.show(block=False)
    
    end = input("Quit(Y/N) : ").strip().upper()[:1]

# ATR — volatility measurement
# OBV — volume pressure
