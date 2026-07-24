from pathlib import Path

from termcolor import colored

# Show available CSV files and return the user-selected path.
def file_find_select():
    file_name_lst = []
    file_lst = []
    print("")
    folder = Path("/Users/teosmith/Desktop/CSV_for_Backtesting")
    for file in folder.glob("*.csv"):
        file_name_lst.append(file.name)
        file_lst.append(file)
    for i in range(0, len(file_lst)):
        file_choice_txt = colored(
            ("Option " + str(i + 1) + " = " + str(file_name_lst[i])),
            "magenta",
            attrs=["bold"],
        )
        print(file_choice_txt)
    file_choice = int(input("Enter CSV option : "))
    print("")
    return file_lst[file_choice - 1]

class ProcessCSV:
    def __init__(self,file):
        self.file = file
        self.opens_loc, self.closes_loc, self.date_loc, self.descendingcsv = self.filetype()
        self.min_year, self.max_year = self.year_range()

    def filetype(self):
        # finds out the format of the file
        with open(self.file, "r") as f:
            f_line = (f.readline().strip("\n")).split(",")
            opens_loc = f_line.index("Open")
            closes_loc = f_line.index("Close")
            date_loc = f_line.index("Date")

            # find if its descending and ensure its not between a month, if it is, go down a few lines and recheck
            f_line1 = (f.readline().strip("\n")).split(",")
            f_line2 = (f.readline().strip("\n")).split(",")
            if ((f_line1[date_loc].split("-"))[1] == (f_line2[date_loc].split("-"))[1]) and (
                (f_line1[date_loc].split("-"))[2] > (f_line2[date_loc].split("-"))[2]
            ):
                descendingcsv = True
            else:
                descendingcsv = False
            if (f_line1[date_loc].split("-"))[1] != (f_line2[date_loc].split("-"))[1]:
                f_line1 = f_line2
                f_line2 = (f.readline().strip("\n")).split(",")
                if (f_line1[date_loc].split("-"))[2] > (f_line2[date_loc].split("-"))[2]:
                    descendingcsv = True
                else:
                    descendingcsv = False

            return opens_loc, closes_loc, date_loc, descendingcsv

    # Return the minimum and maximum year available in the selected CSV.
    def year_range(self):
        max_year = 0
        min_year = 0
        with open(self.file, "r") as f:
            f.readline()
            min_year = int((((f.readline().strip("\n")).split(",")[self.date_loc]).split("-"))[0])
            for line in f:
                year = int((((line.strip("\n")).split(",")[self.date_loc]).split("-"))[0])
                if year < min_year:
                    min_year = year
                if year > max_year:
                    max_year = year
        return min_year, max_year

    # Load only the requested date window and return matching date/open/close lists.
    def load_price_data(self, starting_year, ending_year):
        dates = []
        opens = []
        closes = []
        start = False

        with open(self.file, "r") as f:
            f.readline()
            if self.descendingcsv == False:
                for line in f:
                    line = line.split(",")
                    date = (line[self.date_loc].split("-"))
                    if len(date) == 3 and date[0] == starting_year:
                        # tells the code to begin appending the closes etc, to the variables as the selected year has passed
                        start = True

                    if len(date) == 3 and date[0] == str(int(ending_year) + 1):
                        # stops appending variables
                        start = False

                    if start == True:
                        dates.append(line[self.date_loc])
                        opens.append(float(line[self.opens_loc]))
                        closes.append(float(line[self.closes_loc]))
            else:
                row = []
                for line in f:
                    split = line.split(",")
                    row.append(split)

                for line in reversed(row):
                    date = (line[self.date_loc]).split("-")
                    if len(date) == 3 and date[0] == starting_year:
                        # tells the code to begin appending the closes etc, to the variables as the selected year has passed
                        start = True
                    if len(date) == 3 and date[0] == str(int(ending_year) + 1):
                        # stops appending variables
                        start = False
                    if start == True:
                        dates.append((line[self.date_loc]))
                        opens.append(float(line[self.opens_loc]))
                        closes.append(float(line[self.closes_loc]))
        return dates, opens, closes
