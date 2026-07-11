# Build plot-friendly x/y series that include non-trading calendar days.
from datetime import datetime,timedelta
import copy

class PlotData:
    def __init__(self,dates,delay,portfolio_values):
        self.calendar_dates = self.plotting_dates(dates)
        self.dates = dates
        self.delay = delay
        self.portfolio_plot = self.graph_plot_values(dates,portfolio_values,delay)

    def plotting_dates(self,dates):
        """
        Converts dates from CSV where there is gaps on weekends, and fills in gaps on weekends (essential for matplot)
        Input is expected to be trading dates (YYYY-MM-DD) in ascending order.
        """
        dates_plt = []
        # Walk through adjacent pairs and measure the day gap between them.
        for i in range(0,len(dates)-1):
            prev_date,present_date = datetime.strptime(dates[i],"%Y-%m-%d"),datetime.strptime(dates[i+1],"%Y-%m-%d")
            consecutive,gap = ((present_date - prev_date).days == 1),((present_date - prev_date).days)-1
            if consecutive:
                # Normal trading-day step: append the current normal day.
                dates_plt.append(str(prev_date.date()))
            if not consecutive:
                # Gap detected: add current day first, then fill each missing day.
                dates_plt.append(str(prev_date.date()))
                for j in range(0, gap):
                    new_date = prev_date + timedelta(days = 1)
                    prev_date = copy.deepcopy(new_date)
                    dates_plt.append(str(new_date.date()))
        # The loop appends the "left" date of each pair, so add the last original date here.
        dates_plt.append(dates[-1])
        return dates_plt

    def graph_plot_values(self,dates,portfolio_values,delay):
        """
        Expand portfolio values to match calendar dates for plotting.

        Pad the portfolio with NONE until offset
        If trade day == calender day, append portfolio value, else append previous portfolio

        """
        # Convert trading-day delay into the equivalent calendar-day index.
        offset = self.find_offset(self.calendar_dates,dates,delay)
        new_portfolio_values = []
        # Left-pad with None so y starts at same calendar index as first portfolio value.
        for x in range(offset):
            new_portfolio_values.append(None)
        j=0
        for i in self.calendar_dates[offset:]:
            # Carry forward last known portfolio value across market-closed days.
            prev_value = portfolio_values[j]
            if i in dates:
                new_portfolio_values.append(portfolio_values[j])
                j += 1
            else:
                new_portfolio_values.append(prev_value)
        return new_portfolio_values

    def find_offset(self,plting_dates,dates,delay):
        """
        Map trading-day delay -> calendar-day offset in `plting_dates`.

        Example: if delay=30, locate `dates[30]` inside the calendar-expanded list.
        The index where it appears is the number of calendar points to skip/pad.
        """
        trade_date = dates[delay]
        offset = 0
        for i in plting_dates:
            if trade_date != i:
                offset += 1
            else:
                break
        return offset
