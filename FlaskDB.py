from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app = Flask(__name__)
app.debug=True

@app.route('/')
def index():
    conn = get_db_connection()
    faces = conn.execute('SELECT * FROM faces').fetchall()
    conn.close()
    return render_template('index.html', posts=faces)