import sqlite3

class database_funcs:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS login_info(username TEXT PRIMARY KEY, password TEXT)""")
        self.connection.commit()

    def create_login(self, user, pword):
        temp = self.cursor.execute(f"""SELECT username, password FROM login_info WHERE username = ?""", (user,))
        if temp.fetchone() is None:
            self.cursor.execute(f"""INSERT INTO login_info VALUES(?, ?)""", (user, pword,))
            self.connection.commit()
            return True
        else:
            return False

    def login_find(self, user):
        temp = self.cursor.execute(f"""SELECT username, password FROM login_info WHERE username = ?""", (user,))
        if temp.fetchone() is None:
            return False
        else:
            return True
        