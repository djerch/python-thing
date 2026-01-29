'''prompts for user input and then does some stuff'''
import sys
import scrape_weather
import db_operations
import plot_operations

class WeatherProcessor:
    '''gathers user input to perform tasks'''

    def __init__(self) -> None:
        self.db = db_operations.DBOperations()
        self.plot = plot_operations.PlotOperations()

    def scrape(self):
        db = db_operations.DBOperations()
        print('starting webscrape')
        data = scrape_weather.scrape()
        db.purge_data()
        db.save_data(data)

    def box_plot(self):
        user_input = input('Enter the starting year to graph (ex. 2020): ')
        starting_year = user_input.strip()
        user_input = input('Enter the ending year to graph (ex. 2020): ')
        ending_year = user_input.strip()
        monthly = False
        data = self.db.fetch_data(starting_year, ending_year, monthly)
        print(f'graphing monthly weather data from {starting_year} to {ending_year}')
        self.plot.box_plot(data)

    def line_plot(self):
        print('Graph the mean values of a particular months data')
        user_input = input('Enter the year to graph (ex. 2020): ')
        year = user_input.strip()
        user_input = input('Enter the month to graph (ex. 09 or 9 for September): ')
        month = user_input.strip()
        if len(month) == 1:
            month = '0' + month
        monthly = True
        data = self.db.fetch_data(year, month, monthly)
        print(f'generating line plot from {year}-{month}')
        self.plot.line_plot(data)


print('Welcome to the weather processor\n' +
    'Please select an option\n' +
    '1. Download or update weather data\n' +
    '2. Generate box plot\n' +
    '3. Generate line plot\n' +
    '4. Exit')
user_input = input('Enter option number: ')
cleaned_input = float(user_input.strip())

myWeatherProcessor = WeatherProcessor()

if cleaned_input not in [1, 2, 3, 4]:
    print('Please enter a valid option')
else:
    if cleaned_input == 1:
        myWeatherProcessor.scrape()
    elif cleaned_input == 2:
        myWeatherProcessor.box_plot()
    elif cleaned_input == 3:
        myWeatherProcessor.line_plot()
    elif cleaned_input == 4:
        sys.exit('Exiting program')
