'''generates various plots when given data'''

import matplotlib.pyplot as plt

class PlotOperations():
    '''generates various plots when given data'''

    def __init__(self) -> None:
        self.data = []
        self.month_list = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December']

    def box_plot(self, data):
        '''generates a box plot from given data'''

        weather = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}

        first_year = data[len(data) - 1][0].split('-')[0]
        final_year = data[0][0].split('-')[0]

        for row in data:
            month = int(row[0][5:7])
            weather[month].append(row[3])

        temps = list(weather.values())

        plt.figure()
        plt.boxplot(temps)
        plt.title(f'Monthly Temperature Distribution for: {first_year} to {final_year}')
        plt.xlabel('Month')
        plt.ylabel('Temperature (Celsius)')
        plt.show()

    def line_plot(self, data):
        '''generates a line plot from given data'''

        dates = []
        temps = []
        month = data[0][0].split('-')[1]
        year = data[0][0].split('-')[0]

        for row in data:
            dates.append(row[0])
            temps.append(row[3])

        plt.figure()
        plt.plot(dates, temps)
        plt.xticks(rotation=45, ha='right')
        plt.title(f'Average Daily Temperatures for {self.month_list[int(month) - 1]} {year}')
        plt.xlabel('Date')
        plt.ylabel('Average Temperature')
        plt.show()
