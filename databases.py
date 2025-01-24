import sqlite3
from argon2 import PasswordHasher

class users_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
                            (userID INTEGER PRIMARY KEY AUTOINCREMENT, 
                            username TEXT, 
                            password TEXT, 
                            email TEXT)""")
        self.connection.commit()
        self.ph = PasswordHasher()

    def create_login(self, user, pword, email):
        exists = self.cursor.execute("""SELECT username, password FROM users WHERE username = ?""", (user,))
        if exists.fetchone() is None:
            hashed_pword = self.ph.hash(pword)
            self.cursor.execute("""INSERT INTO users(username, password, email) VALUES(?, ?, ?)""", (user, hashed_pword, email,))
            self.connection.commit()
            return True
        else:
            return False

    def login_find(self, user, pword, email):
        uname_check = self.cursor.execute("""SELECT username FROM users WHERE username = ?""", (user,))
        uname_check = uname_check.fetchone()
        email_check = self.cursor.execute("""SELECT email FROM users WHERE email =?""", (email,))
        email_check = email_check.fetchone()
        if uname_check is None or email_check is None:
            return False
        else:
            pword_check = self.cursor.execute("""SELECT password FROM users WHERE username = ?""", (user,))
            if self.ph.verify(pword_check.fetchone()[0], pword):
                return True
            else:
                return False

    def userID_get(self, user, pword, email):
        hashed_pword = self.ph.verify(self.cursor.execute("""SELECT password FROM users WHERE username = ?""", (user,)).fetchone()[0], pword)
        if hashed_pword:
            id_found = self.cursor.execute(f"""SELECT userID FROM users WHERE username = '{user}' AND email = '{email}'""")
            id = id_found.fetchone()[0]
        return id
    
class subjects_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS subjects
                            (subjectID INTEGER PRIMARY KEY AUTOINCREMENT, 
                            subjectName TEXT)""")
        self.connection.commit()

    def subID_to_sub(self, subject_id):
        subjects = []
        for item in subject_id:
            self.cursor.execute(f"""SELECT subjectName FROM subjects WHERE subjectID = '{item}'""")
            subjects.append(self.cursor.fetchall()[0])
        print('subjects from func', subjects)
        return subjects
        
class subject_user_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS usersubjects
                            (userID INTEGER, 
                            subjectID INTEGER,
                            FOREIGN KEY (userID) REFERENCES users (userID),
                            FOREIGN KEY (subjectID) REFERENCES subjects (subjectID))""")
        self.connection.commit()

    def subID_get(self, userID):
        self.cursor.execute(f"""SELECT subjectID FROM usersubjects WHERE userID = '{userID}'""")
        sub_id = self.cursor.fetchall()
        print('sub_id',sub_id)
        if sub_id == []:
            return ''
        else:
            return subjects_table.subID_to_sub(self, sub_id)

    def subject_change(self, userID):
        current_subjects = self.subID_get(userID)
        print('current subjects',current_subjects)
        
            
class questions_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS questions
                            (questionID INTEGER PRIMARY KEY AUTOINCREMENT,
                            subjectID INTEGER,
                            topicID INTEGER,
                            question TEXT,
                            answer TEXT,
                            question_type TEXT,
                            FOREIGN KEY (subjectID) REFERENCES subjects (subjectID),
                            FOREIGN KEY (topicID) REFERENCES topics (topicID))""")
        self.connection.commit()

class topic_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS topics
                            (topicID INTEGER PRIMARY KEY AUTOINCREMENT,
                            subjectID INTEGER,
                            topicName TEXT,
                            qualification TEXT,
                            FOREIGN KEY (subjectID) REFERENCES subjects (subjectID))""")
        self.connection.commit()

class user_progress_table:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS user_progress
                            (topicID INTEGER,
                            userID INTEGER,
                            progress INTEGER,
                            FOREIGN KEY (topicID) REFERENCES topics (topicID)
                            FOREIGN KEY (userID) REFERENCES users (userID))""")
        self.connection.commit()