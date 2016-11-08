from flask import Flask, render_template, request, url_for, redirect, session, flash
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

            errorMsg = 'Oops, that email is already registered, need your password reset?'

            return render_template('register.html', errorMsg=errorMsg)   
        
        user = user_datastore.create_user(name=request.form['firstname'], 
        email=request.form['email'], 
        password=request.form['password'],
        access=request.form['access'])
        user_datastore.commit()

        sucessMsg = 'Success you registered!, navigate to the Rosters page, to continue'
        session['firstname'] = request.form['firstname']
        return render_template('register.html', sucessMsg=sucessMsg)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':

        return render_template('login.html')

    if request.method == 'POST':
        
        user = user_datastore.find_user(name=request.form['firstname'],
        email=request.form['email'], password=request.form['password'])

        if user is not None:

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

@app.route('/useradmin', methods=['GET', 'POST'])
def useradmin():
    
    if session:
        
        if request.method == 'GET':
            
            return render_template('useradmin.html')

        if request.method == 'POST':

            user = User()
            user.name = request.form['name']
            user.email = request.form['email']
            user.password = request.form['password']
            user.access = request.form['access']
            user.save()

            return render_template('useradmin.html')

        
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if session:
        
        if request.method == 'POST':
            
            try:
                roster = Roster()
                roster.dayofweek = request.form['dayofweek']
                roster.date = request.form['date']
                roster.startandendtime = request.form['startandendtime']
                roster.notes = request.form['notes']
                roster.save()

                successMsg = 'Success, results saved successfully, please navigate to the Roster page to view results'

                return render_template('admin.html', successMsg=successMsg)

            except Exception:
                
                errorMsg = 'Come on, you can do better than that, please check the feilds and try again.'

                return render_template('admin.html', errorMsg=errorMsg)
                
        if request.method == 'GET':
            
            return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('firstname', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(threaded=True,debug=True, port=5000)