from flask import Flask, render_template, request, send_from_directory, make_response, redirect
app = Flask(__name__)

@app.route('/')
def main():
    return render_template("main_page.html")
  
@app.route('/login')       
def login(): 
    return render_template("login_page.html")

@app.route('/account')
def account():
    return render_template("account_page.html")

@app.route('/login_check', methods=["POST"])
def login_check():
    print(request.form)
    if request.form.get("uname") == "hello" and request.form.get("pword") == "no":
        return redirect("/account")
    else:
        return render_template("failure.html")

if __name__=='__main__': 
   app.run(debug=True)
   