from flask import Flask, render_template, request, url_for, redirect, session, flash
from model import User, user_datastore, Role, Roster, db
from flask.ext.security import Security, MongoEngineUserDatastore, \
UserMixin, login_required
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
admin = Admin(app)

admin.add_view(ModelView(Roster))

@app.route("/")
def index():
    return render_template('index.html')
    
@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'GET':

        return render_template('register.html')
    
    if request.method == 'POST':

        # - Check for exsisting User
        exsistingUser = user_datastore.find_user(email=request.form['email'])
        
        if exsistingUser is not None:

            errorMsg = 'Oops, that email is already registered, need your password reset?'
 
            return render_template('register.html', errorMsg=errorMsg)

        firstname = request.form['firstname'].lower()
        email = request.form['email'].lower()
        passwordField = request.form['password']

        user = user_datastore.create_user(name=firstname,
        email=email, 
        password=passwordField)
        user_datastore.commit()

        sucessMsg = 'Success you registered!, navigate to the Rosters page, to continue'
        session['firstname'] = request.form['firstname']
        return render_template('register.html', sucessMsg=sucessMsg)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        return render_template('login.html')

    if request.method == 'POST':

        firstname = request.form['firstname'].lower()
        emailFeild = request.form['email'].lower()
        passwordField = request.form['password']
        
        user = user_datastore.find_user(email=emailFeild, 
        password=passwordField)

        if user is not None:

            session['firstname'] = request.form['firstname']
            if session:
                return redirect(url_for('roster'))

        errorMsg = 'Sorry, there was an issue logging you in, please check your email and password, and try again'

        return render_template('login.html', errorMsg=errorMsg)

@app.route('/roster', methods=['GET', 'POST'])
def roster():
    if session:

        rosters = Roster.objects
        
        return render_template('roster.html', rosters=rosters)
        
    else:
        
        return redirect(url_for('login'))

@app.route('/useradmin', methods=['GET', 'POST'])
def useradmin():
    
    if session:
        
        if request.method == 'GET':
            
            return render_template('useradmin.html')

        if request.method == 'POST':

            try:
                
                user = User()
                user.name = request.form['name']
                user.email = request.form['email']
                user.password = request.form['password']
                user.access = request.form['access']
                user.save()
                
                successMsg = 'Success, user added successfully!'
                
                return render_template('useradmin.html', successMsg=successMsg)
            
            except Exception:

                errorMsg = 'Sorry that did not work, please check the fields and try again'

                return render_template('useradmin.html', errorMsg=errorMsg)

@app.route('/logout')
def logout():
    session.pop('firstname', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(threaded=True,debug=True, port=5000)