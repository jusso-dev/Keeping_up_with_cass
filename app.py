from flask import Flask, render_template, request, url_for, redirect, session
from model import User, user_datastore, Role, Roster, db
from flask.ext.security import Security, MongoEngineUserDatastore, \
UserMixin, login_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

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

            return 'That email already exsists, need to reset your password?'   
        
        user = user_datastore.create_user(name=request.form['firstname'], 
        email=request.form['email'], 
        password=request.form['password'])
        user_datastore.commit()

        session['firstname'] = request.form['firstname']
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

            session['firstname'] = request.form['firstname']
            return redirect(url_for('roster'))

        return render_template('error.html')


@app.route('/roster', methods=['GET', 'POST'])
def roster():
    if session:

        rosters = Roster.objects
        
        return render_template('roster.html', rosters=rosters)
        
    else:
        
        return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if session:
        
        if request.method == 'POST':
            
            roster = Roster()
            roster.dayofweek = request.form['dayofweek']
            roster.date = request.form['date']
            roster.startandendtime = request.form['startandendtime']
            roster.notes = request.form['notes']
            roster.save()

            return render_template('admin.html')
    
        if request.method == 'GET':
            
            return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('firstname', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(threaded=True,debug=True, port=5001)