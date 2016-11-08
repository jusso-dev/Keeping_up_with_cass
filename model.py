from flask import Flask, request, redirect, url_for
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin, login_required
import os
from securemongoengine.fields import *

_key = 'workingWithAES256AlgorithmKey32B'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
# MongoDB Config
app.config['MONGODB_DB'] = 'KeepingUpWithCass'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

db = MongoEngine(app)

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    name = db.StringField(max_length=255)
    email = db.StringField(max_length=255, unique=True)
    password = EncryptedStringField(key=_key,max_length=40, required=True)
    access = db.StringField()
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

class Roster(db.Document, RoleMixin):
    dayofweek = db.StringField(required=True, min_length=5)
    date = db.StringField(required=True, min_length=5)
    startandendtime = db.StringField(required=True, min_length=10)
    notes = db.StringField(max_length=255)

user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)