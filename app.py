from flask import Flask, render_template, request, url_for, redirect, session
from model import client
from flask_login import LoginManager, login_required
import bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
db = client.user

@app.route("/")
def index():
    gettingStarted = 'Getting Started'
    login = 'Login'
    return render_template('index.html',
    gettingstarted=gettingStarted, login=login)
    
    
@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'GET':

        return render_template('register.html')
    
    if request.method == 'POST':

        # - Check for exsisting User

        exsistingUser = db.user.find_one({"email" : request.form['email']})
        
        if exsistingUser is not None:

            return 'That email already exsists, need to reset your password?'

        user = db.user.insert_one({"firstname" : request.form['firstname']})
        email = db.user.insert_one({"email" : request.form['email']})
        password = db.user.insert_one({"password" : request.form['password']})

        return 'Success you registered!'

        session['firstname'] = request.form['firstname']      

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        return render_template('login.html')

    if request.method == 'POST':
        
        user = db.user.find_one({"email" : request.form['email']})
        password = db.user.find_one({"password" : request.form['password']})

    if user and password is not None:
        
        return 'Welcome'
        session['firstname'] = True
 
    return render_template('error.html')
        
@app.route('/logout')
@login_required    
def logout():

    return redirect(url_for('index'), logout=logout)   


if __name__ == "__main__":
    app.run(threaded=True,port=5000, debug=True)