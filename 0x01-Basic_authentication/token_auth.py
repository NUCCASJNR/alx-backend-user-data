#!/usr/bin/env python3

"""This module implements the token auth type of authentication"""

from flask import Flask
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


@auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()


@app.route('/admin')
@auth.login_required(role='admin')
def admins_only():
    return "Hello {}, you are an admin!".format(auth.current_user())


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


if __name__ == '__main__':
    app.run(debug=True)
