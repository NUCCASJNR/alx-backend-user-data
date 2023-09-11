#!/usr/bin/env python3

from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin
from flask_login import LoginManager, login_user, login_required, logout_user
from os import getenv
from flask_mail import Mail, Message
import bcrypt

user = getenv("prep_user")
pwd = getenv("prep_pwd")
db_name = getenv("prep_db")
host = getenv("prep_host")
email = getenv("email")
email_pwd = getenv("email_pwd")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hack_it_if_you_can221'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqldb://{user}:{pwd}@{host}/{db_name}'
app.config['USER_EMAIL_SENDER_EMAIL'] = email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_PASSWORD'] = email_pwd
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = 'auth_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)


user_manager = UserManager(app, db, User)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(username=username, email=email, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_value = request.form['input_value']
        password = request.form['password']
        if '@' in input_value:
            user = User.query.filter_by(email=input_value).first()
        else:
            user = User.query.filter_by(username=input_value).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
