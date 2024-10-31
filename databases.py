import sqlite3
from argon2 import PasswordHasher

class logins_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
                            (userID INT PRIMARY KEY, 
                            username TEXT, 
                            password TEXT, 
                            email TEXT)""")
        self.connection.commit()
        self.ph = PasswordHasher

    def create_login(self, user, pword):
        temp = self.cursor.execute(f"""SELECT username, password FROM login_info WHERE username = ?""", (user,))
        if temp.fetchone() is None:
            hashed_pword = PasswordHasher.hash(pword)
            self.cursor.execute(f"""INSERT INTO login_info VALUES(?, ?)""", (user, hashed_pword,))
            self.connection.commit()
            return True
        else:
            return False

    def login_find(self, user, pword):
        uname_check = self.cursor.execute(f"""SELECT username, password FROM login_info WHERE username = ?""", (user,))
        hashed_pword = PasswordHasher.hash(pword)
        pword_check = self.cursor.execute(f"""SELECT username, password FROM login_info WHERE username = ?""", (hashed_pword),)
        if uname_check.fetchone() is None or pword_check.fetchone() is None :
            return False
        else:
            return True
        
class subjects_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS subjects
                            (subjectID INT PRIMARY KEY, 
                            subjectName TEXT)""")
        self.connection.commit()

class subuser_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS usersubjects
                            (userSubjectID INT PRIMARY KEY, 
                            userID INT, 
                            subjectID INT,
                            FOREIGN KEY (userID) REFERENCES users (userID),
                            FOREIGN KEY (subjectID) REFERENCES subjects (subjectID)))""")
        self.connection.commit()

class questions_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS questions
                            (questionID INT PRIMARY KEY,
                            subjectID INT,
                            topicID INT,
                            question TEXT,
                            answer TEXT,
                            FOREIGN KEY (subjectID) REFERENCES subjects (subjectID),
                            FOREIGN KEY (topicID) REFERENCES topics (topicID))""")
        self.connection.commit()

class topic_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS topics
                            (topicID INT PRIMARY KEY,
                            subjectID INT,
                            topicName TEXT,
                            FOREIGN KEY (subjectID) REFERENCES subjects (subjectID))""")
        self.connection.commit()

