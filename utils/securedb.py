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

        if hash_alg == "scrypt":
            self.hash_params = {
                "n": 2**14,
                "r": 8,
                "p": 1
            }
        elif hash_alg == "sha512":
            self.hash_params = {
                "rounds": 15000
            }
        else:
            self.hash_params = {}
        # create database if not yet created
        self._init_table()

    def __del__(self):
        self.conn.close()

    def _validate_password(self, password: str) -> str | None:
        if len(password) < 5:
            return "Password is too short. Must be at least 5 characters."
        
        return None
    
    def _hash_password_scrypt(self, password: str, salt: bytes, n: int=2**14, r: int=8, p: int=1, maxmem: int=0, dklen: int=64) -> bytes:
        password_hash = hashlib.scrypt(
            password.encode(),      # password in bytes
            salt=salt,              # randomly generated salt
            n=n,                    # CPU / Memory cost factor
            r=r,                    # block size
            p=p,                    # parallelization factor
            maxmem=maxmem,          # maximum memory usage (0 = unlimited)
            dklen=dklen             # length of derived key
        )
        return password_hash

    def _hash_password_sha512(self, password: str, salt: bytes, rounds: int = 10000) -> bytes:
        password_hash = password.encode() + salt

        for _ in range(rounds):
            password_hash = hashlib.sha512(password_hash).digest()

        return password_hash

    def _pack_mcf(self, hash_alg: str, parameters: dict[str, int], salt: bytes, password_hash: bytes):
        parameter_str = ",".join(f"{k}={v}" for k, v in parameters.items()) if parameters else ""

        print(f"parameter string = {parameter_str}")
        print(f"parameter items = {parameters.items()}")
        salt_str = salt.hex()
        password_hash_str = password_hash.hex()

        if parameter_str:
            mcf_str = f"${hash_alg}${parameter_str}${salt_str}${password_hash_str}"
        else:
            mcf_str = f"${hash_alg}${salt_str}${password_hash_str}"

        return mcf_str


    def _unpack_mcf(self, mcf: str):
        parts = mcf.split("$")
        if len(parts) < 4:
            raise ValueError("Invalid MCF string")

        hash_alg = parts[1]

        if len(parts) == 5:  # with parameters
            param_str, salt_hex, hash_hex = parts[2], parts[3], parts[4]
            parameters = {}
            if param_str:
                for kv in param_str.split(","):
                    k, v = kv.split("=", 1)
                    parameters[k] = int(v)
        elif len(parts) == 4:  # no parameters
            parameters = {}
            salt_hex, hash_hex = parts[2], parts[3]
        else:
            raise ValueError("Invalid MCF string format")

        salt = bytes.fromhex(salt_hex)
        password_hash = bytes.fromhex(hash_hex)

        return hash_alg, parameters, salt, password_hash

    def _init_table(self):
        """creates users table if it does not exist already"""
        cur = self.conn.cursor()
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT UNIQUE NOT NULL,
                            username TEXT UNIQUE NOT NULL,
                            mcf_string TEXT NOT NULL
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
            print(f"scrypt parameters = {self.hash_params}")
            password_hash = self._hash_password_scrypt(password, salt, **self.hash_params)
        elif self.hash_alg == "sha512":
            password_hash = self._hash_password_sha512(password, salt, **self.hash_params)
        elif self.hash_alg == "plaintext_salt":
            password_hash = password.encode() + salt
        else:
            raise ValueError(f"Error: SecureDB add_user given an invalid hash algorithm '{self.hash_alg}'")
        
        # turn password hash into modular-crypt format (MCF)
        mcf_str = self._pack_mcf(self.hash_alg, self.hash_params, salt, password_hash)

        # add entry to database
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO users (email, username, mcf_string) VALUES (?, ?, ?)", (email, username, mcf_str))
            self.conn.commit()
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
        cur.execute("SELECT mcf_string FROM users WHERE username = ?", (username,))

        mcf_str = cur.fetchone()[0]
        if not mcf_str:
            return False
        
        hash_alg, parameters, salt, stored_hash = self._unpack_mcf(mcf_str)

        if hash_alg is None:
            hash_alg = self.hash_alg

        if hash_alg == "scrypt":
            test_hash = self._hash_password_scrypt(password, salt, **parameters)
        elif hash_alg == "sha512":
            test_hash = self._hash_password_sha512(password, salt, **parameters)
        elif hash_alg == "plaintext_salt":
            test_hash = password.encode() + salt
        else:
            raise ValueError(f"Error: SecureDB add_user given an invalid hash algorithm '{hash_alg}'")

        return test_hash == stored_hash

    