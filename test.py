from flask import Flask, render_template, request, send_from_directory
app = Flask(__name__)
  
@app.route('/')       
def login(): 
    return render_template("login_page.html")

if __name__=='__main__': 
   app.run() 
