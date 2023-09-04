#!/usr/bin/env python3
"""This module implements the basic auth feature of authentication"""
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash('idan'),
    "susan": generate_password_hash('idanre')
 }


@auth.verify_password
def verify_password(username: str, password: str):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


if __name__ == '__main__':
    app.run()
