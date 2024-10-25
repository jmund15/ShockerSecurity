from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from SQLiteConnect import dbConnect

from flaskModels import User, Face
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# app = Flask(__name__)
# app.debug=True

# conn, curs = dbConnect()

class User(UserMixin):
    def __init__(self, id, email, password):
         self.id = str(id)
         self.email = email
         self.password = password
         self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id

class Face():
     def __init__(self, id, name, accepted, encodings, picture):
          self.id = id
          self.name = name
          self.accepted = accepted
          self.encodings = encodings
          self.picture = picture
     
class LoginForm(Form):
    email        = StringField('Email Address', [validators.Length(min=6, max=35)])
    password     = PasswordField('Password', [validators.Length(min=6, max=20)])
    #accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])
