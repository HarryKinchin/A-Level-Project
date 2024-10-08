import sqlite3
from flask import current_app
from flask import g

class database_funcs:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS login_info(username TEXT PRIMARY KEY, password TEXT)""")
        self.connection.commit()

    def login_find(self, user):
        print(self.cursor.execute(f"""SELECT username, password FROM login_info WHERE username = ?""", (user,)))
        
    def create_login(self, user, pword):
        self.cursor.execute(f"""INSERT INTO login_info ?, ?""", (user, pword,))