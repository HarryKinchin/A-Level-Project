import secrets
from flask import Flask, render_template, request, send_from_directory, make_response, redirect, request, session
from databases import *

app = Flask(__name__)


# creating secret key for use in session data
app.secret_key = secrets.token_bytes(nbytes=32)

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
    return redirect('/login')

@app.route('/account')
def account():
    if 'username' in session:
        username, email, userID = session['username'], session['email'], session['userID']
        subjects_oop = SubjectUserTable()
        subjects = subjects_oop.subIDs_get_from_userID(userID)
        if len(subjects) == 2:
            sub1 = 'Mathematics'
            sub2 = 'Computer Science'
        elif len(subjects) == 1:
            if subjects[0] == 'Mathematics':
                sub1 = 'Mathematics'
                sub2 = ''
            else:
                sub1 = ''
                sub2 = 'Computer Science'
        else:
            sub1 = ''
            sub2 = ''
        return render_template('account_page.html', name=username, email=email, maths=sub1, compsci=sub2)
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

@app.route('/login_check', methods=['POST'])
def login_check():
    login_oop = UsersTable()
    if login_oop.login_find(request.form.get('uname'), request.form.get('pword'), request.form.get('email')):
        session['username'], session['email'] = request.form.get('uname'), request.form.get('email')
        session['userID'] = login_oop.userID_get(request.form.get('uname'), request.form.get('pword'), request.form.get('email'))
        return redirect('/account')
    else:
        return render_template('failure.html')

@app.route('/register', methods=['POST','GET'])
def registering():
    login_oop = UsersTable()
    if login_oop.create_login(request.form.get('new_uname'), request.form.get('new_pword'), request.form.get('new_email')):
        return redirect('/login')
    else:
        return render_template('failure.html')
    
@app.route('/subjects')
def subjects():
    if 'username' in session:
        username = session['username']
        return render_template('subjects.html', name=username)
    else:
        return redirect('/login')

if __name__=='__main__': 
   app.run(debug=True)
