'''class using HTMLParser to scrape Winnipeg weather data from the Environment Canada website'''

from html.parser import HTMLParser
import urllib.request

class MyHTMLParser(HTMLParser):
    '''scrapes Winnipeg weather data from the Environment Canada website'''

    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.tbody_tag = False
        self.table_row_tag = False
        self.td_tag = False
        self.valid_row = False
        self.count = 0
        self.date = ''
        self.base_url = 'https://climate.weather.gc.ca'
        self.previous = ''
        self.end_of_page = False
        self.end = False
        self.last_page = False
        self.get_day = False
        self.months = (
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
            'December')
        self.daily_temps = {}
        self.weather = {}

    def handle_starttag(self, tag, attrs):

        if tag == 'tr':
            self.table_row_tag = True

        if tag == 'td':
            self.td_tag = True

        # if tag == 'a' and attrs[0][1].startswith('generate_chart'):
        #     splits = attrs[0][1].split('&')
        #     month = splits[6].split('=')[1]
        #     year = splits[5].split('=')[1]
        #     self.date = year + '-' + month

        if tag == 'a' and attrs[0][1].startswith('/climate_data/hourly_data'):
            splits = attrs[0][1].split('&')
            day = splits[4].split('=')[1]
            if len(day) == 1:
                day = '0' + day
            month = splits[6].split('=')[1]
            if len(month) == 1:
                month = '0' + month
            year = splits[5].split('=')[1]
            if year == '2018':
                self.previous = ''
                self.end = True
            self.date = year + '-' + month + '-' + day
            self.valid_row = True

        # if tag == 'abbr' and attrs[0][1].startswith(self.months):
        #     self.getDay = True
        #     self.validRow = True

        if tag == 'a' and attrs[0][1].startswith('#legend'):
            self.valid_row = False

        if tag == 'li' and attrs != []:
            if attrs[0][1] == 'nav-prev2':
                print('this thing')
                if attrs[1][1] == 'previous':
                    self.end_of_page = True
                # if attrs[1][1] == 'previous disabled':
                #     self.previous = ''
                #     self.end = True
                #     print('end of scraping')

        if tag == 'a' and attrs[0][1] == 'prev' and self.end != True and self.end_of_page:
            self.previous = self.base_url + attrs[1][1]
            self.end_of_page = False

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.table_row_tag = False
            self.td_tag = False
            self.count = 0
            if self.valid_row:
                self.weather[self.date] = self.daily_temps
                #print(self.daily_temps)
            self.valid_row = False
            self.daily_temps = {}
            self.date = ''
        if tag == 'td':
            self.td_tag = False
            self.count = self.count + 1

    def handle_data(self, data):

        if self.td_tag and self.valid_row:
            if self.count == 0:
                self.daily_temps['Max'] = float(data)
            if self.count == 1:
                self.daily_temps['Min'] = float(data)
            if self.count == 2:
                self.daily_temps['Mean'] = float(data)

def scrape():
    '''feeds html to HTMLParser from the url'''

    myHTMLParser = MyHTMLParser()

    with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2022&Month=12#') as response:
        html = str(response.read())

    myHTMLParser.feed(html)
    
    # with urllib.request.urlopen(myHTMLParser.previous) as response:
    #     html = str(response.read())

    # myHTMLParser.feed(html)

    while myHTMLParser.previous != '':
        print(myHTMLParser.previous)

        with urllib.request.urlopen(myHTMLParser.previous) as response:
            html = str(response.read())
            myHTMLParser.feed(html)

    return myHTMLParser.weather
    # print(myHTMLParser.weather)
