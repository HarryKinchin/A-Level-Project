import sqlite3
from argon2 import PasswordHasher

connection = sqlite3.connect("storage.db")
connection.execute("PRAGMA foreign_keys = 1")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS questions
                            (questionID INT PRIMARY KEY,
                            subjectID INT,
                            topicID INT,
                            question TEXT,
                            answer TEXT,
                            FOREIGN KEY (subjectID) REFERENCES subjects (subjectID),
                            FOREIGN KEY (topicID) REFERENCES topics (topicID))""")

connection.commit()