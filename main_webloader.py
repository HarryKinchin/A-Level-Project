from flask import Flask, render_template, request, send_from_directory, make_response, redirect, request, session
from databases import *

app = Flask(__name__)

# creating secret key for use in session data
import secrets
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
   session.pop('username')
   return redirect('/login')

@app.route('/account')
def account():
    if 'username' in session:
        username = session['username']
        email = session['email']
        return render_template('account_page.html', name=username, email=email)
    else:
        return redirect('/login')

@app.route('/login_check', methods=['POST'])
def login_check():
    login_oop = users_table()
    if login_oop.login_find(request.form.get('uname'), request.form.get('pword'), request.form.get('email')):
        session['username'] = request.form.get('uname')
        session['email'] = request.form.get('email')
        return redirect('/account')
    else:
        return render_template('failure.html')

@app.route('/register', methods=['POST','GET'])
def registering():
    login_oop = users_table()
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
