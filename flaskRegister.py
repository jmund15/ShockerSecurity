from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from flaskModels import User
from SQLiteConnect import addUser

register = Blueprint('register', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(register)

@register.route('/register', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if email and password and confirm_password:
            if password == confirm_password:
                if (addUser(email, password)):
                    return redirect(url_for('login.show') + '?success=account-created')
                else:
                    return redirect(url_for('register.show') + '?error=user-or-email-exists')
                # try:
                #     # new_user = User(
                #     #     #USER ID HERE
                #     #     email=email,
                #     #     password=hashed_password,
                #     # )
                #     addUser(email, password)
                # except : # IF EMAIL IS ALREADY ENTERED

        else:
            return redirect(url_for('register.show') + '?error=missing-fields')
    else:
        return render_template('register.html')