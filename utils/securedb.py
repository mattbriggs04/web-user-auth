import sqlite3
from sha512 import SHA512
from enum import Enum

class Users(Enum):
    ID = 0
    username = 1
    password = 2

class SecureDB():
    def __init__(self, db_path: str, salt_rounds: int = 12):
        self.db_path = db_path
        self.salt_rounds = salt_rounds
        
        self.conn = sqlite3.connect(db_path)

    def add_entry(self, username, password_digest):
        with sqlite3.connect(self.dbfp) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_digest))

    def get_entry_from_id(self, id):
        pass

    def get_entry_from_username(self, username):
        pass