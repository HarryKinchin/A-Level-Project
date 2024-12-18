from flask import Flask, render_template, request, send_from_directory, make_response, redirect
from databases import *

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main_page.html')

@app.route('/login')       
def login(): 
    return render_template('login_page.html')

@app.route('/account/<username>')
def account():
    return render_template('account_page.html')

@app.route('/login_check', methods=['POST'])
def login_check():
    login_oop = users_table()
    if login_oop.login_find(request.form.get('uname'), request.form.get('pword'), request.form.get('email')):
        username = request.form.get('uname')
        return redirect(f'/account/{username}')
    else:
        return render_template('failure.html')

@app.route('/register', methods=['POST'])
def registering():
    login_oop = users_table()
    if login_oop.create_login(request.form.get('new_uname'), request.form.get('new_pword'), request.form.get('new_email')):
        return redirect('/login')
    else:
        return render_template('failure.html')
    
@app.route('/subjects')
def subjects():
    return render_template('subjects.html')

if __name__=='__main__': 
   app.run(debug=True)
