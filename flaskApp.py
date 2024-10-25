from flask import Flask
import sqlalchemy
from flask_login import LoginManager
from flask_cors import CORS

from flaskModels import conn, curs, User
from flaskIndex import index
from flaskLogin import login
from flaskLogout import logout
from flaskRegister import register
from flaskStream import stream
from flaskManageFaces import faces

app = Flask(__name__, static_folder='../frontend/static')

app.config['SECRET_KEY'] = 'secret_key'
CORS(app)  # Enable CORS for all routes

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'

login_manager = LoginManager()
login_manager.init_app(app)
#db.init_app(app) # for sqlalchemy
app.app_context().push()

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(stream)
app.register_blueprint(faces)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)