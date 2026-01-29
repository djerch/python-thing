'''does some cool database stuff'''
from dbcm import DBCM

class DBOperations():
    '''does some cool database stuff'''

    def __init__(self) -> None:
        self.db = 'weather.sqlite'
        self.initialize_db()

    def fetch_data(self, start_date, end_date, monthly):
        '''fetches data from database'''

        if monthly:
            start = start_date + '-' + end_date + '-01'
            end = start_date + '-' + end_date + '-31'
        else:
            start = start_date + '-01-01'
            end = end_date + '-12-31'
        weather = []

        try:
            with DBCM(self.db) as cursor:
                for row in cursor.execute(f'''
                        SELECT SAMPLE_DATE, MIN_TEMP, MAX_TEMP, AVG_TEMP
                        FROM SAMPLES
                        WHERE SAMPLE_DATE
                        BETWEEN '{start}' AND '{end}'
                        '''):
                    weather.append(row)

            # with DBCM(self.db) as cursor:
            #     for row in cursor.execute('SELECT SAMPLE_DATE, MIN_TEMP, MAX_TEMP, AVG_TEMP FROM SAMPLES'):
            #         weather.append(row)

            print('data fetched')

        except Exception as exception:
            print('could not fetch data:', exception)

        return weather

    def save_data(self, data) -> None:
        '''saves data to database'''

        try:
            weather_data = []
            for row in data:
                if row != {}:
                    weather_data.append((row, 'Winnipeg, MB', data[row]['Max'], data[row]['Min'], data[row]['Mean']))

            with DBCM(self.db) as cursor:
                sql = '''insert into samples (SAMPLE_DATE, LOCATION, MIN_TEMP, MAX_TEMP, AVG_TEMP) values(?, ?, ?, ?, ?)'''

                cursor.executemany(sql, weather_data)

            print('data inserted')

        except Exception as exception:
            print('could not save data:', exception)

        # for row in cursor.execute('SELECT SAMPLE_DATE, LOCATION, MIN_TEMP, MAX_TEMP, AVG_TEMP FROM SAMPLES'):
        #     print(row)

    def initialize_db(self) -> None:
        '''initializes the database'''

        try:
            with DBCM(self.db) as cursor:
                cursor.execute(''' CREATE TABLE samples(
                                id         INTEGER PRIMARY KEY AUTOINCREMENT, 
                                sample_date       TEXT NOT NULL, 
                                location   TEXT NOT NULL,
                                min_temp   REAL NOT NULL, 
                                max_temp   REAL NOT NULL,
                                avg_temp   REAL NOT NULL
                                )'''
                            )

            print('db created')

        except Exception as exception:
            print('could not initialize database:', exception)

    def purge_data(self) -> None:
        '''purges all data from database'''

        try:
            with DBCM(self.db) as cursor:
                cursor.execute('DELETE FROM samples')

            print('data deleted')

        except Exception as exception:
            print('could not purge database:', exception)

# weather = {'2018-06-01': {'Max': 12.0, 'Min': 5.6, 'Mean': 7.1},
#             '2018-06-02': {'Max': 22.2, 'Min': 11.1, 'Mean': 15.5},
#             '2018-06-03': {'Max': 31.3, 'Min': 29.9, 'Mean': 30.0}}
#initialize_db()
#insert(weather)
