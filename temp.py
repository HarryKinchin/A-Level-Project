import sqlite3
from argon2 import PasswordHasher
ph = PasswordHasher()
connection = sqlite3.connect("storage.db")
cursor = connection.cursor()

connection.commit()
