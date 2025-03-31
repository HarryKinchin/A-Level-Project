from flask import Flask, render_template, redirect, request, session
from datetime import timedelta
from databases import *
import secrets
import re

# creating the inital setup for the website (encryption and cookie expiry length)
app = Flask(__name__)
app.secret_key = secrets.token_bytes(nbytes=32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=3)

# landing page of website
@app.route('/', methods=['POST', 'GET'])
def main():
    if 'username' in session:   # this inital if statement (present in most app.routes) makes sure the user is logged in, if not then they will be prompted to login
        username = session['username']
        return render_template('main_page.html', name=username) # the use of the name value here will pass in the username from the cookie to be used on the html page, similar variables are used through each page to be used in the website
    else:
        return redirect('/login')

# login page
@app.route('/login', methods=['POST', 'GET'])       
def login(): 
    return render_template('login_page.html')

# this page will clear the cookie and send the user back to the login page
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# the account page displays all users personal details, with options to change when needed
@app.route('/account', methods=['POST', 'GET'])
def account():
    if 'username' in session:
        username, email, userID = session['username'], session['email'], session['userID']
        subjectsuser_oop, subject_oop = SubjectUserTable(), SubjectsTable() # this is how the code and use subroutines in the 'databases.py' file, and are used as and when needed throughout
        subjectIDs = subjectsuser_oop.subIDs_get_from_userID(userID)
        subjects = subject_oop.subIDs_to_sub(subjectIDs)
        subs = []
        for item in subjects:   # this is one of many methods used to convert the tuple (returned from sqlite select statements) to arrays, html does not work well with tuples and thus I made ways to change from tuples to arrays
            subs.append(item)
        return render_template('account_page.html', name=username, email=email, subs=subs)
    else:
        return redirect('/login')

# this is the way in which a user changes their subject choices    
@app.route('/account/subject_change', methods=['POST','GET'])
def subject_change():
    if 'username' in session:
        userID = session['userID']
        subchange_oop = SubjectUserTable()
        progress_oop = UserProgressTable()
        subjects_selected = []  # the following if statements separate the subjects so that they can be used to add/remove the default progress of the user
        if request.form.get('maths_check'):
            subjects_selected.append('1,true')
        else:
            subjects_selected.append('1,false')
        if request.form.get('comp_check'):
            subjects_selected.append('2,true')
        else:
            subjects_selected.append('2,false')
        subchange_oop.subject_change(userID, subjects_selected)
        for item in subjects_selected:
            split_item = item.split(',')
            if split_item[1] == 'false':
                progress_oop.del_progress(userID, split_item[0])
            else:
                progress_oop.add_progress(userID, split_item[0])    # this is knowingly a closed-minded way of coding, as it does not allow for expansion of other subjects
        return redirect('/account')
    else:
        return redirect('/login')
    
# this is where the user can change their account information
@app.route('/account/info_change', methods=['POST','GET'])
def info_change():
    if 'username' in session:
        userID = session['userID']
        login_oop = UsersTable()    # this uses a dictionary to get each piece of the data from the form
        new_information = {'new_uname': request.form.get('new_uname'), 
                           'new_email': request.form.get('new_email'),
                           'new_pass': request.form.get('new_password')}
        updated_info = login_oop.change_details(userID, request.form.get('old_password'), new_information)
        if updated_info == True:
            return redirect('/account')
        else:   # the failure page is a default page that changes based on the 'type' to suit where it got redirected from
            return render_template("failures.html", type="account") 
    else:
        return redirect('/login')

# this routine checks that the login details given match what is in the datbase, more depth given in the comments of the subroutine called
@app.route('/login_check', methods=['POST','GET'])
def login_check():
    login_oop = UsersTable()
    if login_oop.login_check(request.form.get('uname'), request.form.get('pword'), request.form.get('email')):
        session['username'], session['email'] = request.form.get('uname'), request.form.get('email')
        session['userID'] = login_oop.userID_get(request.form.get('uname'), request.form.get('pword'), request.form.get('email'))
        return redirect('/')
    else:
        return render_template("failures.html", type="login") 

# this is similar to the routine above, but instead checking that the details match all requirements
@app.route('/register', methods=['POST','GET'])
def registering():
    login_oop = UsersTable()
    if request.form.get('new_uname') == '' or request.form.get('new_pword') == '' or request.form.get('new_email') == '':
        return render_template("failures.html", type="registering")
    elif re.fullmatch(r"[A-Za-z0-9]+", request.form.get('new_uname')) == None or re.fullmatch(r"[a-z]+[A-Z]+[0-9]+[!-\/:-@[-`{-~]+", request.form.get('new_pword')) or re.fullmatch(r"[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?", request.form.get('new_email')):
        return render_template("failures.html", type="registering")
    elif login_oop.create_login(request.form.get('new_uname'), request.form.get('new_pword'), request.form.get('new_email')):
        return redirect('/login')
    else:
        return render_template("failures.html", type="registering") 

