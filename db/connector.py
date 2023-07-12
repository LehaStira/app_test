import sqlite3

from db import DB_NAME


class SQliteConnector:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
