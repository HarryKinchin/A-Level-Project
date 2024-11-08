import sqlite3
from argon2 import PasswordHasher

ph = PasswordHasher()

connection = sqlite3.connect("storage.db")
connection.execute("PRAGMA foreign_keys = 1")
cursor = connection.cursor()

