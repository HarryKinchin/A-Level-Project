import sqlite3
#ALWAYS KEEP QUOTES
connection = sqlite3.connect("storage.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS loginInfo(username TEXT PRIMARY KEY, password TEXT)""")
connection.commit()
