import sqlite3

connection = sqlite3.connect("storage.db")
connection.execute("PRAGMA foreign_keys = 1")
cursor = connection.cursor()

cursor.execute("""DELETE FROM users WHERE userID=7""")
connection.commit()