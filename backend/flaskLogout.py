from flask import Blueprint, url_for, redirect, request
from flask_login import LoginManager, login_required, logout_user
from flask_wtf.csrf import CSRFProtect
from wtforms import Form

from flaskLogin import login_manager

logout = Blueprint('logout', __name__, template_folder='../frontend')
#login_manager = LoginManager()
#login_manager.init_app(logout)

@logout.route('/logout', methods=['POST'])
@login_required
def show():
    #form = Form()
    #if request.method == 'POST':
    print('logging out user!')
    print('Received CSRF token:', request.form.get('csrf_token'))
    logout_user()
    return redirect(url_for('login.show') + '?success=logged-out')
    