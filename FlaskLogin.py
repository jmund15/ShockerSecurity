import SQLiteConnect

from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

from flaskModels import conn, curs, User, LoginForm

from SQLiteConnect import checkUser

# app = Flask(__name__)
# app.debug=True
login = Blueprint('login', __name__, template_folder='../frontend')
login_manager = LoginManager(login)
#login_manager.login_view = "login"
login_manager.init_app(login)

@login_manager.user_loader
def load_user(form):
   lu = checkUser(form.email.data, form.password.data)
   return lu
   # if lu is None:
   #    return None
   # else:
   #    return User(int(lu[0]), lu[1], lu[2])
  
@login.route("/login", methods=['GET','POST'])
def show():
  if current_user.is_authenticated:
     return redirect(url_for('profile'))
  form = LoginForm()
  if form.validate_on_submit():
     Us = load_user(form)
     if Us is not None:
        login_user(Us, remember=form.remember.data)
        Umail = list({form.email.data})[0].split('@')[0]
        flash('Logged in successfully '+Umail)
        redirect(url_for('stream.show'))
     else:
        flash('Login Unsuccessfull.')
  return render_template('login.html',title='Login', form=form)
  

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#if __name__ == '__main__':
    #init_db()  # Ensure the database is initialized
    #app.run(host='0.0.0.0', port=5000)
