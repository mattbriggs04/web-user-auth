import sqlite3
import hashlib
import os
from enum import Enum

class SecureDB():
    def __init__(self, db_path: str, hash_alg: str="scrypt"):
        # initialize class variables
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.hash_alg = hash_alg

        # create database if not yet created
        self._init_table()

    def __del__(self):
        self.conn.close()

    def _validate_password(self, password: str) -> str | None:
        # if len(password) < 10:
        #     return "Password is too short. Must be at least 10 characters."
        
        return None
    
    def _hash_password_scrypt(self, password: str, salt: bytes) -> bytes:
        password_hash = hashlib.scrypt(
            password.encode(),  # password in bytes
            salt=salt,          # randomly generated salt
            n=2**14,            # CPU / Memory cost factor
            r=8,                # block size
            p=1,                # parallelization factor
            maxmem=0,           # maximum memory usage (0 = unlimited)
            dklen=64            # length of derived key
        )
        return password_hash

    def _hash_password_sha512(self, password: str, salt: bytes, num_rounds: int = 10000) -> bytes:
        password_hash = password.encode() + salt

        for _ in range(num_rounds):
            password_hash = hashlib.sha512(password_hash).digest()

        return password_hash

    def _init_table(self):
        """creates users table if it does not exist already"""
        cur = self.conn.cursor()
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT UNIQUE NOT NULL,
                            username TEXT UNIQUE NOT NULL,
                            password_hash BLOB NOT NULL,
                            salt BLOB NOT NULL
                        );
                    """)
        self.conn.commit()

    def add_user(self, email: str, username: str, password: str) -> str | None:
        """adds a new user to users table"""
        # ensure the password meets criteria
        err_msg = self._validate_password(password)
        if err_msg is not None:
            return err_msg
        
        # generate password hash to store in database
        salt = os.urandom(16)
        if self.hash_alg == "scrypt":
            password_hash = self._hash_password_scrypt(password, salt)
        elif self.hash_alg == "sha512":
            password_hash = self._hash_password_sha512(password, salt)
        else:
            raise ValueError(f"Error: SecureDB add_user given an invalid hash algorithm '{self.hash_alg}'")
        
        # add entry to database
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO users (email, username, password_hash, salt) VALUES (?, ?, ?, ?)", (email, username, password_hash, salt))
            self.conn.commit()
            print("successfully committed user")
        except sqlite3.IntegrityError as e:
            msg = str(e).lower()
            if "username" in msg:
                err_msg = "Error: Username already exists"
            elif "email" in msg:
                err_msg = "Error: Email already exists"
            else:
                err_msg = "Duplicate entry"
            return err_msg

        return None
    
    def check_credentials(self, username: str, password: str) -> bool:
        """checks if a username-password pair is valid"""
        cur = self.conn.cursor()
        cur.execute("SELECT password_hash, salt FROM users WHERE username = ?", (username,))

        row = cur.fetchone()
        if not row:
            return False
        stored_hash, salt = row

        if self.hash_alg == "scrypt":
            test_hash = self._hash_password_scrypt(password, salt)
        elif self.hash_alg == "sha512":
            test_hash = self._hash_password_sha512(password, salt)
        else:
            raise ValueError(f"Error: SecureDB add_user given an invalid hash algorithm '{self.hash_alg}'")

        return test_hash == stored_hash

    