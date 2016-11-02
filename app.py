from flask import Flask, render_template, request, url_for, redirect, session, g
from model import User, user_datastore
from flask.ext.security import Security, MongoEngineUserDatastore, \
UserMixin, login_required
import os
from werkzeug import security as sec

app = Flask(__name__)
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
        exsistingUser = user_datastore.find_user(email=request.form['email'])
        
        if exsistingUser is not None:

            return 'That email already exsists, need to reset your password?'   
        
        user = user_datastore.create_user(name=request.form['firstname'], 
        email=request.form['email'], 
        password=request.form['password'])
        user_datastore.commit()

        return 'Success you registered!'   

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        return render_template('login.html')

    if request.method == 'POST':

        user = user_datastore.find_user(name=request.form['firstname'])
        email = user_datastore.find_user(email=request.form['email'])
        password = user_datastore.find_user(password=request.form['password'])

        if user and email and password is not None:
            
            return redirect(url_for('index'))
            
        return render_template('error.html')
        
@app.route('/logout')
def logout():

    return redirect(url_for('index'))   


if __name__ == "__main__":
    app.run(threaded=True,debug=True, port=5000)