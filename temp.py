import sqlite3

connection = sqlite3.connect("storage.db")
cursor = connection.cursor()

cursor.execute("""DELETE FROM users""")
connection.commit()
