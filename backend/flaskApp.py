from datetime import timedelta
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_wtf import CSRFProtect

#from flaskModels import User
from flaskIndex import index
from flaskLogin import login, login_manager
from flaskLogout import logout
from flaskRegister import register
from flaskStream import stream, init_video, camera_inited
from flaskManageFaces import faces

from SQLiteConnect import initialize_db
from sendEmail import alertUsers

app = Flask(__name__, static_folder='../frontend/static')
app.debug = False
app.config['SECRET_KEY'] = 'secret_key'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=100)#days=1)  # Optional: Set duration for remember cookie
app.config['SESSION_COOKIE_SECURE'] = False
CORS(app, supports_credentials=True)  # Enable CORS for all routes
csrf = CSRFProtect(app) # Enable CSRF protection

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
#login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.show'
#db.init_app(app) # for sqlalchemy
#app.app_context().push()

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(stream)
app.register_blueprint(faces)
   
if __name__ == '__main__':
    #print('running main!')
    initialize_db()
    alertUsers("C:\\Users\\jmund\\WSU Shtuff\\CS 598\\ShockerSecurity\\Dr. Joel\\image_0.jpg")
    #if not camera_inited:
    #init_video()
    #app.run(host='0.0.0.0', port=3000)
