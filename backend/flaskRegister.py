from flask import Blueprint, url_for, render_template, redirect, request, flash
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from flaskModels import User, RegisterForm
from flaskLogin import login_manager
from SQLiteConnect import addUser

register = Blueprint('register', __name__, template_folder='../frontend')
#login_manager = LoginManager()
#login_manager.init_app(register)

@register.route('/register', methods=['GET', 'POST'])
def show():
    form = RegisterForm()  # Create an instance of RegisterForm

    if form.validate_on_submit():  # Validate the form
        email = form.email.data
        password = form.password.data

        if addUser(email, password):
            flash('Account created successfully!', 'success')  # Flash message for success
            return redirect(url_for('login.show') + '?success=account-created')
        else:
            flash('User or email already exists.', 'error')  # Flash message for error

    # If GET request or form is not valid, render the registration page
    return render_template('register.html', title='ShockerSecurity User Registration', form=form)

    # if request.method == 'POST':
    #     email = request.form['email']
    #     password = request.form['password']
    #     confirm_password = request.form['confirm-password']

    #     if email and password and confirm_password:
    #         if password == confirm_password:
    #             if (addUser(email, password)):
    #                 return redirect(url_for('login.show') + '?success=account-created')
    #             else:
    #                 return redirect(url_for('register.show') + '?error=user-or-email-exists')
    #             # try:
    #             #     # new_user = User(
    #             #     #     #USER ID HERE
    #             #     #     email=email,
    #             #     #     password=hashed_password,
    #             #     # )
    #             #     addUser(email, password)
    #             # except : # IF EMAIL IS ALREADY ENTERED

    #     else:
    #         return redirect(url_for('register.show') + '?error=missing-fields')
    # else:
    #     return render_template('register.html')