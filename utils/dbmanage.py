import sqlite3
from enum import Enum

class Users(Enum):
    ID = 0
    username = 1
    password = 2


class DBManager():
    def __init__(self, dbfp: str):
        self.dbfp = dbfp

    def add_entry(self, username, password_digest):
        with sqlite3.connect(self.dbfp) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_digest))

    def get_entry_from_id(self, id):
        pass

    def get_entry_from_username(self, username):
        pass