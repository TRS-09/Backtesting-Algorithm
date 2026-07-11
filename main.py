import matplotlib.pyplot as plt
from termcolor import colored
from calculate_signals import IndicatorCalculator
from csv_processing import file_find_select, ProcessCSV
from portfolio import Portfolio
from rsi_range import best_RSI_range
from plot_run import PlotData

# Base RSI lookback. The RSI strategy later uses `period + 2` to match the original offsets.
period = 14

end = "N"
prev_overbuy = None
prev_oversell = None

overbuy = 0
oversell = 0

# Select and inspect the CSV once before entering the backtest loop
csv_data = ProcessCSV(file_find_select())
min_year = csv_data.min_year
max_year = csv_data.max_year

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
    dates, opens, closes = csv_data.load_price_data(starting_year, ending_year)

    if not dates:
        print(colored(f"No data found for year {starting_year}. Try a different year.", "yellow"))
        continue
        
    plt.ylabel("PORTFOLIO (£)")
    plt.xlabel("YEAR")


    # Run the indicator class
    ind = IndicatorCalculator(closes,dates,minimum_days,period,overbuy,oversell)

    # Run the moving-average strategy first, then plot its portfolio curve.
    MA_signals = ind.moving_average()

    MAportfolio = Portfolio(opens, risk_percentage, starting_cash, slippage, fees,MA_signals,30)
    end_cash_text = colored(round(MAportfolio.end_cash,2),"red")
    profit_text = colored(round(MAportfolio.profit,2),"red")
    print("Total end cash for MA :",end_cash_text)
    print("Profit for MA :",profit_text)

    #30 because portfolio for MA is 30 less than dates 
    MAplot = PlotData(dates,30,MAportfolio.portfolio)
    plt.plot(MAplot.calendar_dates, MAplot.portfolio_plot,label = "MA | Risk = "+str(risk) +"% | Profit =  £"+ str(round(MAportfolio.profit,2))+ " | "+str(starting_year)+"→" + str(int(ending_year)+1))

    # Choose RSI thresholds manually, reuse the previous pair, or brute-force a new pair.
    overbuy,oversell = best_RSI_range(risk_percentage,starting_cash,opens,slippage,fees,prev_overbuy,prev_oversell,ind,period,closes,dates,minimum_days)
    prev_overbuy,prev_oversell = overbuy,oversell
    print("Best range for RSI found. Overbuy =",overbuy,"Oversell =",oversell)

    # Run the RSI strategy with the selected thresholds and plot the result.
    rsi_offset = period + 3
    RSI_signals = IndicatorCalculator(closes, dates, minimum_days, period, overbuy, oversell).RSI_signals()
    RSIportfolio = Portfolio(opens, risk_percentage, starting_cash, slippage, fees,RSI_signals,period + 3)
    end_cash_text = colored(round(RSIportfolio.end_cash,2),"red")
    profit_text = colored(round(RSIportfolio.profit,2),"red")
    print("Total end cash for MA :",end_cash_text)
    print("Profit for MA :",profit_text) 

    #30 because portfolio for MA is 30 less than dates 
    RSIplot = PlotData(dates,period + 3,RSIportfolio.portfolio)
    plt.plot(RSIplot.calendar_dates, RSIplot.portfolio_plot,label = "MA | Risk = "+str(risk) +"% | Profit =  £"+ str(round(RSIportfolio.profit,2))+ " | "+str(starting_year)+"→" + str(int(ending_year)+1))

    #x-axis year steps
    index = []
    amount = 0
    index_check_year = 0
    for i in RSIplot.calendar_dates:
        year = (i.split("-"))[0]
        if index_check_year != year:
            index.append(amount)
            index_check_year = year
        amount += 1

    #  append the final date, as it falls the day before a new year (only if there is a sufficient gap of 100 
    # dates inbetween to prevent overcrowding)
    if len(RSIplot.calendar_dates) - index[-1] > 100:
        index.append(len(RSIplot.calendar_dates)-1)

    plt.xticks(index)

    plt.title("Backtesting Results")

    #display savings account at rate 5%
    def plot_savings(RSIplot):
        yvalues = [starting_cash]
        for i in range(1,((int(ending_year))-int(starting_year)+2)):
            yvalues.append(yvalues[i-1]*(1.05))
        xvalues = [f"{year}-01-01" for year in range(int(starting_year)+1,int(ending_year)+1)]
        # just add the first date in dates_dt, into xvalues. This is because the first date of dates_dt can change
        xvalues.insert(0,RSIplot.calendar_dates[0])
        xvalues.append(RSIplot.calendar_dates[-1])
        plt.plot(xvalues,yvalues,label = "Savings Account (5% AER)")
        
    
    plot_savings(RSIplot)

    plt.legend(fontsize=8)
    plt.show(block=False)
    
    end = input("Quit(Y/N) : ").strip().upper()[:1]

# ATR — volatility measurement
# OBV — volume pressure
