import sqlite3
#ALWAYS KEEP QUOTES
connection = sqlite3.connect("storage.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS loginInfo(username TEXT PRIMARY KEY, password TEXT)""")
cursor.execute(f"""INSERT INTO loginInfo(username, password) VALUES('{uname}', 'Ism311lik3b4ll5')""")
connection.commit()