# this page displays the users' subjects, from which they can create questions of quizzes
@app.route('/subjects', methods=['POST', 'GET'])
def subjects():
    if 'username' in session:
        username, userID = session['username'], session['userID']
        subjectsuser_oop, subject_oop, topics_oop = SubjectUserTable(), SubjectsTable(), TopicsTable()
        subjectIDs = subjectsuser_oop.subIDs_get_from_userID(userID)
        subjects = subject_oop.subIDs_to_sub(subjectIDs)
        topics = topics_oop.get_topics(subjectIDs)
        subs = []
        for item in subjects:
            subs.append(item)
        topic_list = []
        for item in topics:
            topic_list.append(item)
        maths_topics = []
        comp_topics = []
        for item in topic_list:
            if item[0] == 1:
                maths_topics.append(item)
            else:
                comp_topics.append(item)
        return render_template('subjects.html', name=username, subs=subs, maths=maths_topics, comps=comp_topics)
    else:
        return redirect('/login')

# creating a question utilises a dictionary to parse in the data to be added to the database
@app.route('/subjects/create_question', methods=['POST', 'GET'])
def create_question():
    if 'username' in session:
        questions_oop = QuestionsTable()
        question_data = {"topic": request.form.get('topic_choice'),
                        "type": request.form.get('question_type'),
                        "name": request.form.get('question_name'),
                        "answer": request.form.get('question_answer')}
        questions_oop.create_question(question_data)
        return redirect('/subjects')
    else:
        return redirect('/login')

# creating a quiz requires all the data from a question to be used very specifically in the html code
@app.route('/subjects/create_quiz', methods=['POST', 'GET'])
def create_quiz():
    if 'username' in session:
        questions_oop = QuestionsTable()
        quiz_data = {"topic": request.form.get('topic_choice'),
                    "quiz_length": request.form.get('quiz_length')}
        question_data = questions_oop.create_quiz(quiz_data)
        length = []
        for i in range(1, int(quiz_data["quiz_length"])+1):
            length.append(i)
        if question_data[0] == True:
            list_of_tuples = question_data[1]
            list_of_lists = []
            for item in list_of_tuples:
                list_of_lists.append(list(item))
            return render_template('quiz.html', topic=quiz_data['topic'], length=length , questions=list_of_lists)
        else:
            return render_template("failures.html", type="quiz", topic=quiz_data['topic'])
    else:
        return redirect('/login')
    
# the progress page displays a users progress within a given topic, which they can choose and change as they deem fit
@app.route('/progress', methods=['POST', 'GET'])
def progress():
    if 'username' in session:
        username, userID = session['username'], session['userID']
        subjectsuser_oop, subject_oop, topics_oop, progress_oop = SubjectUserTable(), SubjectsTable(), TopicsTable(), UserProgressTable()
        subjectIDs = subjectsuser_oop.subIDs_get_from_userID(userID)
        subjects = subject_oop.subIDs_to_sub(subjectIDs)
        topics, rag_values = topics_oop.get_topics(subjectIDs), progress_oop.get_progress(userID)
        subs = []
        for item in subjects:
            subs.append(item)
        topic_list = []
        for item in topics:
            topic_list.append(item)
        maths_topics = []
        comp_topics = []
        for i in range(len(topic_list)):
            if topic_list[i][0] == 1:
                maths_topics.append([topic_list[i][1], rag_values[i]])
            else:
                comp_topics.append([topic_list[i][1], rag_values[i]])
        return render_template('user_progress.html', name=username, subs=subs, topics=topic_list, maths=maths_topics, comps=comp_topics)
    else:
        return redirect('/login')

# this allows users to change their progress of a given topic, on a scale of Red, Amber, Green
@app.route('/progress/change_progress', methods=['POST', 'GET'])
def change_progress():
    if 'username' in session:
        progress_oop = UserProgressTable()
        userID = session['userID']
        change_data = {"userID": userID,
                       "topic": request.form.get("topic_choice"),
                       "rag": request.form.get("rag_choice")}
        progress_oop.change_progress(change_data)
        return redirect('/progress')
    else:
        return redirect('/login')

if __name__=='__main__':
   app.run(debug=True)
