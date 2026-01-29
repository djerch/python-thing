'''context manager for database operations'''
import sqlite3

class DBCM:
    '''context manager class for database operations'''

    def __init__(self, path) -> None:
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.conn.commit()
        self.conn.close()
