from flask import Flask, render_template, request, url_for, redirect, session
from model import User, user_datastore
from flask.ext.security import Security, MongoEngineUserDatastore, \
UserMixin, login_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

