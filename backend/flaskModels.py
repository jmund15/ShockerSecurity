from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import Form, SubmitField, BooleanField, EmailField, StringField, PasswordField, validators

#from SQLiteConnect import dbConnect

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
         #self.authenticated = False
    def is_active(self):
        return True  # Always active for now
    def is_anonymous(self):
        return False  # Not an an
    def is_authenticated(self):
        return True  # This will be true when the user is logged in
    def get_id(self):
        return self.id

class Face():
    def __init__(self, id, name, accepted, encodings, image_path):
        self.id = id
        self.name = name
        self.accepted = accepted
        self.encodings = encodings
        self.image_path = image_path
        
    def to_dict(self):
        return {
            'id': self.id, 
            'name': self.name,
            'accepted': self.accepted,
            'face': self.image_path  # Adjust if you need a different representation for the face
        }
     
class LoginForm(FlaskForm):
    email        = EmailField('Email Address', [
         validators.Length(min=6, max=35),
         validators.DataRequired(),
         validators.Email()  # Optional: validates the email format
        ])
    password     = PasswordField('Password', [
         validators.Length(min=6, max=20),
         validators.DataRequired()])
    remember = BooleanField('Remember Me') 
    #accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])

class LogoutForm(FlaskForm):
    submit = SubmitField('Logout')
class RegisterForm(FlaskForm):
    email = EmailField('Email Address', [
        validators.Length(min=6, max=35),
        validators.DataRequired(),
        validators.Email()  # Optional: validates the email format
    ])
    password = PasswordField('Password', [
        validators.Length(min=6, max=20),
        validators.DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password', [
        validators.EqualTo('password', message='Passwords must match'),
        validators.DataRequired()
    ])
