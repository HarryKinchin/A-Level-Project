import secrets
from flask import Flask, render_template, redirect, request, session
from databases import *
from datetime import timedelta
import re

app = Flask(__name__)

# creating secret key for use in session data
app.secret_key = secrets.token_bytes(nbytes=32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=3)

@app.route('/')
def main():
    if 'username' in session:
        username = session['username']
        return render_template('main_page.html', name=username)
    else:
        return redirect('/login')

@app.route('/login')       
def login(): 
    return render_template('login_page.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/account')
def account():
    if 'username' in session:
        username, email, userID = session['username'], session['email'], session['userID']
        subjectsuser_oop, subject_oop = SubjectUserTable(), SubjectsTable()
        subjectIDs = subjectsuser_oop.subIDs_get_from_userID(userID)
        subjects = subject_oop.subIDs_to_sub(subjectIDs)
        subs = []
        for item in subjects:
            subs.append(item)
        return render_template('account_page.html', name=username, email=email, subs=subs)
    else:
        return redirect('/login')
    
@app.route('/account/subject_change', methods=['POST','GET'])
def subject_change():
    userID = session['userID']
    subchange_oop = SubjectUserTable()
    subjects_selected = []
    if request.form.get('maths_check'):
        subjects_selected.append('1,true')
    else:
        subjects_selected.append('1,false')
    if request.form.get('comp_check'):
        subjects_selected.append('2,true')
    else:
        subjects_selected.append('2,false')
    subchange_oop.subject_change(userID, subjects_selected)
    return redirect('/account')

@app.route('/account/info_change', methods=['POST','GET'])
def info_change():
    userID = session['userID']
    login_oop = UsersTable()
    new_information = {'new_uname': request.form.get('new_uname'),
                       'new_email': request.form.get('new_email'),
                       'new_pass': request.form.get('new_password')}
    updated_info = login_oop.change_details(userID, request.form.get('old_password'), new_information)
    if updated_info == True:
        return redirect('/account')
    else:
        return render_template('account_failure.html')

@app.route('/login_check', methods=['POST','GET'])
def login_check():
    login_oop = UsersTable()
    if login_oop.login_check(request.form.get('uname'), request.form.get('pword'), request.form.get('email')):
        session['username'], session['email'] = request.form.get('uname'), request.form.get('email')
        session['userID'] = login_oop.userID_get(request.form.get('uname'), request.form.get('pword'), request.form.get('email'))
        return redirect('/account')
    else:
        return render_template('login_failure.html')

@app.route('/register', methods=['POST','GET'])
def registering():
    login_oop = UsersTable()
    if request.form.get('new_uname') == '' or request.form.get('new_pword') == '' or request.form.get('new_email') == '':
        return render_template('login_failure.html')
    elif re.fullmatch(r"[A-Za-z0-9]+", request.form.get('new_uname')) == None or re.fullmatch(r"[a-z]+[A-Z]+[0-9]+[!-\/:-@[-`{-~]+", request.form.get('new_pword')) or re.fullmatch(r"[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-A-Za-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[-A-Za-z0-9]*[A-Za-z0-9])?", request.form.get('new_email')):
        return render_template('login_failure.html')
    elif login_oop.create_login(request.form.get('new_uname'), request.form.get('new_pword'), request.form.get('new_email')):
        return redirect('/login')
    else:
        return render_template('login_failure.html')
    
@app.route('/subjects')
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

@app.route('/subjects/create_question', methods=["POST"])
def create_question():
    questions_oop = QuestionsTable()
    question_data = {"topic": request.form.get('topic_choice'),
                     "type": request.form.get('question_type'),
                     "name": request.form.get('question_name'),
                     "answer": request.form.get('question_answer')}
    print(question_data)
    questions_oop.create_question(question_data)
    return redirect('/subjects')

if __name__=='__main__': 
   app.run(debug=True)
