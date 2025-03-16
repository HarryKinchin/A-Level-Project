import sqlite3
import re
from argon2 import PasswordHasher

class UsersTable:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
                            (userID INTEGER PRIMARY KEY AUTOINCREMENT, 
                            username TEXT NOT NULL, 
                            password TEXT NOT NULL, 
                            email TEXT NOT NULL)""")
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

    def login_check(self, user, pword, email):
        uname_check = self.cursor.execute("""SELECT username FROM users WHERE username = ?""", (user,))
        uname_check = uname_check.fetchone()
        email_check = self.cursor.execute("""SELECT email FROM users WHERE email = ?""", (email,))
        email_check = email_check.fetchone()
        if uname_check is None or email_check is None:
            return False
        else:
            pword_check = self.cursor.execute("""SELECT password FROM users WHERE username = ?""", (user,))
            if self.ph.verify(pword_check.fetchone()[0], pword):
                return True
            else:
                return False
            
    def change_details(self, userID, old_pass, new_details):
        try:
            self.ph.verify(self.cursor.execute("""SELECT password FROM users WHERE userID=?""", (userID,)).fetchone()[0], old_pass)
            if new_details["new_pass"] != '':
                new_hashed_pword = self.ph.hash(new_details["new_pass"])
                self.cursor.execute(f"""UPDATE users password=? WHERE userID={userID}""", (new_hashed_pword,))
                self.connection.commit()
            else:
                pass
            if new_details["new_uname"] != '':
                self.cursor.execute(f"""UPDATE users username=? WHERE userID={userID}""", (new_details["new_uname"],))
                self.connection.commit()
            else:
                pass
            if new_details["new_email"] != '':
                self.cursor.execute(f"""UPDATE users email=? WHERE userID={userID}""", (new_details["new_email"],))
                self.connection.commit()
            else:
                pass
            return True
        except:
            pass
            return False

    def userID_get(self, user, pword, email):
        hashed_pword = self.ph.verify(self.cursor.execute("""SELECT password FROM users WHERE username = ?""", (user,)).fetchone()[0], pword)
        if hashed_pword:
            id_found = self.cursor.execute(f"""SELECT userID FROM users WHERE username = ? AND email = ?""", (user, email,))
            id = id_found.fetchone()[0]
        return id
    
class SubjectsTable:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS subjects
                            (subjectID INTEGER PRIMARY KEY AUTOINCREMENT, 
                            subjectName TEXT NOT NULL)""")
        self.connection.commit()

    def subIDs_to_sub(self, subject_ids):
        subjects = []
        for item in subject_ids:
            self.cursor.execute(f"""SELECT subjectName FROM subjects WHERE subjectID = ?""", (item,))
            subjects.append(self.cursor.fetchone()[0])
        return subjects
    
    def subs_to_subID(self, subjects):
        subjectIDs = []
        for item in subjects:
            self.cursor.execute(f"""SELECT subjectID FROM subjects WHERE subjectName = ?""", (item,))
            subjectIDs.append(self.cursor.fetchall()[0])
        return subjectIDs
        
class SubjectUserTable:
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

    def subIDs_get_from_userID(self, userID):
        self.cursor.execute(f"""SELECT subjectID FROM usersubjects WHERE userID = ?""", (userID,))
        sub_id = self.cursor.fetchall()
        if sub_id == []:
            return ''
        else:
            return sub_id

    def subject_change(self, userID, changing_subjectIDs):
        for item in changing_subjectIDs:
            sub_change = item.split(',')
            self.cursor.execute(f"""SELECT subjectID FROM usersubjects WHERE subjectID={sub_change[0]}""")
            sub_found = self.cursor.fetchall()
            if sub_change[1] == 'true' and sub_found == []:                         #add subject to table
                self.cursor.execute("""INSERT INTO usersubjects VALUES(?,?)""", (userID, sub_change[0],))
            elif sub_change[1] == 'false' and sub_found == [int(sub_change[0])]:    #remove from table
                self.cursor.execute("""DELETE FROM usersubjects WHERE subjectID=? AND userId=?""", (sub_found[0], userID,))                                                                  #do nothing
            self.connection.commit()

class TopicsTable:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS topics
                            (topicID INTEGER PRIMARY KEY AUTOINCREMENT,
                            subjectID INTEGER,
                            topicName TEXT NOT NULL,
                            qualification TEXT NOT NULL,
                            FOREIGN KEY (subjectID) REFERENCES subjects (subjectID))""")
        self.connection.commit()
    
    def get_topics(self, subID):
        topics = []
        for item1 in subID:
            self.cursor.execute(f"""SELECT topicName FROM topics WHERE subjectID={item1}""")
            fetched_topics = self.cursor.fetchall()
            for item2 in fetched_topics:
                topics.append([item1, item2])
        if topics == []:
            return ''
        else:
            return topics
        
    def topic_to_topicID(self, topics):
        topicIDs = []
        for item1 in topics:
            self.cursor.execute(f"""SELECT topicID FROM topics WHERE topicName = ?""", (item1,))
            fetched_topics = self.cursor.fetchall()
            for item2 in fetched_topics:
                topicIDs.append(item2)
        return topicIDs

class QuestionsTable:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS questions
                            (questionID INTEGER PRIMARY KEY AUTOINCREMENT,
                            topicID INTEGER,
                            question TEXT NOT NULL,
                            answer TEXT NOT NULL,
                            answer_keywords TEXT,
                            question_type TEXT NOT NULL,
                            FOREIGN KEY (topicID) REFERENCES topics (topicID))""")
        self.connection.commit()

    def create_question(self, question_data):
        keywords_list = re.findall(r"\*[A-Za-z0-9 ]+\*", question_data["answer"])
        keywords = "-".join(keywords_list)
        topicId = TopicsTable.topic_to_topicID(self, [question_data["topic"]])
        self.cursor.execute("""INSERT INTO questions(topicID, question, answer, answer_keywords, question_type) VALUES(?, ?, ?, ?, ?)""", (topicId[0], question_data["name"], question_data["answer"], keywords, question_data["type"], ))
        self.connection.commit()

class UserProgressTable:
    def __init__(self):
        self.connection = sqlite3.connect("storage.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.connection.row_factory = lambda cursor, row: row[0]
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS user_progress
                            (topicID INTEGER,
                            userID INTEGER,
                            progress INTEGER,
                            FOREIGN KEY (topicID) REFERENCES topics (topicID)
                            FOREIGN KEY (userID) REFERENCES users (userID))""")
        self.connection.commit()